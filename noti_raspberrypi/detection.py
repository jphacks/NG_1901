#!/usr/bin/python
###########################################################################
#Filename      :jphacks.py
#Description   :noti
############################################################################
import RPi.GPIO as GPIO
import time
import json
import urllib.request
import collections as cl
import sys
from flask import Flask, request

app = Flask(__name__)

# set BCM_GPIO
trigPin   = 17
echoPin   = 27
PIRPin    = 22
LEDPin_G  =  5
LEDPin_Y  =  6
LEDPin_R  = 13

detection = 200.0

count     = 0
check_LED = 0
count_sensor = 0
distance_total = 0

with open('./config.json') as data:
    config = json.load(data)

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    GPIO.setup(trigPin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(echoPin,GPIO.IN)
    GPIO.setup(PIRPin,GPIO.IN)
    GPIO.setup(LEDPin_G,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDPin_Y,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDPin_R,GPIO.OUT,initial=GPIO.LOW)

#measurment function
def measure():
    GPIO.output(trigPin,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigPin,GPIO.LOW)
    
    while GPIO.input(echoPin) == 0:
        signal_off = time.time()
        
    while GPIO.input(echoPin) == 1:
        signal_on = time.time()
        
    timepassed = signal_on - signal_off
    distance = timepassed * 17000
    return distance

# def main():
#     count = 0
#     while True:
#         #measur distance
#         distance = measure()
        
#         print('distance = ',distance)
        
#         #check presence sensor
#         check_PIR = GPIO.input(PIRPin)
        
#         #detect distance
#         if distance < df['detection']:
            
#             #count and turn on LED
#             if check_PIR == 1 and count != 1:
#                 print ('********************')
#                 print ('*     alarm!       *')
#                 print ('********************')
#                 print ('\n')
                
#                 # noti_count = {'count': 1}
#                 # url = df['url'] + 'count' + '?' + urllib.parse.urlencode(noti_count)
#                 # with urllib.request.urlopen(url) as data:
#                 #     print('ok')
#                 url = df['url'] + 'count'
#                 urllib.request.urlopen(url)
                
#                 GPIO.output(LEDPin_G,GPIO.HIGH)
#                 count = 1
                
#         else:
#             count = 0
                
# #            if check_PIR != 1:
#             GPIO.output(LEDPin_G,GPIO.LOW)
                    
#         time.sleep(0.5)

@app.route("/setting", methods=['GET'])
def setting():
    count = 0
    global count_sensor
    global distance_total 
    while True:
        #measur distance
        distance = measure()
        
        print('distance = ',distance)
        
        #check presence sensor
        check_PIR = GPIO.input(PIRPin)
        
        #detect distance
        if distance < detection:
            #3回反応したら，そこから閾値設定計算
            count_sensor = count_sensor + 1
            distance_total = distance_total + distance
            # setting()
            if count_sensor > 2:
                distance_total = distance_total / 3 * 1.25
                #閾値が決まったら，config.json書き換え
                json_config = cl.OrderedDict()
                json_config['url'] = config['url']
                json_config['detection'] = distance_total
                config_new = open('config.json','w')
                json.dump(json_config,config_new,indent=4)
                #Herokuへの閾値設定完了通知
                url = config['url'] + 'distance'
                urllib.request.urlopen(url)
                ####登録完了したら，終了
                print("fin")
                count_sensor = 0
                distance_total = 0
                sys.exit()
                return "ok"
            else:
                setting()
            #count and turn on LED
            if check_PIR == 1 and count != 1:
                # GPIO.output(LEDPin_G,GPIO.HIGH)
                count = 1
        else:
            count = 0
                
#            if check_PIR != 1:
            GPIO.output(LEDPin_G,GPIO.LOW)
                    
        time.sleep(0.5)
                
       
#define a destroy function for clean up everything after the script finished
def destroy():
    #release resource
    GPIO.cleanup()

#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    app.run(debug=False, host='0.0.0.0', port=5000)