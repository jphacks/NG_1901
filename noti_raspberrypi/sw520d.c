/********************************************************************************************
*Filename      : sw520d.c
*Description   : If the SW520D tilt red led flashing alarm
*Author        : Alan
*Website       : www.osoyoo.com
*Update        : 2017/06/20
********************************************************************************************/
#include <wiringPi.h>
#include <stdio.h>

#define LedPin		22
#define Sw520dPin	21

int main(void)
{
	// When initialize wiring failed, print messageto screen
	if(wiringPiSetup() == -1){
		printf("setup wiringPi failed !");
		return 1; 
	}
	
	pinMode(LedPin, OUTPUT);
	pinMode(Sw520dPin,INPUT);

	printf("\n");
	printf("\n");
	printf("========================================\n");
	printf("|              LED alarm               |\n");
	printf("|    ------------------------------    |\n");
	printf("|        If SW520D tilt                |\n");
	printf("|                                      |\n");
	printf("|        LED will Blink                |\n");
	printf("|                                      |\n");
	printf("|                                OSOYOO|\n");
	printf("========================================");
	printf("\n");
	printf("\n");
	
	while(1){
		if(!(digitalRead(Sw520dPin))){
		// LED off
		digitalWrite(LedPin, HIGH);
		printf("\n");
		printf("-------------------|\n");
		printf("|     Not tilt...  |\n");
		printf("-------------------|\n");
		printf("Not tilt...\n");
		delay(1000);
		}
		else{
		// LED blink
		digitalWrite(LedPin, LOW);
		delay(500);
		digitalWrite(LedPin,HIGH);
		delay(500);
		printf("\n");
		printf("===================|\n");
		printf("|     tilting!     |\n");
		printf("===================|\n");
		}
	}

	return 0;
}

