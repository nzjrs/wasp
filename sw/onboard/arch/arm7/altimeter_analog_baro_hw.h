/*
 * Copyright (C) 2008  Antoine Drouin
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

#ifndef BOOZ2_ANALOG_BARO_H
#define BOOZ2_ANALOG_BARO_H

#include "std.h"
#include "altimeter.h"

#include "LPC21xx.h"
#include "arm7/config.h"
#include "arm7/led_hw.h"

#include "generated/settings.h"

#define Booz2AnalogSetDAC(x) {  DACR = x << 6; }

/* decrease offset until adc reading is over a threshold */
static inline void
booz2_analog_baro_calibrate(void)
{
    RunOnceEvery(60, {
	if (booz2_analog_baro_value_filtered < 850 && booz2_analog_baro_offset >= 1) 
    {
        if (booz2_analog_baro_value_filtered == 0)
            booz2_analog_baro_offset -= 15;
	    else
	        booz2_analog_baro_offset--;

        Booz2AnalogSetDAC(booz2_analog_baro_offset);

        altimeter_system_status = STATUS_INITIALIZING;
	    LED_TOGGLE(LED_BARO);
    }
	else
    {
        altimeter_system_status = STATUS_INITIALIZED;
        LED_ON(LED_BARO);
    }
    });
}

static inline void
booz2_analog_baro_isr(uint16_t val)
{
    booz2_analog_baro_value = val;
    booz2_analog_baro_value_filtered = (3*booz2_analog_baro_value_filtered + booz2_analog_baro_value)/4;
    if (altimeter_system_status != STATUS_INITIALIZED)
        booz2_analog_baro_calibrate();
    booz2_analog_baro_data_available = TRUE;
}

#endif /* BOOZ2_ANALOG_BARO_H */
