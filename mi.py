#!/usr/bin/python

import socket
import time
import colorsys
import math
import milight

controller = milight.MiLight({'host': '192.168.178.32', 'port': 8899}, wait_duration=0) #Create a controller with 0 wait between commands
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
    return round(1 / 360 * h, 10), round(s, 10), round(v, 10)

#UDP SERVER
port = 19446
last = ""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print("waiting on port:", port)

light = milight.LightBulb(['rgbw']) #Can specify which types of bulbs to use
controller.send(light.on(1)) # Turn on group 1 lights
status = "on";

try:
    while True:
        d = s.recvfrom(3)
        new = bytearray(d[0])

        # print (colorsys.rgb_to_hls(new[0]/255, new[1]/255, new[2]/255))
        if new != last:
            hls = colorsys.rgb_to_hls(new[0]/255, new[1]/255, new[2]/255);
            bri = round(100 / 255 * ((new[0]*299) + (new[1]*587) + (new[0]*114)) / 1000)
            if bri == 0: 
                controller.send(light.color(milight.color_from_rgb(0,0,0), 1))
            elif hls[0] == 0 and hls[2] == 0:
                controller.send(light.color(milight.color_from_rgb(255,255,255), 1))
                controller.send(light.brightness(bri, 1))
            else:
                controller.send(light.color(milight.color_from_hls(*hls), 1))
                controller.send(light.brightness(bri, 1))

            print (bri)
            
        last = new
except KeyboardInterrupt:
    print("Exit ...")

