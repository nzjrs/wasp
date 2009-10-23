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
#include "actuators.h"
#include "arm7/buss_twi_blmc_hw.h"
#include "arm7/servos_4017_hw.h"

void actuators_init( uint8_t bank )
{
    if ( bank & ACTUATOR_BANK_MOTORS )
        buss_twi_blmc_init();
#if USE_SERVOS_4017
    if ( bank & ACTUATOR_BANK_SERVOS )
        servos_4017_init();
#endif
}

void actuators_set( ActuatorID_t id, uint8_t value )
{
    /* mask out the bank */
    ActuatorID_t aid = id & 0x0F;

    if ( id & ACTUATOR_BANK_MOTORS )
        buss_twi_blmc_motor_power[aid] = value;

#if USE_SERVOS_4017    
    if ( id & ACTUATOR_BANK_SERVOS ) {
        /* value is in range 0 -> 255, so scale this
           range to be in the servo range of 1000 - 2000us */
        uint16_t tmp = ((((uint32_t)value*1000)/0xFF) + 1000);
        /*FIXME: HACK HACK BROKEN BROKEN. 
        THE FIRST TWO CHANNELS DO NOT SO SUBTRACT 2 FROM THE INDEX.
        !!!!!!
        THIS MEANS WE DO NOT HAVE TO CHANGE ANY SETTINGS LATER, BUT LIMITS
        US TO 6 CHANNELS
        !!!!!!
        NEED TO FIX THE TIMING IN SERVOS_4017_HW.c */
        if (aid >= 2)
            aid -= 2;
        servos_values[aid] = SERVOS_TICS_OF_USEC(tmp);
    }
#endif

}

void actuators_commit( uint8_t bank )
{
    if ( bank & ACTUATOR_BANK_MOTORS )
        buss_twi_blmc_commit();
}
