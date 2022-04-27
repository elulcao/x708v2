#!/usr/bin/env python
import struct
import smbus
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setwarnings(False)

def readVoltage(bus):

     address = 0x36
     read = bus.read_word_data(address, 2)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     voltage = swapped * 1.25 /1000/16
     return voltage


def readCapacity(bus):

     address = 0x36
     read = bus.read_word_data(address, 4)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     capacity = swapped/256
     if capacity > 100:
        capacity = 100
     return capacity


bus = smbus.SMBus(1)

while True:

 print ("******************")
 print ("Voltage:%5.2fV" % readVoltage(bus))

 print ("Battery:%5i%%" % readCapacity(bus))

 if readCapacity(bus) >= 100:
         print ("Battery FULL")

 if readCapacity(bus) < 20:
         print ("Battery Low")

#Set battery low voltage to shut down, You can modify this voltage threshold (the voltage threshold range must be 2.5~4.1vdc)
 if readVoltage(bus) < 3.00:

         print ("Battery LOW!!!")
         print ("Shutdown in 5 seconds")
         time.sleep(5)
         GPIO.output(13, GPIO.HIGH)
         time.sleep(3)
         GPIO.output(13, GPIO.LOW)

 time.sleep(2)
