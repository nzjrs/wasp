#include "actuators.h"
#include "arm7/buss_twi_blmc_hw.h"
#include "arm7/servos_4017_hw.h"

void actuators_init( uint8_t bank )
{
    if ( bank & ACTUATOR_BANK_MOTORS )
        buss_twi_blmc_init();
#if USE_SERVOS_4017
    if ( bank & ACTUATOR_BANK_SERVOS )
        servos_4017_init();
#endif
}

void actuators_set( ActuatorID_t id, uint8_t value )
{
    /* mask out the bank */
    ActuatorID_t aid = id & 0x0F;

    if ( id & ACTUATOR_BANK_MOTORS )
        buss_twi_blmc_motor_power[aid] = value;

#if USE_SERVOS_4017    
    if ( id & ACTUATOR_BANK_SERVOS ) {
        /* value is in range 0 -> 255, so scale this
           range to be in the servo range of 1000 - 2000us */
        uint16_t tmp = ((((uint32_t)value*1000)/0xFF) + 1000);
        servos_values[aid] = SERVOS_TICS_OF_USEC(tmp);
    }
#endif

}

void actuators_commit( uint8_t bank )
{
    if ( bank & ACTUATOR_BANK_MOTORS )
        buss_twi_blmc_commit();
}
