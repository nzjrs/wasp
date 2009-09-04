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
    
    if ( id & ACTUATOR_BANK_SERVOS )
        servos_values[aid] = value;
}

void actuators_commit( uint8_t bank )
{
    if ( bank & ACTUATOR_BANK_MOTORS )
        buss_twi_blmc_commit();
}
