#!/usr/bin/env python

import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setwarnings(False)


GPIO.output(5, GPIO.HIGH)
time.sleep(10)
GPIO.output(5, GPIO.LOW)
time.sleep(10)
GPIO.output(5, GPIO.HIGH)

GPIO.cleanup()
