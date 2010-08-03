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
#include "comm.h"
#include "actuators.h"

#include "generated/messages.h"
#include "generated/settings.h"

#define MOTOR_SPEED 30

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

uint32_t t0, t1, diff;

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

    comm_init(COMM_TELEMETRY);

    actuators_init(ACTUATOR_BANK_MOTORS);

    int_enable();
}

static inline void main_periodic_task( void ) {
    static uint16_t i = 0;

    switch(i++) 
    {
        case 1:
            actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_FRONT, 0);
            actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_BACK, 0);
            actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_RIGHT, 0);
            actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_LEFT, 0);
            break;
        case 2001:
            actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_FRONT, MOTOR_SPEED);
            break;
        case 4001:
            actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_BACK, MOTOR_SPEED);
            break;
        case 6001:
            actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_RIGHT, MOTOR_SPEED);
            break;
        case 8001:
            actuators_set(ACTUATOR_BANK_MOTORS | MOTOR_LEFT, MOTOR_SPEED);
            break;
        case 10001:
            i = 0;
            break;
    }
    actuators_commit(ACTUATOR_BANK_MOTORS);
}

static inline void main_event_task( void ) {

}

