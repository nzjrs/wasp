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
#ifndef SERVOS_4017_HW_H
#define SERVOS_4017_HW_H

#include "std.h"

#include "LPC21xx.h"
#include "arm7/config.h"
#include "arm7/servos_hw.h"

#define SERVOS_4017_RESET_WIDTH         SERVOS_TICS_OF_USEC(1000)
#define SERVOS_4017_FIRST_PULSE_WIDTH   SERVOS_TICS_OF_USEC(100)

extern uint16_t servos_4017_values[SERVOS_4017_NB_CHANNELS];
extern uint8_t  servos_4017_idx;

void    servos_4017_init(void);
uint8_t servos_4017_get_num(void);
void    servos_4017_set(uint8_t id, uint8_t value);
uint8_t servos_4017_get(uint8_t id);

static inline void servos_4017_isr(void)
{
    if (servos_4017_idx == SERVOS_4017_NB_CHANNELS) 
    {
        /* Set reset high */
        SetBit(SERVO_RESET_IOSET, SERVO_RESET_PIN);
        /* Start a long 1ms reset, keep clock low */
        T0MR0 += SERVOS_4017_RESET_WIDTH;
        servos_4017_idx++;
        T0EMR &= ~TEMR_EM0;
    }
    else if (servos_4017_idx > SERVOS_4017_NB_CHANNELS) 
    {
        /* Clear the reset*/
        SetBit(SERVO_RESET_IOCLR, SERVO_RESET_PIN);
        /* assert clock */
        T0EMR |= TEMR_EM0;
        /* Starts a short pulse-like period */
        T0MR0 += SERVOS_4017_FIRST_PULSE_WIDTH;
        servos_4017_idx=0; /* Starts a new sequence next time */
    }
    else 
    {
        /* request next match */
        T0MR0 += servos_4017_values[servos_4017_idx];
        /* clock low if not last one, last is done with reset */
        if (servos_4017_idx != SERVOS_4017_NB_CHANNELS-1) 
        {
            /* raise clock pin */
            T0EMR |= TEMR_EM0;
        }
        servos_4017_idx++;
    }
}

#endif /* SERVOS_4017_HW_H */
