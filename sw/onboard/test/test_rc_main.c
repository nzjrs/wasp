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
#include <inttypes.h>

#include "std.h"
#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "comm.h"
#include "rc.h"
#include "generated/messages.h"
#include "generated/settings.h"

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

int main( void ) {
    main_init();
    while(1)
    {
        if (sys_time_periodic())
            main_periodic_task();
        main_event_task();
    }
    return 0;
}

static inline void main_init( void ) {
    hw_init();
    sys_time_init();
    led_init();

    comm_init(COMM_1);

    rc_init();

    int_enable();
}

static inline void main_periodic_task( void ) {
    comm_periodic_task(COMM_1);

    rc_periodic_task();
    if (rc_status == RC_OK)
        led_on(LED_RC);
    else
        led_off(LED_RC);

    RunOnceEvery(250, {
        MESSAGE_SEND_PPM(COMM_1, ppm_pulses);
        MESSAGE_SEND_RC(COMM_1, rc_values);
    });

}

static inline void main_event_task( void )
{
    comm_event_task(COMM_1);
    rc_event_task();
}

