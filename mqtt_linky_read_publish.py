#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   Lecture des informations de teleinformation du compteur Linky
   et envoi vers un broker mqtt
#  use case: python3 mqtt_linky_read_publish.py
"""

import serial
import time
import sys
import logging

from mymqtt import myMqtt
from paho.mqtt import client as mqtt_client

client_id="linky2mqtt"
linky_args = ["URMS1", "IRMS1", "URMS2", "IRMS2", "URMS3", "IRMS3"]
broker="127.0.0.1"
port = 1883
mqttc = myMqtt(client_id)
ymdhms = mqttc.yyyymmddhhmmss()
item_values={}
"""
Mode de teleinformation dit 'standard': 
  permettant de monitorer les 3 phases
  utilise un baudrate=9600
NB: Le mode de teleinformation dit (historique) fonctionne avec baudrate=1200 et ne permet pas
  de monitorer le triphasé
"""
baudrate=9600

debug = False
trace = False
ser = serial.Serial('/dev/ttyAMA0', baudrate, bytesize=7, timeout=1)
ser.isOpen()

item = "trace"
if item in sys.argv:
    trace = True
    sys.argv.remove(item)

item = "debug"
if item in sys.argv:
    debug = True
    trace = True
    sys.argv.remove(item)

mqttc.connect_to(broker, port, keepalive=30, publisher=True)
mqttc.log.info(f"time/{client_id}/start/loop")
mqttc.publish(topic=f"time/{client_id}/start/loop", msg=ymdhms)

for item in linky_args:
  item_values[item]=""

while True:
  try:
    response = ser.readline().decode("utf-8")
    if response != "":
      items = response.split()
      items = items[:-1]
      # print "# The line is not empty, let's go on..." 
      splitLen = len(items)
      if splitLen >= 2:
        # There are at least 3 items in the line, as expected, let's go on...
        #   The name  is the first item
        #   The value is the one-before-last item (in most cases). 
        item  = items[0]
        value = items[splitLen-1]
        if item in linky_args:
          # Remove leading zeros from numerical values
          value_int = int(value)
          value = str(value_int)
          if value != item_values[item]:
            item_values[item] = value
            if trace: print(f"{item:8} {str(value)}")
            mqttc.publish(topic=f"linky/item/{item}", msg=str(value), retain=False)
          else:
            if debug: print(" unchanged  " + item + " " + str(value))
  except serial.serialutil.SerialException as e:
    if "device " in str(e):
      if debug: print("passing over " + str(e) +" exception")
      pass
    else:
      if debug: print(f"serial.serialutil.SerialException {e}")
      #mqttc.log.error(f"serial.serialutil.SerialException {e}")
      #mqttc.publish(topic=f"linky/exception", msg=str(e), retain=True)
      #time.sleep(1)
      #ser = serial.Serial('/dev/ttyAMA0', baudrate, bytesize=7, timeout=1)
      #ser.isOpen()
      pass
      #ser.close()
      #exit()
  except ValueError:
    pass
  except KeyboardInterrupt:
    ser.close()
    sys.exit(0)
