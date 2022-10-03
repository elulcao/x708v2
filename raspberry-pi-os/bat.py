#!/usr/bin/env python

import struct
import smbus
import sys
import time
import RPi.GPIO as GPIO
import logging
import logging.handlers as handlers


logger = logging.getLogger("bat")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logHandler = handlers.RotatingFileHandler(
    "/home/pi/x708v2/raspberry-pi-os/x708.log",
    mode="a",
    maxBytes=1000000,
    backupCount=1,
    encoding="utf-8",
    delay=0,
)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setwarnings(False)
bus = smbus.SMBus(1)


def readVoltage(bus):
    address = 0x36
    read = bus.read_word_data(address, 2)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25 / 1000 / 16

    return voltage


def readCapacity(bus):
    address = 0x36
    read = bus.read_word_data(address, 4)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped / 256

    if capacity >= 100:
        capacity = 100

    return capacity


try:
    while True:
        cap = readCapacity(bus)
        vol = readVoltage(bus)

        # Only trace if capacity is less than 20%
        if cap <= 20:
            logger.info("Battery capacity: %5i%%", cap)

        # Set battery low voltage to shut down, You can modify this voltage threshold (the voltage threshold range must be 2.5~4.1vdc)
        if vol <= 3.0 or cap <= 10:
            logger.info("Battery low: %5.1fV, shutdown in 5 seconds", vol)

            time.sleep(5)
            GPIO.output(13, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(13, GPIO.LOW)

        time.sleep(5)
except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()  # resets all GPIO ports used by this program
