#!/usr/bin/python
#----------------------------------------------------
# File: example.py
# Description: display status on e-Paper display
#----------------------------------------------------

import sys
import os

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd2in13_V2


import requests
import json
import logging
from os import listdir
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library 

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'star-wars-icons')
iconsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons')
icons = os.listdir(iconsdir)
URL = 'http://localhost:3000'

with open('data.json', 'r') as datafile:
    data = json.load(datafile)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pul
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pul
logging.basicConfig(level=logging.DEBUG)
font15 = ImageFont.truetype(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts/Font.ttc'), 15)
fontStarWars = ImageFont.truetype(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts/Starjhol.ttf'),30, encoding="unic")
pic_id = -1
icon_id = 0
epd = False

def displayStartup(epd):
    count = 0
    serverReady = False
    while not serverReady:
        r = False
	try:
            r = requests.get(URL, timeout=0.5)
        except requests.exceptions.Timeout as e:
            r = False 
        serverReady = True if r  else False
        sw_image = Image.new('1', (epd.height, epd.width), 255)
        sw_draw = ImageDraw.Draw(sw_image)
        sw_draw.rectangle((0,0,250,122), fill=255)
        sw_draw.text((25,30), "Droid Pod", font=fontStarWars, fill=0)
        loadstr = count * "."
        sw_draw.text((115,65), loadstr, font=font15, fill=0)
        epd.displayPartial(epd.getbuffer(sw_image))
        count =count +1
        count = count%4        
        logging.info(loadstr)

def button_callback(channel):
        global pic_id
        global icon_id
        if channel == 20 or channel == 0:
        	pic_id = (pic_id+1) if (pic_id+1) < len(data) else 0 
        	icon_id = (icon_id+1) if (icon_id+1) < len(icons) else 0
        elif channel == 15:
                pic_id = (pic_id-1) if (pic_id-1) > -1 else  (len(data)-1)

        file_ = data[pic_id]
        bmp = Image.open(os.path.join(picdir,file_['primaryIcon']))
        sw_draw.rectangle((0,0,250,120), fill=255)
        sw_draw.text((2,2), file_['label'], font=font15, fill=0)
        sw_image.paste(bmp, (93,28))    #x,y (max x = 250, maxy = 120) : x_center = 250/2 - x_image/2

        icon = Image.open(os.path.join(iconsdir, icons[icon_id]))
        sw_image.paste(icon, (250-18, 4))

        epd.displayPartial(epd.getbuffer(sw_image))

try:
    epd = epd2in13_V2.EPD()
    sw_image = Image.new('1', (epd.height, epd.width), 255)
    sw_draw = ImageDraw.Draw(sw_image)
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(sw_image))
    epd.init(epd.PART_UPDATE)

    displayStartup(epd)
    button_callback(0)

    
    GPIO.add_event_detect(15,GPIO.RISING,callback=button_callback,bouncetime=1100) # Setup event on pin 10 rising edg
    GPIO.add_event_detect(20,GPIO.RISING,callback=button_callback,bouncetime=1100) # Setup event on pin 10 rising edg
    message = input("Press enter to quit\n\n") # Run until someone presses enter                                                                                    

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd2in13_V2.epdconfig.module_exit()
    exit()
