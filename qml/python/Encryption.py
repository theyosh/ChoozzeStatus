#!/usr/bin/env python
# -*- coding: utf-8 -*-

ENCRYPTION_IMPORT = False
try:
  import Crypto.Random
  from Crypto.Cipher import AES
  ENCRYPTION_IMPORT = True
except:
  pass

if ENCRYPTION_IMPORT:
  import subprocess
  import hashlib
  import re

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
    if ENCRYPTION_IMPORT:
      self.__get_secret_key()

  def __get_secret_key(self):
    network_data = ''
    regex_hardwareaddress = re.compile('(?P<addr>([0-9a-f]{1,2}[\.:-]){5}([0-9a-f]{1,2}))',re.IGNORECASE)
    try:
      network_data = subprocess.check_output(['/sbin/ifconfig','wlan0'],universal_newlines=True)
    except CalledProcessError as error:
      pass

    key = regex_hardwareaddress.search(network_data)
    if key is not None:
      # Key needs to be in bytes
      self.__uniqe_key = str(key.group('addr')).encode()
      return True

    return False

  def isEnabled(self):
    return self.__uniqe_key is not None

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
