#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   Lecture des informations de capteurs de temperature DS18B20
   et envoi vers un broker mqtt
#  use case: python3 mqtt_ds18b20_read_temp_publish.py
"""

import time
import sys
import os

from mymqtt import myMqtt
from paho.mqtt import client as mqtt_client

client_id="ds18_mqtt"
broker="PiCuisine"
port = 1883
mqttc = myMqtt(client_id)
ymdhms = mqttc.yyyymmddhhmmss()

w1_dir = "/sys/bus/w1/devices/"
item = "temperature"
item_values={}
sensors = os.listdir(f"{w1_dir}")

nb_sensors = 0
for id in sensors:
    if "28-" in id:
        print(f"Existing ds18b20 sensor: {w1_dir}{id}")
        item_values[id]=""
        nb_sensors += 1
        
mqttc.connect_to(broker, port)
mqttc.log.info(f"time/{client_id}/start/loop")

if nb_sensors == 0:
    mqttc.publish(topic=f"time/{client_id}/end/loop", msg="No sensor, leaving")
    mqttc.publish(topic=f"time/{client_id}/end/loop", msg=ymdhms)
    mqttc.log.info(f"time/{client_id}/end/loop")
    mqttc.disconnect()
    exit()
else:
    mqttc.publish(topic=f"time/{client_id}/start/loop", msg=ymdhms)

mqttc.disconnect()

try:
  while True:
    # Disconnect and reconnect after receiving all items, to keep mosquitto connected
    # there is probably a better method, but so far it works
    mqttc.connect_to(broker, port)
    for id in sensors:
        if "28-" in id:
            ds18b20_file = open(f"/sys/bus/w1/devices/{id}/{item}", "r")
            file_content = ds18b20_file.read()
            ds18b20_file.close()
            for line in file_content.split("\n"):
                if len(line) > 0:
                    if line != item_values[id]:
                        print(f"topic=ds28b20/{id}/{item} msg={line}")
                        mqttc.publish(topic=f"ds28b20/{id}{item}", msg=line, retain=True)
                        item_values[id] = line
    mqttc.disconnect()
    time.sleep(5)
except KeyboardInterrupt:
  exit()
