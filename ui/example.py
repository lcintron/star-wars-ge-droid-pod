#!/usr/bin/python
# -*- coding:utf8 -*-
#----------------------------------------------------
# File: example.py
# Description: display status on e-Paper display
#----------------------------------------------------
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'star-wars-icons')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
pic_list = os.listdir(picdir)

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from os import listdir
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library 

iconsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons')
icons = os.listdir(iconsdir)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pul
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pul
#GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pul
#GPIO.add_event_detect(38,GPIO.FALLING,callback=button_callback,bouncetime=500) # Setup event on pin 10 rising edg
#logging.basicConfig(level=logging.DEBUG)

try:
    #print(pic_list)
    #logging.info("epd2in13_V2 Demo")
    epd = epd2in13_V2.EPD()
    #logging.info("init and Clear")
    #epd.init(epd.FULL_UPDATE)
    #epd.Clear(0xFF)
    font15 = ImageFont.truetype(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts/Font.ttc'), 15)

    #logging.info("0. quick test")
    #image = Image.open(os.path.join(picdir, 'bb8.bmp'))
    #epd.display(epd.getbuffer(image))
    #time.sleep(5)

    ##partial update

    #logging.info("1. show star wars...")
    sw_image = Image.new('1', (epd.height, epd.width), 255)
    sw_draw = ImageDraw.Draw(sw_image)
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(sw_image))
    epd.init(epd.PART_UPDATE)

    # for file_ in pic_list:
    #     bmp = Image.open(os.path.join(picdir,file_))
    #     sw_draw.rectangle((2,2,220,100), fill=255)
    #     sw_draw.text((2,2), file_, font=font15, fill=0)
    #     sw_image.paste(bmp, (20,20))
    #     epd.displayPartial(epd.getbuffer(sw_image))
    #     time.sleep(8)

    pic_id = 0
    icon_id = 0
    def button_callback(channel):
        global pic_id
        global icon_id
        file_ = pic_list[pic_id]
        bmp = Image.open(os.path.join(picdir,file_))
        sw_draw.rectangle((2,2,220,100), fill=255)
        filename, fileextension = os.path.splitext(file_)
        sw_draw.text((2,2), filename, font=font15, fill=0)
        sw_image.paste(bmp, (93,28))    #x,y (max x = 250, maxy = 120) : x_center = 250/2 - x_image/2

	icon = Image.open(os.path.join(iconsdir, icons[icon_id]))
        sw_image.paste(icon, (250-18, 4))

        epd.displayPartial(epd.getbuffer(sw_image))
        pic_id = (pic_id+1) if (pic_id+1) < len(pic_list) else 0 
        icon_id = (icon_id+1) if (icon_id+1) < len(icons) else 0
	
        
	print("button-"+str(pic_id))

    GPIO.add_event_detect(15,GPIO.RISING,callback=button_callback,bouncetime=1100) # Setup event on pin 10 rising edg
    GPIO.add_event_detect(20,GPIO.RISING,callback=button_callback,bouncetime=1100) # Setup event on pin 10 rising edg
    #logging.info("Clear...")
    #epd.init(epd.FULL_UPDATE)
    #epd.Clear(0xFF)
    #logging.info("Goto Sleep...")
    #epd.sleep()
    message = input("Press enter to quit\n\n") # Run until someone presses enter                                                                                    


except IOError as e:
    logging.info(e)


except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd2in13_V2.epdconfig.module_exit()
    exit()
