#!/usr/bin/python
# -*- coding:utf-8 -*-
#----------------------------------------------------
# File: example.py
# Description: display status on e-Paper display
#----------------------------------------------------
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/star-wars-icons')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from os import listdir

from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    pic_list = os.listdir(picdir)
    print(pic_list)
    logging.info("epd2in13_V2 Demo")

    epd = epd2in13_V2.EPD()
#    logging.info("init and Clear")
#    epd.init(epd.FULL_UPDATE)
#    epd.Clear(0xFF)

    font15 = ImageFont.truetype(os.path.join(picdir, '../Font.ttc'), 15)

    #logging.info("0. quick test")
    #image = Image.open(os.path.join(picdir, 'bb8.bmp'))
    #epd.display(epd.getbuffer(image))
    #time.sleep(5)

# # partial update
    logging.info("1. show star wars...")
    sw_image = Image.new('1', (epd.height, epd.width), 255)
    sw_draw = ImageDraw.Draw(sw_image)
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(sw_image))

    epd.init(epd.PART_UPDATE)
    for file_ in pic_list:
        bmp = Image.open(os.path.join(picdir,file_))
        sw_draw.rectangle((2,2,220,100), fill=255)
        sw_draw.text((2,2), file_, font=font15, fill=0)
        sw_image.paste(bmp, (20,20))
        epd.displayPartial(epd.getbuffer(sw_image))
        time.sleep(8)

    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()