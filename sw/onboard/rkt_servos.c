/*  
 * Written by the rocket project team "Flying Kiwi" 2009
 */

/** \file rkt_servos.h
 *  \brief API for the servos on the rocket
 *
 */
 
#include "rkt_servos.h"
#include "arm7/i2c_hw.h"

#define LO_BYTE(value) ( (uint8_t) (0x00FF & value) )
#define HI_BYTE(value) ( (uint8_t) (value>>8) )

void servos_set_pid(uint16_t kp, uint16_t ki, uint16_t kd);

static uint8_t servoAddresses[] = {0x22, 0x23}; //TODO put correct addresses here

void servos_init( void ){
	i2c_init();
	
	//could set up PID control gains
	//servos_set_pid(servoID, p, i, d);
}

void servos_set_pid( ServoID_t id, uint16_t kp, uint16_t ki, uint16_t kd ) {
	uint8_t len = 0;
	i2c_buf[len++]= PID_PGAIN_HI; 
	i2c_buf[len++] = HI_BYTE(kp);
	i2c_buf[len++] = LO_BYTE(kp);
	
	i2c_buf[len++]= PID_DGAIN_HI; 
	i2c_buf[len++] = HI_BYTE(kd);
	i2c_buf[len++] = LO_BYTE(kd);
	
	i2c_buf[len++]= PID_IGAIN_HI; 
	i2c_buf[len++] = HI_BYTE(ki);
	i2c_buf[len++] = LO_BYTE(ki);
	
	bool_t finished = False;
	
	//transmit the command
	i2c_transmit(servoAddresses[id], len, &finished);
	
	//wait for it to finish
	while (finished != True){continue;}
}

void servos_set_speed( ServoID_t id, uint16_t pos, uint16_t speed ) {
	//TODO: implement this
}

void servos_set_position( ServoID_t id, uint16_t value ) {

	//slave address sent first automatically
	//so send the register address
	uint8_t len = 0;
	i2c_buf[len++]= SEEK_HI; 
	
	//convert value into two hex bytes
	i2c_buf[len++] = HI_BYTE(value)
	i2c_buf[len++] = LO_BYTE(value)
	
	bool_t finished = False;
	
	//transmit the command
	i2c_transmit(servoAddresses[id], len, &finished);
	
	//wait for it to finish
	while (finished != True){continue;}
}
