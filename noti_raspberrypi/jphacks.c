/*

jphacks Noti sensor

*/
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>

#define    trigPin    0
#define    echoPin    2
#define    PIRPin     3
#define    LEDPin_G   21
#define    LEDPin_Y   22
#define    LEDPin_R   23

#define    detection  10.0

int count = 0;
int check_LED = 0;

//distance measurment function
int pulseIn(int pin, int level, int timeout)
{
   struct timeval tn, t0, t1;
   long micros;
   gettimeofday(&t0, NULL);
   micros = 0;
   while (digitalRead(pin) != level)
   {
      gettimeofday(&tn, NULL);
      if (tn.tv_sec > t0.tv_sec) micros = 1000000L; else micros = 0;
      micros += (tn.tv_usec - t0.tv_usec);
      if (micros > timeout) return 0;
   }
   gettimeofday(&t1, NULL);
   while (digitalRead(pin) == level)
   {
      gettimeofday(&tn, NULL);
      if (tn.tv_sec > t0.tv_sec) micros = 1000000L; else micros = 0;
      micros = micros + (tn.tv_usec - t0.tv_usec);
      if (micros > timeout) return 0;
   }

   if (tn.tv_sec > t1.tv_sec) micros = 1000000L; else micros = 0;
   micros = micros + (tn.tv_usec - t1.tv_usec);
   return micros;
}

//main function
int main (int argc, char **argv) {
  double duration, distance;

//Pin setup
  if(wiringPiSetup() == -1) return 0;
  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
  pinMode(PIRPin,INPUT);
  pinMode(LEDPin_G,OUTPUT);
  pinMode(LEDPin_Y,OUTPUT);
  pinMode(LEDPin_R,OUTPUT);
  
while(1){
//measure distance by sonar
  //digitalWrite(trigPin, LOW); 
  //delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH, 1000000);
  distance = (duration/2) / 29.1;
  printf("distance=%lf cm\n",distance);

//check presence sensor
  check_LED=digitalRead(PIRPin);

//detect distanse  
  if(distance < detection){

//count and turn on or turn off LED
  		if(check_LED && count != 1){
		printf("===================|\n");
		printf("|      alarm...    |\n");
		printf("===================|\n");
      digitalWrite(LEDPin_G, HIGH); 
      count = 1;
		};
   }
   else{
      count =0 ;
      if(!check_LED)digitalWrite(LEDPin_G, LOW); 
   };
      
  delay(500);
		}
}
