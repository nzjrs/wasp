#include "std.h"
#include "rc.h"

#include "generated/radio.h"

#include "led.h"

SystemStatus_t rc_system_status = STATUS_UNINITIAIZED;

void rc_init ( void )
{
    led_log("Start some threads\n");   
}

void rc_periodic_task ( void )
{
    /* Take your mutex */
    /* Copy the values for each channel */
    rc_values[RADIO_ROLL] = 4500;
    rc_status = RC_OK;
    ppm_pulses[RADIO_ROLL] = 12000;
    /* Release the mutex */

    //FIXME: (JOHN) Set and document this
    //rc_values_contains_avg_channels;
}

bool_t rc_event_task ( void )
{
    /* See docs, return trur if valid */
    return TRUE;
}
