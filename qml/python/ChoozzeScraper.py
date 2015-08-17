#!/usr/bin/env python3
# -*- coding: utf-8 -*-

JOLLA = False
try:
  import pyotherside
  JOLLA = True
except:
  pass

ENCRYPTION_IMPORT = False
try:
  import Crypto.Random
  from Crypto.Cipher import AES
  ENCRYPTION_IMPORT = True
except:
  pass
import subprocess
import hashlib

import re
import http.cookiejar
import urllib.request, urllib.error, urllib.parse
import math
import time
import random
import json
import os.path
import threading
from datetime import date
import time

class Encryption:
  #http://stackoverflow.com/questions/6425131/encrypt-decrypt-data-in-python-with-salt

  # salt size in bytes
  SALT_SIZE = 16

  # number of iterations in the key generation
  NUMBER_OF_ITERATIONS = 20

  # the size multiple required for AES
  AES_MULTIPLE = 16

  def __init__(self):
    self.__uniqe_key = None
    self.__enabled = False
    if ENCRYPTION_IMPORT:
      if self.__get_secret_key():
        self.__enabled = True
      else:
        if JOLLA:
          pyotherside.send('notification','Error getting secure key')
        print('Error getting secure key')
    else:
      if JOLLA:
        pyotherside.send('notification','No encryption modules available')
      print('No crypto modules')

    print('Encryption is ' + ('enabled' if self.isEnabled() else 'disabled'))

  def __get_secret_key(self):
    network_data = ''
    regex_hardwareaddress = re.compile('(?P<addr>([0-9a-f]{1,2}[\.:-]){5}([0-9a-f]{1,2}))',re.IGNORECASE)
    try:
      network_data = subprocess.check_output(['/sbin/ifconfig','wlan0'],universal_newlines=True)
    except CalledProcessError as a:
      if JOLLA:
        pyotherside.send('notification','Error generating secret key:' + str(a))

    key = regex_hardwareaddress.search(network_data)
    if key is not None:
      # Key needs to be in bytes
      self.__uniqe_key = str(key.group('addr')).encode()
      return True

    return False

  def isEnabled(self):
    return self.__enabled == True

  def generate_key(self, password, salt, iterations):
    assert iterations > 0
    key = password + salt
    for i in range(iterations):
      key = hashlib.sha256(key).digest()

    return key

  def pad_text(self, text, multiple):
    extra_bytes = len(text) % multiple
    padding_size = multiple - extra_bytes
    padding = chr(padding_size) * padding_size
    padded_text = text + padding
    return padded_text

  def unpad_text(self, padded_text):
    padding_size = ord(padded_text[-1])
    text = padded_text[:-padding_size]
    return text

  def encrypt(self,plaintext):
    if not self.isEnabled():
      return plaintext.encode()

    salt = Crypto.Random.get_random_bytes(Encryption.SALT_SIZE)
    key = self.generate_key(self.__uniqe_key, salt, Encryption.NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = self.pad_text(plaintext, Encryption.AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt

  def decrypt(self,ciphertext):
    if not self.isEnabled():
      return ciphertext.decode()

    salt = ciphertext[0:Encryption.SALT_SIZE]
    ciphertext_sans_salt = ciphertext[Encryption.SALT_SIZE:]
    key = self.generate_key(self.__uniqe_key, salt, Encryption.NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB)
    # Explicited decode back to str
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt).decode()
    plaintext = self.unpad_text(padded_plaintext)
    return plaintext


class ChoozzeScraper:

  data_update_timeout = 43200 # 12 Hours timeout
  update_timeout = 3600 # 1 Hours timeout
  data_file = '.ChoozzeScraper.data.bin' # Hidden data file

  MOCK = True
  DEBUG = True

  # Mock Data
  MOCK_data = """<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <meta name="description" content="">
  <meta name="author" content="">
  <link rel="icon" href="favicon.ico">
  <link rel="apple-touch-icon" href="apple-touch-icon.png"/>
  <link rel="apple-touch-icon-precomposed" href="apple-touch-icon.png"/>
  <link rel="icon" href="apple-touch-icon.png" type="image/png"/>

  <title>Choozze Me</title>

  <!-- Bootstrap core CSS -->
  <link href="css/bootstrap.min.css" rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="css/navbar-static-top.css" rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="css/signin.css" rel="stylesheet">
  <link href="css/style.css" rel="stylesheet">

  <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
  <script src="js/ie10-viewport-bug-workaround.js"></script>

  <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->
</head>

<body>

  <div>&nbsp;</div>

  <div class="container">

    <!-- Main component for a primary marketing message or call to action -->
    <div class="jumbotron">
      <h1>Welkom Choozzer!</h1>
      <p>Jouw Choozze nummer: +31600000009        </p>
      <p>
<p>Jij hebt gekozen voor Choozze Zero</p><b>Happiness verbruiksmeter</b><br/><div class="row"><div class="col-xs-12 col-md-8">100 SMSjes voor nop (13% gebruikt)</div><div class="col-xs-6 col-md-4"></div></div><div class="row"><div class="col-xs-12 col-md-8">100 belminuten voor nop (5% gebruikt)</div><div class="col-xs-6 col-md-4"></div></div><div class="row"><div class="col-xs-12 col-md-8">500MB mobiel internet NL (3% gebruikt)</div><div class="col-xs-6 col-md-4"><a class="btn btn-aanpassen btn-xs" href="https://choozze.me/changedata.php?addon=500MB">Bundel wijzigen</a></div></div><div class="row"><div class="col-xs-12 col-md-8">Geen Onderling bundel</div><div class="col-xs-6 col-md-4"><a class="btn btn-aanpassen btn-xs" href="https://choozze.me/changevoice.php?addon=geen">Bundel wijzigen</a></div></div><br/><div class="row"><div class="col-xs-12 col-md-8"><b>Europa</b><br/><i>Met de Europa bundel kan je kiezen uit 100MB, 200M of 400MB</i></div><div class="col-xs-6 col-md-4"><a class="btn btn-reserveren btn-sm" href="https://choozze.me/changeroaming.php?addon=roam100">Reserveer hier je Europa bundel</a></div></div></p><p>Buitenbundelkosten: &euro;0,00</p>
Buitenbundelkosten kunnen onder andere bevatten: Overschrijdingen van de aanwezige bundels,
kosten voor bellen naar servicenummers, kosten voor bellen naar het buitenland of roaming kosten
(indien geen Europa bundel actief is, of er buiten de EU is gereisd).
<br/><br/>
Let op: Verbruiksgegevens worden met enige vertraging weergegeven en dienen ter indicatie.
    </div>

  </div> <!-- /container -->


      <!-- Static navbar -->
    <div class="navbar navbar-default navbar-fixed-bottom" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="https://choozze.me/"><img src="https://choozze.me/img/choozze-logobutton-sm.png" alt="Mijn Choozze"></a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="https://choozze.me/voicemail.php">Voicemail</a></li>
            <li><a href="https://choozze.me/forward.php">Doorschakelen</a></li>
            <li><a href="https://choozze.me/apn.php">Internet</a></li>
            <li><a href="https://choozze.me/simcard.php">Simkaart</a></li>
            <li><a href="https://choozze.me/invoices.php">Facturen</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li><a href="https://choozze.me/contact.php">Contact</a></li>
            <li class="active"><form id="logout" name="logout" method="post" action="https://choozze.me/login.php"><input type="hidden" name="action" value="logout" /></form><a href="#" onClick="document.getElementById('logout').submit()">Logout</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div><!--/.container-fluid -->
    </div>
  <!-- Bootstrap core JavaScript
  ================================================== -->
  <!-- Placed at the end of the document so the pages load faster -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script type="text/javascript">
      $(document).ready(function(){
          if (typeof state !== 'undefined') {
              hideInvoices();

              $('#invoices-toggle').click(function (e) {
                  e.preventDefault();
                  toggleInvoiceView();
              });

          }
      });
  </script>
</body>
</html>
"""

  def __init__(self, username = None ,password = None):
    self.encryption = Encryption()
    if JOLLA:
      pyotherside.send('notification','Encryption is ' + ('enabled' if self.encryption.isEnabled() else 'disabled'))

    self.portal_url     = 'https://choozze.me'
    self.login_page     = 'login.php'
    self.voicemail_page = 'voicemail.php'
    self.forward_page   = 'forward.php'

    self.login_cookie = None
    self.login_ok = False

    self.application_data = {
        'last_update': None,
        'username': None,
        'password': None,
        'mobile_number': None,
        'mobile_plan': None,
        'extra_costs': None,
        'sms_usage':  {'total': None, 'used': None, 'free': None},
        'call_usage': {'total': None, 'used': None, 'free': None},
        'data_usage': {'total': None, 'used': None, 'free': None},
        'days_usage': {'total': None, 'used': None, 'free': None},
    }

    self.valid_email_regex = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
    self.regex_logged_in   = re.compile('Welkom Choozzer!')

    self.regex_phonenumber = re.compile('<p>.*nummer:\s(?P<phonenumber>\+\d{11})\s*<\/p>')
    self.regex_mobile_plan = re.compile('<p>.*gekozen voor\s*(?P<mobileplan>[^</]+)<\/p>')
    self.regex_extra_costs = re.compile('<p>Buitenbundelkosten:\s(?P<currentcy>.*)(?P<extra_costs>\d+,\d+)\s*<\/p>')
    self.regex_sms_usage   = re.compile('(?P<totalsms>\d+) SMSjes voor \S+ \((?P<usedsms>\d+)%[^</]+')
    self.regex_call_usage  = re.compile('(?P<totalcall>\d+) belminuten voor \S+ \((?P<usedcall>\d+)%[^</]+')
    self.regex_data_usage  = re.compile('(?P<totaldata>\d+)(?P<dataunit>[(M|G)B]+) mobiel internet \S+ \((?P<useddata>\d+)%[^</]+')
    self.internetdata_unit = 1000

    self.__load_application_data()

    if username is not None:
      self.set_username(username)

    if password is not None:
      self.set_password(password)

    self.login()

    self.updater = threading.Thread(target=self.__auto_update)
    self.updater.start()

  def __load_application_data(self):
    try:
      with open(ChoozzeScraper.data_file, mode='rb') as data_file:
        self.application_data = json.loads(self.encryption.decrypt(data_file.read()))
    except Exception as e:
      if JOLLA:
        pyotherside.send('notification','Error loading data excetpion: ' + str(e))
      if ChoozzeScraper.DEBUG:
        print('Load exception: ' + str(e))

  def __save_application_data(self):
    try:
      with open(ChoozzeScraper.data_file, mode='wb') as data_file:
        data_file.write(self.encryption.encrypt(json.dumps(self.application_data)))
    except Exception as e:
      if JOLLA:
        pyotherside.send('notification','Error saving data excetpion: ' + str(e))
      if ChoozzeScraper.DEBUG:
        print('Save exception: ' + str(e))

  def __auto_update(self):
    while True:
      if ChoozzeScraper.DEBUG:
        print('Print looop')
      if self.isLoggedIn():
        update_result = self.__update_data()
        if update_result == -1:
          if JOLLA:
            pyotherside.send('notification','Error updating data')
          if ChoozzeScraper.DEBUG:
            print('Error updating')
        elif update_result == 0:
          if JOLLA:
            pyotherside.send('notification','No new data available')
          if ChoozzeScraper.DEBUG:
            print('No new data')
        elif update_result == 1:
          if JOLLA:
            pyotherside.send('update-data','Updated data!')
          if ChoozzeScraper.DEBUG:
            print('Got new data!')
          self.__save_application_data()

      else:
          if JOLLA:
            pyotherside.send('notification','Not logged in (yet)')
          if ChoozzeScraper.DEBUG:
            print('Not logged in')

      if ChoozzeScraper.DEBUG:
        print('Do a new update in ' + str(ChoozzeScraper.update_timeout) + ' seconds')
      time.sleep(ChoozzeScraper.update_timeout)

  def __parse_account_data(self,html):
    self.application_data['mobile_number'] = self.regex_phonenumber.search(html).group('phonenumber')
    self.application_data['mobile_plan']   = self.regex_mobile_plan.search(html).group('mobileplan')
    self.application_data['extra_costs']   = self.regex_extra_costs.search(html).group('extra_costs')

    sms_usage = self.regex_sms_usage.search(html)
    if sms_usage:
      self.application_data['sms_usage']['total'] = float(sms_usage.group('totalsms'))
      self.application_data['sms_usage']['used'] = self.application_data['sms_usage']['total'] * (float(sms_usage.group('usedsms')) / 100)

      # Mock data
      if ChoozzeScraper.MOCK:
        self.application_data['sms_usage']['used'] =  random.randint(1, self.application_data['sms_usage']['total'])

      self.application_data['sms_usage']['free'] = self.application_data['sms_usage']['total'] - self.application_data['sms_usage']['used']

    call_usage = self.regex_call_usage.search(html)
    if call_usage:
      self.application_data['call_usage']['total'] = float(call_usage.group('totalcall'))
      self.application_data['call_usage']['used'] = self.application_data['call_usage']['total'] * (float(call_usage.group('usedcall')) / 100)

      # Mock data
      if ChoozzeScraper.MOCK:
        self.application_data['call_usage']['used'] =  random.randint(1, self.application_data['sms_usage']['total'])

      self.application_data['call_usage']['free'] = self.application_data['call_usage']['total'] - self.application_data['call_usage']['used']

    data_usage = self.regex_data_usage.search(html)
    if data_usage:
      self.application_data['data_usage']['total'] = float(data_usage.group('totaldata')) * self.__data_unit_factor(data_usage.group('dataunit'))
      self.application_data['data_usage']['used'] = self.application_data['data_usage']['total'] * (float(data_usage.group('useddata')) / 100)

      # Mock data
      if ChoozzeScraper.MOCK:
        self.application_data['data_usage']['used'] =  (random.randint(1, 100) / 100) * self.application_data['data_usage']['total']

      self.application_data['data_usage']['free'] = self.application_data['data_usage']['total'] - self.application_data['data_usage']['used']

    now = date.today()
    self.application_data['days_usage']['total'] = (date(now.year, now.month+1, 1) - date(now.year, now.month, 1)).days
    self.application_data['days_usage']['used']  = now.day
    self.application_data['days_usage']['free']  = self.application_data['days_usage']['total'] - self.application_data['days_usage']['used']

    self.application_data['last_update'] = int(time.time())
    self.__save_application_data()

  def __update_data(self):
    return_value = 0
    account_return = self.__update_account_data()
    return self.__update_account_data()
      #or self.__update_voicemail_data()

  def __update_account_data(self,force_update = False):
    return self.__get_account_data(force_update)

  def __get_account_data(self,force_update = False):
    if self.isLoggedIn():
      if not force_update and int(time.time()) - self.application_data['last_update'] < ChoozzeScraper.data_update_timeout:
        return 0
      try:
        html = ''
        if ChoozzeScraper.MOCK:
          html = ChoozzeScraper.MOCK_data
        else:
          response = self.opener.open(self.portal_url)
          html = response.read().decode('utf-8')

        if ChoozzeScraper.DEBUG:
          print('Got account data')
          print(html)
        self.__parse_account_data(html)
        return 1
      except:
        return -1

    return -99

  def __update_voicemail_data(self):
    return self.__get_voicemail_data()

  def __get_voicemail_data(self):
    if self.isLoggedIn():
      try:
        #response = self.opener.open(self.portal_url + '' + self.voicemaile_age)
        #self.__parse_voicemail_data(response.read().decode('utf-8'))
        return True
      except:
        pass

    return False

  def __data_unit_factor(self,unit):
    if 'MB' == unit:
      return math.pow(self.internetdata_unit,2)
    elif 'GB' == unit:
      return math.pow(self.internetdata_unit,3)

    return float(1)

  def set_credentials(self,username,password):
    self.set_username(username)
    self.set_password(password)
    return self.login()

  def set_username(self,username):
    if username is not None and username != '' and self.valid_email_regex.match(username):
      self.application_data['username'] = username
      self.__save_application_data()

  def get_username(self):
    return self.application_data['username']

  def set_password(self,password):
    if password is not None and password != '':
      self.application_data['password'] = password
      self.__save_application_data()

  def get_password(self):
    return self.application_data['password']

  def login(self):
    if ChoozzeScraper.DEBUG:
      print('Start login')
    self.login_ok = False

    if self.application_data['username'] is None or self.application_data['password'] is None:
      if ChoozzeScraper.DEBUG:
        print('Login methode missing credentials')
      return False

    login_data = {'action': 'login',
                  'login-username': self.application_data['username'],
                  'password': self.application_data['password'] }

    data = urllib.parse.urlencode(login_data).encode('utf-8')
    self.login_cookie = http.cookiejar.CookieJar()

    self.opener = urllib.request.build_opener(
        urllib.request.HTTPRedirectHandler(),
        urllib.request.HTTPSHandler(debuglevel=0),
        urllib.request.HTTPCookieProcessor(self.login_cookie))

    urllib.request.install_opener(self.opener)
    if ChoozzeScraper.DEBUG:
      print('Start login methode retreiving HTML')
    html = ''
    try:
      if ChoozzeScraper.MOCK:
        html = ChoozzeScraper.MOCK_data
      else:
        response = self.opener.open(self.portal_url + '/' + self.login_page, data)
        html = response.read().decode('utf-8')

      if ChoozzeScraper.DEBUG:
        print('Got HTML:')
        print(html)

    except:
      if ChoozzeScraper.DEBUG:
        print('Start login methode something went wrong')
      return False

    self.login_ok = self.regex_logged_in.search(html) is not None
    if self.login_ok:
      if ChoozzeScraper.DEBUG:
        print('Start login methode login success')
      self.__parse_account_data(html)

    return self.isLoggedIn()

  def isLoggedIn(self):
    return True == self.login_ok

  def get_account_status(self,force_update = False):
    if force_update:
      self.__update_account_data(force_update)

    return self.application_data

  def get_voicemail_status(self):
    pass

  def set_voicemail_status(self):
    pass

choozzescraper = ChoozzeScraper()
