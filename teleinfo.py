#!/usr/bin/python3

import serial
import time
import sys

baudrate = 9600

ser = serial.Serial('/dev/ttyAMA0', baudrate, bytesize=7, timeout=1)
ser.isOpen()
count=0
looping = 1
results_table=""
debug = False

item = "debug"
if item in sys.argv:
    debug = True
    sys.argv.remove(item)

try:
  print("...demarrage du mode standard a "+str(baudrate)+"... ")
  while looping:
    response = ser.readline().decode("utf-8")
    localtime = time.asctime( time.localtime(time.time()) )
    if debug:  print("count " + str(count) + " empty_count " + str(empty_count) + " | ", end='')
    count = count + 1
    if count >= 100:
      looping = 0
    if response != "":
      count = count - 1
      # The line is not empty, let's go on... 
      items = response.split()
      items = items[:-1]
      splitLen = len(items)
      if splitLen >= 2:
        # There are 3 items in the line, as expected, let's go on...
        if debug:  print(str(splitLen) + " items : " + str(items))
        item  = items[0]
        value = items[splitLen-2]
        if item in sys.argv or "all" in sys.argv:
          if value.isdigit():
            # Remove leading zeros from numerical values
            value_int = int(value)
            value = str(value_int)
          if not "all" in sys.argv:
            print(" " + item + " " + value)
          filename = "/home/pi/teleinfo/" + str(item)
          file_object = open(filename, 'w')
          result = localtime + "     " + item + "     " + value
          file_object.write(result)
          file_object.close( )
          if "all" not in sys.argv:
            if "loop" not in sys.argv:
              sys.argv.remove(item)
          if len(sys.argv) == 1:
            break;

except KeyboardInterrupt:
  ser.close()


