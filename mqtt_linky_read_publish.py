#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   Lecture des informations de teleinformation du compteur Linky
   et envoi vers un broker mqtt
#  use case: python3 mqtt_linky_read_publish.py
"""

import random
import serial
import time
import sys

from mymqtt import myMqtt
from paho.mqtt import client as mqtt_client

linky_args = ["URMS1", "IRMS1", "URMS2", "IRMS2", "URMS3", "IRMS3"]
broker="PiCuisine"
client_id="linky2mqtt"
port = 1883
mqttc = myMqtt(client_id)
ymdhms = mqttc.yyyymmddhhmmss()

"""
Mode de teleinformation dit 'standard': 
  permettant de monitorer les 3 phases
  utilise un baudrate=9600
NB: Le mode de teleinformation dit (historique) fonctionne avec baudrate=1200 et ne permet pas
  de monitorer le triphasé
"""
baudrate=9600

ser = serial.Serial('/dev/ttyAMA0', baudrate, bytesize=7, timeout=1)
ser.isOpen()

mqttc.connect_to(broker, port)
mqttc.publish(f"time/{client_id}/start/loop", ymdhms)
mqttc.disconnect()

try:
  while True:
    # Disconnect and reconnect after receiving all items, to keep mosquitto connected
    # there is probably a better method, but so far it works
    count = 0
    mqttc.connect_to(broker, port)
    while count < 20*len(linky_args):
      response = ser.readline()
      localtime = time.asctime( time.localtime(time.time()) )
      # If one of the arguments is not found, we must exit after a while
      count = count + 1
      if response != "":
        # print "# The line is not empty, let's go on..." 
        items = response.split()
        splitLen = len(items)
        if splitLen >= 2:
          # There are at least 3 items in the line, as expected, let's go on...
          #   The name  is the first item
          #   The value is the one-before-last item (in most cases). 
          item  = items[0].decode('utf-8')
          value = items[splitLen-2]
          if str(item) in linky_args:
            if value.isdigit():
              # Remove leading zeros from numerical values
              value_int = int(value)
              value = str(value_int)
            mqttc.publish(f"linky/{item}", value)
    mqttc.disconnect()
except KeyboardInterrupt:
  ser.close()

exit()
