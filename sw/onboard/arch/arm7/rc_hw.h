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
#ifndef RC_HW_H
#define RC_HW_H

#include "std.h"
#include "rc.h"

#include "arm7/sys_time_hw.h"   /* for SYS_TICS_OF_USEC */

#include "generated/radio.h"

#define RC_AVG_PERIOD 8
#define RC_LOST_TIME 30         /* 500ms with a 60Hz timer */
#define RC_REALLY_LOST_TIME 60  /* ~1s */

int32_t     avg_rc_values[RADIO_CTL_NB];
bool_t      ppm_valid;
uint8_t     state;
uint32_t    last;
uint8_t     time_since_last_ppm;
uint8_t     ppm_cpt, last_ppm_cpt;

static inline void ppm_isr ( void )
{
    uint32_t now = T0CR2;
    uint32_t length = now - last;
    last = now;

    rc_system_status = STATUS_ALIVE;

    if (state == RADIO_CTL_NB)
    {
        if (length > SYS_TICS_OF_USEC(PPM_SYNC_MIN_LEN) &&
                length < SYS_TICS_OF_USEC(PPM_SYNC_MAX_LEN))
        {
            state = 0;
        }
    }
    else
    {
        if (length > SYS_TICS_OF_USEC(PPM_DATA_MIN_LEN) &&
                length < SYS_TICS_OF_USEC(PPM_DATA_MAX_LEN))
        {
            ppm_pulses[state] = length;
            state++;
            if (state == RADIO_CTL_NB)
                ppm_valid = TRUE;
        }
        else
            state = RADIO_CTL_NB;
    }
}

#endif /* RC_HW_H */
