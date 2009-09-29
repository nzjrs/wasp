#include "std.h"
#include "config/config.h"

#include "arm7/led_hw.h"

#include "rc.h"
#include "arm7/rc_hw.h"

SystemStatus_t rc_system_status = STATUS_UNINITIAIZED;

void rc_init ( void )
{
    /* select pin for capture */
    PPM_PINSEL |= PPM_PINSEL_VAL << PPM_PINSEL_BIT;
    /* enable capture 0.2 on falling edge + trigger interrupt */
#if RADIO_CONTROL_TYPE == RC_FUTABA
    T0CCR = TCCR_CR2_F | TCCR_CR2_I;
#elif RADIO_CONTROL_TYPE == RC_JR
    T0CCR = TCCR_CR2_R | TCCR_CR2_I;
#else
    #error "rc_hw.c: Unknown RADIO_CONTROL_TYPE"
#endif

    ppm_valid = FALSE;
    rc_status = RC_REALLY_LOST;
    time_since_last_ppm = RC_REALLY_LOST_TIME;
    rc_system_status = STATUS_INITIALIZED;
}

void rc_periodic_task ( void )
{
    static uint8_t _1Hz;
    _1Hz++;

    if (_1Hz >= 60)
    {
        _1Hz = 0;
        last_ppm_cpt = ppm_cpt;
        ppm_cpt = 0;
    }

    if (time_since_last_ppm >= RC_REALLY_LOST_TIME)
    {
        rc_status = RC_REALLY_LOST;
    }
    else
    {
        if (time_since_last_ppm >= RC_LOST_TIME)
            rc_status = RC_LOST;
        time_since_last_ppm++;
    }
}

bool_t
rc_event_task ( void )
{
    if (ppm_valid)
    {
        ppm_valid = FALSE;

        ppm_cpt++;
        time_since_last_ppm = 0;
        rc_status = RC_OK;

        /** From ppm values to normalised rc_values */
        NormalizePpm();

        return TRUE;
    }
    return FALSE;
}




