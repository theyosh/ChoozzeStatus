#!/usr/bin/env python3
# -*- coding: utf-8 -*-

DEBUG = False
MOCKDATA = False

JOLLA = False
try:
  import pyotherside
  JOLLA = True
except:
  pass

import re
import http.cookiejar
import urllib.request, urllib.error, urllib.parse
import math
import time
import json
import threading
from datetime import date, datetime

import Encryption

if MOCKDATA:
  import MockData

class ChoozzeScraper:

  update_timeout = 3600 # 1 Hours timeout
  data_file = '.ChoozzeScraper.data.bin' # Hidden data file
  history_file = '.ChoozzeScraper.history.bin' # Hidden data file

  def __init__(self, username = None ,password = None):
    try:
      self.encryption = Encryption.Encryption()
    except Encryption.EncryptionException as error:
      self.__notify_message('notification','Encryption error ' + str(error))

    self.encryption = Encryption.Encryption()
    self.__notify_message('notification','Encryption is ' + ('enabled' if self.encryption.isEnabled() else 'disabled'))

    self.portal_url   = 'https://choozze.me'
    self.online_pages = {'login':'login.php',
                         'account':'',
                         'voicemail':'voicemail.php',
                         'callforward': 'forward.php'}

    self.login_cookie = None
    self.login_ok = False

    self.reset_settings(False)

    # Login regexes
    self.login_detect_regex = re.compile('<input type=("|\')?hidden("|\')? name=("|\')?action("|\')? value=("|\')?login("|\')? />')
    self.valid_email_regex  = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
    self.regex_logged_in    = re.compile('Welkom Choozzer!')

    # Account regexes
    self.regex_phonenumber = re.compile('<p>.*nummer:\s(?P<phonenumber>\+\d{11})\s*<\/p>')
    self.regex_mobile_plan = re.compile('<p>.*gekozen voor\s*(?P<mobileplan>[^</]+)<\/p>')
    self.regex_extra_costs = re.compile('<p>Buitenbundelkosten:\s(?P<currentcy>.*)(?P<extra_costs>\d+,\d+)\s*<\/p>')
    self.regex_sms_usage   = re.compile('(?P<totalsms>\d+) SMSjes voor \S+ \((?P<usedsms>\d+)%[^</]+')
    self.regex_call_usage  = re.compile('(?P<totalcall>\d+) belminuten voor \S+ \((?P<usedcall>\d+)%[^</]+')
    self.regex_data_usage  = re.compile('(?P<totaldata>\d+)(?P<dataunit>[(M|G)B]+) mobiel internet \S+ \((?P<useddata>\d+)%[^</]+')
    self.internetdata_unit = 1000

    # Voicemail regexes
    self.regex_voicemail_active = re.compile('Jouw voicemail is\s?(?P<active>[^\s]+)? actief')
    self.regex_voicemail_pin    = re.compile('placeholder=("|\')?Pincode("|\')?.*value=("|\')?(?P<pincode>\d{4})("|\')?')
    self.regex_voicemail_email  = re.compile('type=("|\')?email("|\')?.*value=("|\')?(?P<voicemailemail>[^("|\')?]+)("|\')?')

    # Callforward regexes
    self.regex_callforward_direct = re.compile('type=("|\')?text("|\')?.*((name|id)=("|\')?cfim("|\')?){1,2}.*value=("|\')?(?P<direct>[^("|\')?]+)("|\')?')
    self.regex_callforward_busy   = re.compile('type=("|\')?text("|\')?.*((name|id)=("|\')?cfbs("|\')?){1,2}.*value=("|\')?(?P<busy>[^("|\')?]+)("|\')?')

    self.__load_application_data()

    self.__history_fields = {'data_update_timeout', 'mobile_plan','extra_costs','sms_usage','call_usage','data_usage','days_usage','voicemail_active','callforward_active'}

    self.__load_application_history()

    if username is not None:
      self.set_username(username)

    if password is not None:
      self.set_password(password)

    if self.login():
      self.__get_online_data()

    self.updater = threading.Thread(target=self.__auto_update)
    self.updater.daemon = True
    self.updater.start()

  def __notify_message(self,type,message):
    if JOLLA:
      pyotherside.send(type,str(message))

  def __print_debug(self,message):
    if DEBUG:
      self.__notify_message('notification',str(message))
      print('DEBUG: ' + str(message))

  def __load_application_data(self):
    try:
      with open(ChoozzeScraper.data_file, mode='rb') as data_file:
        old_application_data = json.loads(self.encryption.decrypt(data_file.read()))
        self.application_data = dict(list(self.application_data.items()) + list(old_application_data.items()))
    except Exception as e:
      self.__notify_message('notification','Error loading data exception: ' + str(e))

  def __save_application_data(self):
    try:
      with open(ChoozzeScraper.data_file, mode='wb') as data_file:
        data_file.write(self.encryption.encrypt(json.dumps(self.application_data)))
    except Exception as e:
      self.__notify_message('notification','Error saving data exception: ' + str(e))

  def __load_application_history(self):
    try:
      with open(ChoozzeScraper.history_file, mode='rb') as data_file:
        old_history_data = json.loads(self.encryption.decrypt(data_file.read()))
        self.history_data = dict(list(self.history_data.items()) + list(old_history_data.items()))
    except Exception as e:
      self.__notify_message('notification','Error loading history exception: ' + str(e))

  def __save_application_history(self):
    try:
      with open(ChoozzeScraper.history_file, mode='wb') as data_file:
        data_file.write(self.encryption.encrypt(json.dumps(self.history_data)))
    except Exception as e:
      self.__notify_message('notification','Error saving history exception: ' + str(e))

  def __add_history(self):
      history = {}
      for data_field in self.__history_fields:
          history[data_field] = self.application_data[data_field]

      self.history_data[str(self.application_data['last_update'])] = history
      self.__print_debug('Added data to history')
      self.__print_debug(self.history_data)
      self.__save_application_history()

  def __init_online_session(self):
    self.login_cookie = http.cookiejar.CookieJar()

    self.opener = urllib.request.build_opener(
        urllib.request.HTTPRedirectHandler(),
        urllib.request.HTTPSHandler(debuglevel=0),
        urllib.request.HTTPCookieProcessor(self.login_cookie))

    urllib.request.install_opener(self.opener)

  def __get_online_data(self,page = None,data = None,force_update = False):
    # Get online data when:
    #    1. Forced
    #    2. Postdata
    #    3. Outdated
    last_update = int(time.time()) - int(self.application_data['last_update'])
    self.__print_debug('Get online data for page: ' + str(page) + ' -> Forced: ' + str(force_update) + ', Data: ' + str(data is not None) + ', Outdated: ' + str(last_update > self.application_data['data_update_timeout']) + ', ' + str( int(self.application_data['data_update_timeout']) - (int(time.time()) - self.application_data['last_update'])) + ' seconds left')
    if force_update or (data is not None) or ( last_update > int(self.application_data['data_update_timeout'])):
      pages = ['account','voicemail','callforward']
      if data is not None:
          pages = [page]

      for page in pages:
        html = self.__process_online_data(page,data)
        self.__parse_data(page,html)
        self.__print_debug('Downloaded online data for page ' + page)

      self.application_data['last_update'] = int(time.time())
      self.__add_history();
      self.__save_application_data()

  def __process_online_data(self,page,data = None):
    html = ''
    if page in self.online_pages:
      if MOCKDATA:
        self.__print_debug('Using MOCK Data for page ' + page)
        html = MockData.getpage(page)
      else:
        post_data = None
        if data is not None:
          post_data = urllib.parse.urlencode(data).encode('utf-8')

        response = self.opener.open(self.portal_url + '/' + self.online_pages[page],post_data)
        html = response.read().decode('utf-8')
        if page != 'login' and self.login_detect_regex.search(html):
          #self.__notify_message('notification','Cookie expired, relogin for page' + page)
          if self.login():
            self.__print_debug('Recursive restart processing online data')
            html = self.__process_online_data(page,data)

    return html

  def __auto_update(self):
    while True:
      self.__print_debug('Auto update loop')
      if self.isLoggedIn():
        last_update = self.application_data['last_update']
        self.__get_online_data()

        if self.application_data['last_update'] != last_update:
          self.__notify_message('update-data','Updated data!')
      else:
          self.__print_debug('Not logged in (yet)')

      self.__print_debug('Do a new update in ' + str(ChoozzeScraper.update_timeout) + ' seconds')
      time.sleep(ChoozzeScraper.update_timeout)

  def __parse_data(self,type,html):
    if html == '':
      return

    if type in self.online_pages:
      if 'account' == type:
        self.__parse_account_data(html)
      if 'voicemail' == type:
        self.__parse_voicemail_data(html)
      if 'callforward' == type:
        self.__parse_callforward_data(html)

  def __parse_account_data(self,html):
    self.application_data['mobile_number'] = self.regex_phonenumber.search(html).group('phonenumber')
    self.application_data['mobile_plan']   = self.regex_mobile_plan.search(html).group('mobileplan')
    self.application_data['extra_costs']   = self.regex_extra_costs.search(html).group('extra_costs')

    sms_usage = self.regex_sms_usage.search(html)
    if sms_usage:
      self.application_data['sms_usage']['total'] = int(sms_usage.group('totalsms'))
      self.application_data['sms_usage']['used'] = int(float(self.application_data['sms_usage']['total']) * (float(sms_usage.group('usedsms')) / 100))

      # Mock data
      if MOCKDATA:
        self.application_data['sms_usage']['used'] =  MockData.random(self.application_data['sms_usage']['total'])

      self.application_data['sms_usage']['free'] = int(self.application_data['sms_usage']['total']) - int(self.application_data['sms_usage']['used'])

    call_usage = self.regex_call_usage.search(html)
    if call_usage:
      self.application_data['call_usage']['total'] = int(call_usage.group('totalcall'))
      self.application_data['call_usage']['used'] = int(float(self.application_data['call_usage']['total']) * (float(call_usage.group('usedcall')) / 100))

      # Mock data
      if MOCKDATA:
        self.application_data['call_usage']['used'] =  MockData.random(self.application_data['sms_usage']['total'])

      self.application_data['call_usage']['free'] = int(self.application_data['call_usage']['total']) - int(self.application_data['call_usage']['used'])

    data_usage = self.regex_data_usage.search(html)
    if data_usage:
      self.application_data['data_usage']['total'] = int(float(data_usage.group('totaldata')) * self.__data_unit_factor(data_usage.group('dataunit')))
      self.application_data['data_usage']['used'] = int(float(self.application_data['data_usage']['total']) * (float(data_usage.group('useddata')) / 100))

      # Mock data
      if MOCKDATA:
        self.application_data['data_usage']['used'] =  MockData.random(self.application_data['data_usage']['total'])

      self.application_data['data_usage']['free'] = int(self.application_data['data_usage']['total']) - int(self.application_data['data_usage']['used'])

    now = date.today()
    self.application_data['days_usage']['total'] = (date(now.year, now.month+1, 1) - date(now.year, now.month, 1)).days
    self.application_data['days_usage']['used']  = now.day
    self.application_data['days_usage']['free']  = int(self.application_data['days_usage']['total']) - int(self.application_data['days_usage']['used'])


  def __parse_voicemail_data(self,html):
    match = self.regex_voicemail_active.search(html)
    if match:
      self.application_data['voicemail_active'] = match.group('active') is None or (match.group('active').strip()).lower() != 'niet'

    match = self.regex_voicemail_pin.search(html)
    self.application_data['voicemail_pin'] = ''
    if match and match.group('pincode') is not None:
      self.application_data['voicemail_pin'] = match.group('pincode')

    match = self.regex_voicemail_email.search(html)
    self.application_data['voicemail_email'] = ''
    if match and match.group('voicemailemail') is not None:
      self.application_data['voicemail_email'] = match.group('voicemailemail')

  def __parse_callforward_data(self,html):
    match = self.regex_callforward_direct.search(html)
    self.application_data['callforward_direct'] = ''
    if match:
      self.application_data['callforward_direct'] = match.group('direct')

    match = self.regex_callforward_busy.search(html)
    self.application_data['callforward_busy'] = ''
    if match:
      self.application_data['callforward_busy'] = match.group('busy')

    self.application_data['callforward_active'] = ( self.application_data['callforward_direct'] != '' or \
                                                    self.application_data['callforward_busy'] != '')


  def __set_voicemail_active(self,active):
    self.application_data['voicemail_active'] = active in [True,1,'True','true','on','On']

  def __set_voicemail_pin(self,pin):
    if re.match('^[0-9]{4}$',str(pin)):
      self.application_data['voicemail_pin'] = pin

  def __set_voicemail_email(self,email):
    if self.valid_email_regex.match(email):
      self.application_data['voicemail_email'] = email

  def __set_callforward_direct(self,direct):
    if direct is not None:
      self.application_data['callforward_direct'] = direct

  def __set_callforward_busy(self,busy):
    if busy is not None:
      self.application_data['callforward_busy'] = busy

  def __data_unit_factor(self,unit):
    if 'MB' == unit:
      return math.pow(self.internetdata_unit,2)
    elif 'GB' == unit:
      return math.pow(self.internetdata_unit,3)

    return float(1)


  # Public functions starts here
  def set_username(self,username):
    if username is not None and username != '' and self.valid_email_regex.match(username):
      self.application_data['username'] = username
      self.__save_application_data()

  def set_password(self,password):
    if password is not None and password != '':
      self.application_data['password'] = password
      self.__save_application_data()

  def set_data_update_timeout(self,timeout):
    if timeout is not None and timeout != '' and int(timeout) >= 2 and int(timeout) <= 24:
      self.application_data['data_update_timeout'] = int(timeout) * 3600
      self.__save_application_data()
      return True
    else:
      return False

  def set_credentials(self,username,password):
    self.set_username(username)
    self.set_password(password)
    return self.login()

  def get_username(self):
    return self.application_data['username']

  def get_password(self):
    return self.application_data['password']

  def login(self):
    self.__print_debug('Start login')
    self.login_ok = False

    if self.application_data['username'] is None or self.application_data['password'] is None:
      self.__print_debug('Login methode missing credentials')
      return False

    self.__init_online_session()

    login_data = {'action': 'login',
                  'login-username': self.application_data['username'],
                  'password': self.application_data['password'] }

    html = self.__process_online_data('login',login_data)

    self.login_ok = self.regex_logged_in.search(html) is not None
    if self.login_ok:
      self.__print_debug('Login successfull!!')
      self.login_ok = True

    return self.isLoggedIn()

  def isLoggedIn(self):
    return True == self.login_ok

  def get_account_data(self,force_update = False):
    self.__get_online_data(force_update = force_update)

    return_data = {}
    for item in self.application_data.keys():
      if 'voicemail_' not in item and 'callforward_' not in item:
        return_data[item] = self.application_data[item]

    return return_data

  def get_voicemail_data(self,force_update = False):
    self.__get_online_data(force_update = force_update)

    return_data = {}
    for item in self.application_data.keys():
      if 'voicemail_' in item:
        return_data[item] = self.application_data[item]

    return_data['last_update'] = self.application_data['last_update']
    return return_data

  def get_callforward_data(self,force_update = False):
    self.__get_online_data(force_update = force_update)

    return_data = {}
    for item in self.application_data.keys():
      if 'callforward_' in item:
        return_data[item] = self.application_data[item]

    return_data['last_update'] = self.application_data['last_update']
    return return_data

  def get_all_data(self,force_update = False):
    self.__get_online_data(force_update = force_update)
    return self.application_data

  def set_voicemail_settings(self, active = None, pin = None, email = None):
    self.__set_voicemail_active(active)
    self.__set_voicemail_pin(pin)
    self.__set_voicemail_email(email)

    post_data = {'action': 'vmsettings',
                 'vmpin': self.application_data['voicemail_pin'],
                 'vmemail': self.application_data['voicemail_email'] }

    if self.application_data['voicemail_active'] is True:
      post_data['vmactive'] = 'on'

    self.__get_online_data('voicemail',post_data)
    return True

  def set_callforward_settings(self, direct = None, busy = None):
    self.__set_callforward_direct(direct)
    self.__set_callforward_busy(busy)

    post_data = {'action': 'cfsettings',
                 'cfim': self.application_data['callforward_direct'],
                 'cfbs': self.application_data['callforward_busy'] }

    self.__get_online_data('callforward',post_data)
    return True

  def get_history(self,month = None,year = None):
    self.__print_debug('Get history data')

    # Create tempory history data array based on days
    history_data = {}

    for history_update_date in self.history_data:
      # Copy of the data
      data = self.history_data[history_update_date]
      data['last_update'] = int(history_update_date)

      # Create date index in format 20151121
      history_update_date = datetime.fromtimestamp(int(history_update_date)).strftime('%Y%m%d')

      if history_update_date not in history_data or history_data[history_update_date]['last_update'] < data['last_update']:
        history_data[history_update_date] = data

    self.__print_debug(history_data)
    return history_data

  def reset_settings(self, save = True):
    self.application_data = {
        'last_update': 0,
        'data_update_timeout': int(4 * 3600),
        'username': None,
        'password': None,
        'mobile_number': None,
        'mobile_plan': None,
        'extra_costs': None,
        'sms_usage':  {'total': None, 'used': None, 'free': None},
        'call_usage': {'total': None, 'used': None, 'free': None},
        'data_usage': {'total': None, 'used': None, 'free': None},
        'days_usage': {'total': None, 'used': None, 'free': None},

        'voicemail_active': None,
        'voicemail_pin': '',
        'voicemail_email': '',

        'callforward_active': None,
        'callforward_direct': '',
        'callforward_busy': '',
    }
    self.history_data = {}

    if save:
      self.__save_application_data()
      self.__save_application_history()

    return True

choozzescraper = ChoozzeScraper()
