#i!/usr/bin/python
#----------------------------------------------------
# File: example.py
# Description: display status on e-Paper display
#----------------------------------------------------
import sys
import os

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import traceback
import time
from os import listdir
import logging
import json
import requests
from waveshare_epd import epd2in13_V2

logging.basicConfig(filename='pod-ui.log', filemode='w',level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

picdir = os.path.join(os.path.dirname(os.path.dirname( os.path.realpath(__file__))), 'star-wars-icons')
iconsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons')
icons = os.listdir(iconsdir)
URL = 'http://localhost:3000'

with open('data.json', 'r') as datafile:
    data = json.load(datafile)

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)
# Set pin 10 to be an input pin and set initial value to be pul
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Set pin 10 to be an input pin and set initial value to be pul
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#logging.basicConfig(level=logging.DEBUG)
font15 = ImageFont.truetype(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'fonts/Font.ttc'), 15)
fontStarWars = ImageFont.truetype(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'fonts/Starjhol.ttf'), 30, encoding="unic")
selected_device = -1
icon_id = 0
epd = False


def displayStartup(epd):
    count = 0
    serverReady = False
    while not serverReady:
        r = False
        try:
            r = requests.get(URL, timeout=0.5)
	except requests.exceptions.RequestException as e:
            r = False

        serverReady = True if r else False
        sw_image = Image.new('1', (epd.height, epd.width), 255)
        sw_draw = ImageDraw.Draw(sw_image)
        sw_draw.rectangle((0, 0, 122, 250), fill=255)
        sw_draw.text((25, 30), "Droid Pod", font=fontStarWars, fill=0)
        loadstr = count * "."
        sw_draw.text((115, 65), loadstr, font=font15, fill=0)
        epd.displayPartial(epd.getbuffer(sw_image))
        count = count + 1
        count = count % 4
        logging.info(loadstr)


def broadcastSelectedDevice(deviceToBroadcast):
    dataToBroadcast = deviceToBroadcast['data']
    response = False
    try:
        response = requests.get(URL+'/start/EIRAdvertisement/'+dataToBroadcast, timeout=0.5)
    except requests.exceptions.RequestException as e:
        response = False
    
    if response:
        bleStatus = response.json()
        if bleStatus['status'] == "success" and (bleStatus['data'])['advertising']:
            drawSelectedDeviceStatus(deviceToBroadcast, True)
        else:
            logging.info('unable to broadcast' + dataToBroadcast)



def drawSelectedDeviceStatus(deviceToBroadcast, isAdvertising):
        bmp = Image.open(os.path.join(
            picdir, deviceToBroadcast['primaryIcon']))
        sw_draw.rectangle((0, 0, 120, 250), fill=255)
        sw_draw.text((2, 2), deviceToBroadcast['label'], font=font15, fill=0)
        # x,y (max x = 250, maxy = 120) : x_center = 250/2 - x_image/2
        sw_image.paste(bmp, (93, 28))
        icon = Image.open(os.path.join(
            iconsdir, icons[0 if isAdvertising else 1]))
        sw_image.paste(icon, (250-18, 4))
        epd.displayPartial(epd.getbuffer(sw_image))


def button_callback(channel):
	time.sleep(.20)
        global selected_device
        global icon_id
        if channel == 20 or channel == 0:
        	selected_device = (
        	    selected_device+1) if (selected_device+1) < len(data) else 0
        	icon_id = (icon_id+1) if (icon_id+1) < len(icons) else 0
        elif channel == 15:
            selected_device = (
                selected_device-1) if (selected_device-1) > -1 else (len(data)-1)

        deviceToBroadcast = data[selected_device]
        drawSelectedDeviceStatus(deviceToBroadcast, False)
        broadcastSelectedDevice(deviceToBroadcast)


try:
    epd = epd2in13_V2.EPD()
    sw_image = Image.new('1', (epd.height, epd.width), 255)
    sw_draw = ImageDraw.Draw(sw_image)
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(sw_image))
    epd.init(epd.PART_UPDATE)

    displayStartup(epd)
    button_callback(0)

    # Setup event on pin 15 rising edg
    GPIO.add_event_detect(15, GPIO.RISING, callback=button_callback, bouncetime=200)
    
    # Setup event on pin 20 rising edg
    GPIO.add_event_detect(20, GPIO.RISING, callback=button_callback, bouncetime=200)
    
    # Run until someone presses enter
    sys.stdin = open('/dev/tty')
    print "Press ctrl + c to quit."
    while True:
        m = raw_input()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd2in13_V2.epdconfig.module_exit()
    exit()
