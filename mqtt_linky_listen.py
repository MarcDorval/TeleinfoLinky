#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   Test du broker mqtt pour teleinformation linky
   la fonction 'on_message' sera appelée à chaque mise à jour d'un des topics listés 
#  use case: python3 mqtt_linky_listen.py
"""

import random
import time
import sys

from mymqtt import myMqtt
from paho.mqtt import client as mqtt_client

broker="PiCuisine"

mqttc = myMqtt("mowgli")
mqttc.connect_to(broker)

mqttc.subscribe([("linky/URMS1", 1), ("linky/IRMS1", 1)])
mqttc.listen()
