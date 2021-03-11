#!/usr/bin/python
#  use case: python teleinfo_nas.py  IRMS1 IRMS2 IRMS3 URMS1 URMS2 URMS3 loop

import random
import serial
import time
import sys

from paho.mqtt import client as mqtt_client

baudrate=9600
ser = serial.Serial('/dev/ttyAMA0', baudrate, bytesize=7, timeout=1)
ser.isOpen()

count=0
looping = 1
results_items=[]
results_dict={}
return_string=""
results_folder="/var/tmp_ram/"

sys.argv.remove(sys.argv[0])
expected_items = len(sys.argv)

mqtt_client_id = "python-mqtt"
mqtt_broker = 'PiCuisine'
mqtt_port = 1883


def connect_mqtt():
	def on_connect(mqtt_client_id, userdata, flags, rc):
		if rc == 0:
			print("Connected to MQTT Broker!")
		else:
			print("Failed to connect, return code %d\n", rc)

	client = mqtt_client.Client(mqtt_client_id)
	# client.username_pw_set(username, password)
	client.on_connect = on_connect
	client.connect(mqtt_broker, mqtt_port)
	return client


def mqtt_publish(mqtt_client, topic, msg):
	msg_count = 0
	#msg = f"messages: {msg_count}"
	result = mqtt_client.publish(topic, msg)
	# result: [0, 1]
	status = result[0]
	if status == 0:
		print("Send " + msg + " to topic " + topic)
	else:
		print("Failed to send message to topic {topic}")
	msg_count += 1


mqtt_client = connect_mqtt()
mqtt_client.loop_start()

for item in sys.argv:
#  print item
  results_items.append(item)

try:
  while looping:
    response = ser.readline()
    localtime = time.asctime( time.localtime(time.time()) )
    count = count + 1
    # print count
    # If one of the arguments is not found, we must exit after a while
    if count >= 100:
      print " At least 1 or more argument missing after " + str(count) + " lines : exiting!\n Remaining (probably mis-spelled or unknown) arguments:"
      for a in sys.argv:
        print "   " + a
      looping = 0
      break;
    if response != "":
      # print "# The line is not empty, let's go on..." 
      items = response.split()
      splitLen = len(items)
      if splitLen >= 2:
        # There are at least 3 items in the line, as expected, let's go on...
        #   The name  is the first item
        #   The value is the one-before-last item (in most cases). This is the only case we handle.
        item  = items[0]
        value = items[splitLen-2]
        #print item + " " + str(value)
        print item + str(sys.argv)
        if item in str(sys.argv):
          if value.isdigit():
            # Remove leading zeros from numerical values
            value_int = int(value)
            value = str(value_int)
          print item + " " + str(value)
          results_dict[item]=value
          filename = results_folder+item
          mqtt_publish(mqtt_client, item, results_dict[item])
          file_object = open(filename, 'w')
          file_object.write(results_dict[item])
          file_object.close( )
          # Once an argument is retrieved, it's removed from the list
          sys.argv.remove(item)
          # Once the list is empty, fill the return string and exit
          if len(sys.argv) == 0:
            for item in results_items:
              return_string = return_string + results_dict[item] + " "
            sys.exit(return_string)
            break;
except KeyboardInterrupt:
  ser.close()



