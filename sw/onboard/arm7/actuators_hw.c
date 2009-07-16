#include "actuators.h"
#include "arm7/buss_twi_blmc_hw.h"
#include "arm7/servos_4017_hw.h"

void actuators_init( void )
{
    buss_twi_blmc_init();
#if USE_SERVOS_4017
    servos_4017_init();
#endif
}

void actuators_set( ActuatorID_t id, uint8_t value )
{
    buss_twi_blmc_motor_power[id] = value;
}

void actuators_commit( void )
{
    buss_twi_blmc_commit();
}
