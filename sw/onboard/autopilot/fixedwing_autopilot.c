#include "autopilot.h"

#include "actuators.h"

#include "generated/settings.h"

uint8_t     autopilot_mode;
bool_t      autopilot_motors_on;
bool_t      autopilot_in_flight;
uint32_t    autopilot_motors_on_counter;
uint32_t    autopilot_in_flight_counter;

void autopilot_init(void)
{

}

void autopilot_periodic(void)
{

}

void autopilot_on_rc_event(void)
{

}

void autopilot_set_mode(uint8_t new_autopilot_mode)
{
    if (new_autopilot_mode != autopilot_mode) 
    {
        bool_t ok = TRUE;
        switch (new_autopilot_mode)
        {
            case BOOZ2_AP_MODE_FAILSAFE:
            case BOOZ2_AP_MODE_KILL:
                break;
            case BOOZ2_AP_MODE_RATE_DIRECT:
                break;
            case BOOZ2_AP_MODE_ATTITUDE_DIRECT:
                break;
            default:
                ok = FALSE;
                break;
        }
        if (ok)
            autopilot_mode = new_autopilot_mode;
    }
}

void autopilot_set_actuators(void)
{
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_set(ACTUATOR_BANK_SERVOS | 0, 0);
    actuators_commit(ACTUATOR_BANK_SERVOS);
}
