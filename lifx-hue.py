#!/usr/bin/env python
# coding=utf-8
import sys
import socket
import time
import colorsys
import math
from lifxlan import LifxLAN
from time import sleep

port = 19446

def RGBtoHSBK (RGB, Temperature = 2500):
    cmax = max(RGB)
    cmin = min(RGB)
    cdel = cmax - cmin
    
    Brightness = int((cmax/255) * 65535)

    if cdel != 0:
        Saturation = int(((cdel) / cmax) * 65535)

        redc = (cmax - RGB[0]) / (cdel)
        greenc = (cmax - RGB[1]) / (cdel)
        bluec = (cmax - RGB[2]) / (cdel)
        
        if RGB[0] == cmax:
            Hue = bluec - greenc
        else:
            if RGB[1] == cmax:
                Hue = 2 + redc - bluec    
            else:
                Hue = 4 + greenc - redc
                
        Hue = Hue / 6
        if Hue < 0:
            Hue = Hue + 1 
            
        Hue = int(Hue*65535)        
    else:
        Saturation = 0
        Hue = 0
    
    #return (Hue, Saturation, int(Brightness), Temperature) # Dynamic brighness
    return (Hue, Saturation, int(65535/8), Temperature) # Fixed brightness

print ("Initizalizing lights");
lifx = LifxLAN(2)
#lights = lifx.get_color_lights()
#print (lights)
g = lifx.get_devices_by_group("Eettafel") # get lights in group 
#print (g)

last = ""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print("waiting on port:", port)


try:
	while True:
		d = s.recvfrom(3)
		new = bytearray(d[0])
		hsbk = RGBtoHSBK(new)    

		if new != last:
			#for light in lights:
			g.set_color(hsbk, 200, True)

		last = new
except KeyboardInterrupt:
	print("Exit ...")


#print (RGBtoHSBK([255,0,0]))
#for light in lights:
#	light.set_color(RGBtoHSBK([0,0,0]));
#	print (light.get_color());
#
#print (lights)
