#include "led.h"
#include "actuators.h"

#include "generated/settings.h"

#define NPS_MAX_ACTUATORS (ACTUATOR_BANK_MAX * ACTUATOR_MAX)
static uint8_t actuators[NPS_MAX_ACTUATORS];

void actuators_init( uint8_t bank )
{
    for (int i = 0; i < NPS_MAX_ACTUATORS; i++)
        actuators[i] = 0;
}

/* actuators are arranged in 4 banks of 16. Because of how access is done
in the oboard API these banks are in the ranges 16-32, 32-48, 64-80 and 128-144
so we convert that into a single number 0-64 so we can use a single array for
storage */
static uint8_t actuator_id_to_index(ActuatorID_t id)
{
    uint8_t base;
    uint8_t offset = (id & 0x0F);

    switch (id & 0xF0) {
        case ACTUATOR_BANK_MOTORS:
            base = 0 * ACTUATOR_MAX; break;
        case ACTUATOR_BANK_SERVOS:
            base = 1 * ACTUATOR_MAX; break;
        case ACTUATOR_BANK_3:
            base = 2 * ACTUATOR_MAX; break;
        case ACTUATOR_BANK_4:
            base = 4 * ACTUATOR_MAX; break;
        default:
            led_log("Unknown actuator bank 0x%X\n", id & 0xF0);
            return 0;
    }

    return base + offset;
}

void actuators_set( ActuatorID_t id, uint8_t value )
{
    actuators[ actuator_id_to_index(id) ] = value;
}

void actuators_commit( uint8_t bank )
{
    ;
}

uint8_t actuators_get_num( uint8_t bank )
{
    return 0;
}

uint8_t actuators_get( ActuatorID_t id )
{
    return actuators[ actuator_id_to_index(id) ];
}


