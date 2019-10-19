#!/usr/bin/python
###########################################################################
#Filename      :jphacks.py
#Description   :noti
############################################################################
import RPi.GPIO as GPIO
import time
import json
import urllib.request

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

def main():
    count = 0
    while True:
        #measur distance
        distance = measure()
        
        print('distance = ',distance)
        
        #check presence sensor
        check_PIR = GPIO.input(PIRPin)
        
        #detect distance
        if distance < df['detection']:
            
            #count and turn on LED
            if check_PIR == 1 and count != 1:
                print ('********************')
                print ('*     alarm!       *')
                print ('********************')
                print ('\n')
                
                # noti_count = {'count': 1}
                # url = df['url'] + 'count' + '?' + urllib.parse.urlencode(noti_count)
                # with urllib.request.urlopen(url) as data:
                #     print('ok')
                url = df['url'] + 'count'
                urllib.request.urlopen(url)
                
                GPIO.output(LEDPin_G,GPIO.HIGH)
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
    try:
            main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()
        pass
