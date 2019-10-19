#!/usr/bin/python
###########################################################################
#Filename      :jphacks.py
#Description   :noti
############################################################################
import RPi.GPIO as GPIO
import time
import json
import urllib.request

# set BCM_GPIO
# 登録と交換用のボタン
PushButton = 19
trigPin   = 17
echoPin   = 27
PIRPin    = 22
LEDPin_G  =  5
LEDPin_Y  =  6
LEDPin_R  = 13

# 反応最大距離設定
detection = 200.0

# 各種カウント
count     = 0
check_LED = 0
count_sensor = 0
count_button = 0
distance_total = 0

# 設定ファイル読み込み
with open('./config.json') as data:
    config = json.load(data)

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    # 物理ボタン
    GPIO.setup(PushButton,GPIO.IN)
    # 超音波センサ1
    GPIO.setup(trigPin,GPIO.OUT,initial=GPIO.LOW)
    # 超音波センサ2
    GPIO.setup(echoPin,GPIO.IN)
    # 人感センサ
    GPIO.setup(PIRPin,GPIO.IN)
    # 緑
    GPIO.setup(LEDPin_G,GPIO.OUT,initial=GPIO.LOW)
    # 黄
    GPIO.setup(LEDPin_Y,GPIO.OUT,initial=GPIO.LOW)
    # 赤
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
        if distance < config['detection']:
            #count and turn on LED
            if check_PIR == 1 and count != 1:
                print ('********************')
                print ('*     alarm!       *')
                print ('********************')
                print ('\n')
                
                url = config['url'] + 'count'
                print(url)
                urllib.request.urlopen(url)
                
                GPIO.output(LEDPin_G,GPIO.HIGH)
                count = 1
        else:
            count = 0
            # if check_PIR != 1:
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
