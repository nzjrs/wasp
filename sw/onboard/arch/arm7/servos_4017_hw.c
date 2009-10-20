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
#include "config/airframe.h"

#include "arm7/sys_time_hw.h"
#include "arm7/servos_4017_hw.h"

#define START_TIMEOUT 0xFFFF;

uint8_t servos_4017_idx;
uint16_t servos_values[SERVOS_4017_NB_CHANNELS];

void servos_4017_init ( void ) 
{
    uint8_t i;

    /* select clock pin as MAT0.0 output */
    SERVO_CLOCK_IODIR  |= _BV(SERVO_CLOCK_PIN);
    SERVO_CLOCK_PINSEL |= SERVO_CLOCK_PINSEL_VAL << SERVO_CLOCK_PINSEL_BIT;

    /* select reset pin as GPIO output */
    SERVO_RESET_IODIR  |= _BV(SERVO_RESET_PIN);

    /* assert RESET */
    SetBit(SERVO_RESET_IOSET, SERVO_RESET_PIN);

    /* enable match 0 interrupt */
    T0MCR |= TMCR_MR0_I;

    /* assert clock */
    T0EMR |= TEMR_EM0;	
    /* set low on match 0 */
    T0EMR |= TEMR_EMC0_1;

    /* set first pulse in a while */
    T0MR0 = START_TIMEOUT;
    servos_4017_idx = SERVOS_4017_NB_CHANNELS;

    /* Set all servos at their midpoints */
    /* compulsory for unaffected servos */
    for( i=0 ; i < SERVOS_4017_NB_CHANNELS ; i++ )
        servos_values[i] = SERVOS_TICS_OF_USEC(1500);

}


