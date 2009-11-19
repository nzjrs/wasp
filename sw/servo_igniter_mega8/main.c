/* Name: main.c
   Purpose : Main file for rocketry servo/igniter Mega8
   Author : Avinash Rao
   Date: 18/11/09
*/

/* INFO
	This code will initally implement interrupt-based servo PWM before implementing SPI control of PWM if PWM generation works well
*/

// #Includes

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>

#include "global.h"
#include "timer.h"

// Define servo pins TODO: Put correct pins here

#define SERVO1	PC0
#define	SERVO2	PC1
#define SERVO3  PC2
#define SERVO4	PC3


/* Function to intialise data direction register */
void init_ddr(void){
	//Initialise Data Direction Registers TODO: Implement this
	outb(DDRC, 0xFF);
}

/* Function to set the pin for a particular servo high */

void set_servos (u08 *servo_status){
	
	u08 i;
	// Read port c
	u08 servos = inb(PINC);

	for (i=0; i<4; i++){
		
	}
}


/* Begin main operation */

int main (void)
{

// Set DDRs
	init_ddr();

// Enable interrupts
	sei();

// Initialise Timer 0 (16 bit timer) and set prescale to 1024x
	timer1Init();								///< initialize timer1
	timer1SetPrescaler(TIMER_CLK_DIV1024);		///< set timer1 prescaler

//Make Variable to Hold Number of half-cylces:
		u08 half_cycles = 0;

//Make variable to hold half-cycle counts
		u16 hc_counts = 0;

// Make array to hold status of each servo pin
		u08 servo_status[4] = {0,0,0,0};

// Make array to hold position of each servo pin
		u08 servo_pos[4] = {50,50,50,50};

// Begin main loop

	int i;

	while(1){
		
		if(half_cycles == 0){
			for (i = 0; i < 4; i++){
				servo_status[i] = TRUE;
			}
		}

		else if(half_cycles == 1){
			if(hc_counts >= servo_pos[1]){
				servo_status[1] = FALSE;
			}
			if(hc_counts >= servo_pos[2]){
				servo_status[1] = FALSE;
			}
			if(hc_counts >= servo_pos[3]){
				servo_status[1] = FALSE;
			}
			if(hc_counts >= servo_pos[4]){
				servo_status[1] = FALSE;
			}
		}

		else if(half_cycles > 1){	
			for (i = 0; i < 4; i++){
				servo_status[i] = FALSE;
			}
		}

		set_servos(servo_status);

		}

	
}

