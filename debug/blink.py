#!/usr/bin/env python

# Author: Andrea Stagi <stagi.andrea@gmail.com>
# Description: keeps your led blinking
# Dependencies: None

from nanpy import (ArduinoApi, SerialManager)
from time import sleep

device = '/dev/cu.usbmodem1411'
connection = SerialManager(device=device)
connection.open()
a = ArduinoApi(connection=connection)

a.pinMode(3, a.OUTPUT)
led_status = 1
while True:
    if led_status:
        led_status = 0
    else:
        led_status = 1
    a.digitalWrite(3, led_status)
    sleep(2)
