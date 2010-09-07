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

#include "init.h"
#include "sys_time.h"
#include "led.h"
#include "rc.h"
#include "actuators.h"
#include "generated/settings.h"

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

int main( void ) {
    main_init();
    while(1) {
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
    actuators_init(ACTUATOR_BANK_SERVOS);
    rc_init();
    int_enable();
}

static inline void main_periodic_task( void ) {
    uint8_t i, val;

    led_periodic_task();

    rc_periodic_task();
    if (rc_status == RC_OK) {
        led_on(LED_RC);
        /* throttle values are in type pprz_t, it ranges from 0->9600
           so we need to scale this to 0->255 */
        val = (uint8_t)(((uint32_t)rc_values[RADIO_THROTTLE]*UINT8_MAX)/MAX_PPRZ);
    } else {
        led_off(LED_RC);
        val = 0;
    }

    for (i = 0; i < actuators_get_num(ACTUATOR_BANK_SERVOS); i++) 
        actuators_set(ACTUATOR_BANK_SERVOS | i, val);

    actuators_commit(ACTUATOR_BANK_SERVOS);
}

static inline void main_event_task( void ) {
    rc_event_task();
}

