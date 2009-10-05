/*  
 * Addresses for the openservo registers
 * Written by the rocket project team "Flying Kiwi" 2009
 */

#ifndef RKT_SERVO_DEFNS_H
#define RKT_SERVO_DEFN_H


/***  OPEN SERVO REGISTERS ***/
#define DEVICE_TYPE		0x00	
#define DEVICE_SUBTYPE		0x01	
#define VERSION_MAJOR		0x02
#define VERSION_MINOR		0x03
#define FLAGS_HI 		0x04
#define FLAGS_LO		0x05
#define	TIMER_HI		0x06
#define	TIMER_LO		0x07
#define POSITION_HI		0x08
#define POSITION_LO		0x09
#define VELOCITY_HI 		0x0A
#define VELOCITY_LO		0x0B
#define POWER_HI		0x0C
#define POWER_LO		0x0D
#define PWM_CW			0x0E
#define PWM_CCW			0x0F
#define SEEK_HI			0x10
#define SEEK_LO			0x11
#define SEEK_VELOCITY_HI	0x12
#define SEEK_VELOCITY_LO	0x13
#define VOLTAGE_HI		0x14
#define VOLTAGE_LO		0x15
#define CURVE_RESERVED		0x16
#define CURVE_BUFFER		0x17	
#define CURVE_DELTA_HI		0x18
#define CURVE_DELTA_LO		0x19
#define CURVE_POSITION_HI	0x1A
#define CURVE_POSITION_LO	0x1B
#define CURVE_IN_VELOCITY_HI	0x1C
#define CURVE_IN_VELOCITY_LO	0x1D
#define CURVE_OUT_VELOCITY_HI	0x1E
#define CURVE_OUT_VELOCITY_LO	0x1F
//#define TWI_ADDRESS		0x10 // Shifted left one for protocol difference. 
// Could change it to work with 0x20, but couldn't be buggered.

#define TWI_ADDRESS		0x20

#define PID_DEADBAND		0x21
#define PID_PGAIN_HI		0x22
#define PID_PGAIN_LO		0x23
#define PID_DGAIN_HI		0x24	
#define PID_DGAIN_LO		0x25
#define PID_IGAIN_HI		0x26
#define PID_IGAIN_LO		0x27
#define PWM_FREQ_DIVIDER_HI	0x28	
#define PWM_FREQ_DIVIDER_LO	0x29
#define MIN_SEEK_HI		0x2A
#define MIN_SEEK_LO		0x2B
#define MAX_SEEK_HI		0x2C
#define MAX_SEEK_LO		0x2D
#define REVERSE_SEEK		0x2E


/*** OPEN SERVO COMMANDS ***/
#define RESET			0x80
#define CHECKED_TXN		0x81
#define PWM_ENABLE		0x82
#define PWM_DISABLE		0x83
#define WRITE_ENABLE		0x84
#define WRITE_DISABLE		0x85
#define REGISTERS_SAVE		0x86
#define REGISTERS_RESTORE	0x87
#define REGISTERS_DEFAULT	0x88
#define EEPROM_ERASE		0x89
#define VOLTAGE_READ		0x90
#define CURVE_MOTION_ENABLE	0x91
#define CURVE_MOTION_DISABLE	0x92
#define CURVE_MOTION_RESET	0x93
#define CURVE_MOTION_APPEND	0x94

#endif /* RKT_SERVO_DEFNS_H */

