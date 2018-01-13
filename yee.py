#!/usr/bin/python

import socket
import time
import colorsys
import math
from yeelight import *

ip_address = "192.168.178.131"
timeout = 500

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return round(h), round(s * 100, 1), round(v * 100, 1)

#UDP SERVER
port = 19446
last = ""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print("waiting on port:", port)

#YEELIGHT
bulb = Bulb(ip_address, effect="smooth", duration=timeout)
bulb.turn_on()
status = "on";
# bulb.effect = "smooth"

#Stop/Start music mode, bypasses lamp rate limits, ensures that previous sockets close before starting
while True:
    try:
        bulb.stop_music()
        break
    except BulbException:
        break
time.sleep(1)
while True:
    try:
        bulb.start_music()
        break
    except BulbException:
        break
time.sleep(1)

try:
    while True:
        d = s.recvfrom(3)
        new = bytearray(d[0])
        hsv = rgb2hsv(new[0], new[1], new[2])    

        if new != last:
            if hsv[2] == 0.0:
                if status == "on":
                    bulb.turn_off()
                    status = "off"
            elif status == "off":
                bulb = Bulb(ip_address, effect="smooth", duration=timeout)
                while True:
                    try:
                        bulb.start_music()
                        break
                    except BulbException:
                        break

                bulb.turn_on()
                status = "on"

            if status == "on":
                bulb.set_hsv(*hsv)

        last = new
except KeyboardInterrupt:
    print("Exit ...")