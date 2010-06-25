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

#include "comm.h"
#include "actuators.h"
#include "generated/messages.h"

typedef struct {
    uint8_t val;
    uint8_t dval;
} Servo_t;

static inline void main_init( void );
static inline void main_periodic_task( void );
static inline void main_event_task( void );

uint32_t t0, t1, diff;
Servo_t servos[ACTUATOR_MAX];

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
    uint8_t i,j, num_servos, seperation;

    hw_init();
    sys_time_init();
    led_init();
    actuators_init(ACTUATOR_BANK_SERVOS);
    int_enable();

    /* Initialise all servos to values which are evenly spaced through the full range */
    num_servos = actuators_get_num(ACTUATOR_BANK_SERVOS);
    seperation = 0xFF / num_servos;
    for (i = 0, j = 0; i < num_servos; i++, j += seperation) {
        servos[i].val = j;
        /* starting moving in the forward direction */
        servos[i].dval = 1;
    }
        

}


#define SERVO_MIN           0x00
#define SERVO_MAX           0xFF
#define SERVO_SPEED         5

/* define as non zero to set all servos to this value */
//#define SERVO_FIXED_VALUE   (0xFF/2)

static inline void main_periodic_task( void ) {
    uint8_t i;
    static uint16_t cnt = 0;

    if (++cnt == SERVO_SPEED) 
    {
        /* Move all servos forward or backward by dval */
        for (i = 0; i < actuators_get_num(ACTUATOR_BANK_SERVOS); i++) 
        {
            Servo_t *servo = &servos[i];

            /* reverse servos when they get to the end */
            if (servo->val == SERVO_MAX && servo->dval == 1)
                servo->dval = -1;
            else if (servo->val == SERVO_MIN)
                servo->dval = 1;

            /* move and set servo */
            servo->val += servo->dval;
#if SERVO_FIXED_VALUE > 0
            actuators_set(ACTUATOR_BANK_SERVOS | i, SERVO_FIXED_VALUE);
#else
            actuators_set(ACTUATOR_BANK_SERVOS | i, servo->val);
#endif
        }

        actuators_commit(ACTUATOR_BANK_SERVOS);
        cnt = 0;
    }
}

static inline void main_event_task( void ) {

}

