/* Name: main.c
   Purpose : Main file to test 16 bit timer
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

// Define LED pin

#define LED		0


/* Function to intialise data direction register */
void init_ddr(void){
	//Initialise Data Direction Registers TODO: Implement this
	outb(DDRB, 0xFF);
}

/* Function to set the pin for a particular servo high */

void set_servos (u08 *servo_status){
	
	u08 i;
	// Read port c
	u08 servos = inb(PINC);

	for (i=0; i<4; i++){
		
	}
}

/* Should set up TCNT1 to be in phase and frequency correct mode */

void phase_freq_correct_init(void){
	//TCCR1A |= (COM1A1 | COM1A0 | COM1B1 | COM1B0);
	//TCCR1B |= (ICES1 | WGM13 | CS10);
	TCCR1A = 0xA0;
	TCCR1B = 0x11;
}


/* Begin main operation */

int main (void)
{

// Set DDRs
	init_ddr();

// Enable interrupts
	sei();

// Initialise Timer 1 (16 bit timer) and set prescale to 1024
	phase_freq_correct_init();

//Initialise Timer 0 (8 bit timer)
	timer0Init();
	timer0SetPrescaler(TIMER_CLK_DIV1024);

// Set desired period and DC

	ICR1 = 10000;
	OCR1A = 600;
	OCR1B = 600;

    
// Begin main loop

	u16 servo_pos = 0;
	u16 full_count = 0;
	u16 cycle_count = 0;

	while(1){
		
		if(TCNT0>100){
			cycle_count++;
			TCNT0 = 0;
		}
		if (cycle_count > 10){
			cycle_count=0;
			servo_pos += 3;
		}
		
		if(servo_pos >= 500){
			servo_pos = 0;
		}

		OCR1A = servo_pos + 500;

		if(TCNT1 > 5000){
			sbi(PORTB, LED);
		}
		else{
			cbi(PORTB, LED);
		}
		
		
	}
}
