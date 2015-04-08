#!/usr/bin/python

# remember to change the GPIO values below to match your sensors
# GPIO output = the pin that's connected to "Trig" on the sensor
# GPIO input = the pin that's connected to "Echo" on the sensor
import time
import RPi.GPIO as GPIO
import locale

import urllib
import urllib2
response ={}
url = "POST先のURL"
headers ={
  "pragma":"no-cache",
}

GPIO.setwarnings(False)   
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.IN)
GPIO.output(17, GPIO.LOW)
time.sleep(0.3)

def await(pin, expected_value, timeout_usec):
    begin = time.time()
    while GPIO.input(pin) == expected_value:
        if (time.time() - begin) > timeout_usec:
            print time.time() - begin
            raise Exception("Timeout")
    return time.time()

def reading(sensor):
    #import time
    
    if sensor == 0:
        GPIO.output(17, True)
        time.sleep(0.00001)
        GPIO.output(17, False)
        
        signaloff = await(27, 0, 1.0)
        signalon = await(27, 1, 1.0)
        timepassed = signalon - signaloff
        distance = timepassed * 17000
        return distance

    else:
        print "Incorrect usonic() function varible."

while 1==1:
    #print time.time()
    try:
        i = []
        for var in range(0,30):
            i.append(reading(0))
            time.sleep(0.1)
            #print i
        i.sort()
        six = i[10:21]
        ave = sum(six)/10
        #print ave
        try :
            params = urllib.urlencode({'distance':ave})
            req = urllib2.Request(url, params ,headers )
            res = urllib2.urlopen(req)
            response["body"] = res.read()
            response["headers"] =  res.info().dict
        except URLError, e:
            print e
            exit()
        #print   response["body"]
    except Exception:
        print "Timeout"