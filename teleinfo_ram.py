#!/usr/bin/python
#  use case: python teleinfo_ram.py  IRMS1 IRMS2 IRMS3 URMS1 URMS2 URMS3 loop

import serial
import time
import sys

baudrate=9600
ser = serial.Serial('/dev/ttyAMA0', baudrate, bytesize=7, timeout=1)
ser.isOpen()

count=0
looping = 1
teleinfo_items=[]
results_items=[]
results_dict={}
return_string=""
results_folder="/var/tmp_ram/"

sys.argv.remove(sys.argv[0])
expected_items = len(sys.argv)

for item in sys.argv:
#  print "item " + item
  item_split = item.split()
#  print item_split
  for sub_item in item_split:
#    print "  sub_item " + sub_item
    teleinfo_items.append(sub_item)
    results_items.append(sub_item)
#  print "teleinfo_items:"
#  print teleinfo_items

try:
  while looping:
    response = ser.readline()
    localtime = time.asctime( time.localtime(time.time()) )
    count = count + 1
    # print count
    # If one of the arguments is not found, we must exit after a while
    if count >= 100:
      print " At least 1 or more argument missing after " + str(count) + " lines : exiting!\n Remaining (probably mis-spelled or unknown) arguments:"
      for a in teleinfo_items:
        print " ~ " + a
      looping = 0
      break;
    if response != "":
      # print "# The line is not empty, let's go on..." 
      items = response.split()
      splitLen = len(items)
      if splitLen >= 2:
        # There are at leaast 3 items in the line, as expected, let's go on...
        #   The name  is the first item
        #   The value is the one-before-last item (in most cases). This is the only case we handle.
        item  = items[0]
        value = items[splitLen-2]
        if item in teleinfo_items:
          # print item + " == " + str(value)
          if value.isdigit():
            # Remove leading zeros from numerical values
            value_int = int(value)
            value = str(value_int)
          results_dict[item]=value
          filename = results_folder+item
          file_object = open(filename, 'w')
          file_object.write(results_dict[item])
          file_object.close( )
          # Once an argument is retrieved, it's removed from the list
          teleinfo_items.remove(item)
          # Once the list is empty, fill the return string and exit
          if len(teleinfo_items) == 0:
            for item in results_items:
              return_string = return_string + results_dict[item] + " "
            print return_string
            sys.exit(0)
            break;
except KeyboardInterrupt:
  ser.close()



