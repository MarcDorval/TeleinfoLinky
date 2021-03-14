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
broker="127.0.01"
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
        
mqttc.connect_to(broker, port, publisher=True)
mqttc.log.info(f"time/{client_id}/start/loop")

if nb_sensors == 0:
    mqttc.publish(topic=f"time/{client_id}/end/loop", msg="No sensor, leaving")
    mqttc.publish(topic=f"time/{client_id}/end/loop", msg=ymdhms)
    mqttc.log.info(f"time/{client_id}/end/loop")
    mqttc.disconnect()
    exit()
else:
    mqttc.publish(topic=f"time/{client_id}/start/loop", msg=ymdhms)

try:
  while True:
    for id in sensors:
        if "28-" in id:
            ds18b20_file = open(f"/sys/bus/w1/devices/{id}/{item}", "r")
            file_content = ds18b20_file.read()
            ds18b20_file.close()
            for line in file_content.split("\n"):
                if len(line) > 0:
                    value = line
                    if item == "temperature":
                        # Temperature values are in 1/1000 °C
                        value_int = int(value)
                        value = str(value_int/1000)
                    if value != item_values[id]:
                        print(f"topic=ds28b20/{id}/{item} msg={value}")
                        mqttc.publish(topic=f"ds28b20/{id}/{item}", msg=value, retain=True)
                        item_values[id] = value
    time.sleep(5)
except KeyboardInterrupt:
  ser.close()
