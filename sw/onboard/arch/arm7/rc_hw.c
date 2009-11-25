/*
 * Copyright (C) 2008 Antoine Drouin
 * Copyright (C) 2009 John Stowers
 *
 * This file is part of wasp, some code taken from paparazzi (GPL)
 *
 * wasp is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * wasp is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, write to
 * the Free Software Foundation, 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 */
#include "std.h"

#include "rc.h"
#include "arm7/rc_hw.h"
#include "arm7/led_hw.h"

#include "config/config.h"

SystemStatus_t rc_system_status = STATUS_UNINITIAIZED;

void rc_init ( void )
{
    /* select pin for capture */
    PPM_PINSEL |= PPM_PINSEL_VAL << PPM_PINSEL_BIT;
    /* enable capture 0.2 on falling edge + trigger interrupt */
#if PPM_PULSE_TYPE == PPM_PULSE_TYPE_POSITIVE
    T0CCR = TCCR_CR2_F | TCCR_CR2_I;
#elif PPM_PULSE_TYPE == PPM_PULSE_TYPE_NEGATIVE
    T0CCR = TCCR_CR2_R | TCCR_CR2_I;
#else
    #error "Invalid ppm pulse type, check radio.xml"
#endif

    ppm_valid = FALSE;
    rc_status = RC_REALLY_LOST;
    time_since_last_ppm = RC_REALLY_LOST_TIME;
    rc_system_status = STATUS_INITIALIZED;
    state = RADIO_CTL_NB;
    last = 0;
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




