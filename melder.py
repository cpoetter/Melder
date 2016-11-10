#! /usr/bin/env python

import RPi.GPIO as GPIO
import httplib, urllib
import datetime
import time
import json
import os


# This function sends out the push notification and triggers the on board LED
def trigger_alarm(): 

    # Send push
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': Melder triggered'
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.urlencode({"token": "a72ixa4uudncku5wygvnc9vio4342n", "user": "unpgpsea1vvxnk2522otkng3ffoef5", "priority": 2, "retry": 60, "expire": 120, "sound": "alien", "timestamp": int(time.time()), "title": "Emergency", "message": "DLRG Alarm.",}), { "Content-type": "application/x-www-form-urlencoded" })
    push_response = conn.getresponse()
    response = json.load(push_response)
    if response['status'] == 1:
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': Push successfully send'
    else:
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': Could not send Push notification'

    # trigger on board led
    os.system("sudo su -l root -c 'echo '1' >/sys/class/leds/led0/brightness'")
    # GRIO is true for 10 seconds after alarm
    time.sleep(12)
    os.system("sudo su -l root -c 'echo '0' >/sys/class/leds/led0/brightness'")


# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up the GPIO channels, 14 is Ground
# number 6 on the left side
GPIO.setup(11, GPIO.IN)

# set start value
os.system("sudo su -l root -c 'echo none >/sys/class/leds/led0/trigger'")
os.system("sudo su -l root -c 'echo '0' >/sys/class/leds/led0/brightness'")

print "Start Melder Observer"

while True:
    try:
        
        if GPIO.input(11) == False:
            trigger_alarm()
        
        time.sleep(0.5)

    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
