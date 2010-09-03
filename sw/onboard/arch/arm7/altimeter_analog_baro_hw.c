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

#include "std.h"
#include "altimeter.h"
#include "analog.h"
#include "led.h"

#include "LPC21xx.h"
#include "arm7/config.h"

#include "generated/settings.h"

#define AnalogSetDAC(x) {  DACR = x << 6; }

SystemStatus_t altimeter_system_status = STATUS_UNINITIAIZED;

uint16_t altimeter_calibration_offset;
uint16_t altimeter_calibration_raw;
uint16_t altimeter_calibration_raw_filtered;
bool_t   analog_baro_data_available;

/* offset on DAC on P0.25 */
void altimeter_init( void ) 
{
    /* turn on DAC pins */
    PINSEL1 |= 2 << 18;
    /* start calibration procedure */
    altimeter_recalibrate();
}

void altimeter_recalibrate( void )
{
    altimeter_calibration_offset = 1023;
    AnalogSetDAC(altimeter_calibration_offset);

    altimeter_calibration_raw = 0;
    altimeter_calibration_raw_filtered = 0;
    analog_baro_data_available = FALSE;

    altimeter_system_status = STATUS_INITIALIZING;
}

uint8_t
altimeter_event_task(void)
{
    uint8_t ret = FALSE;
    if (analog_baro_data_available)
    {
      ret = TRUE;
      altimeter_system_status = STATUS_ALIVE;
      analog_baro_data_available = FALSE;
    }
    return ret;
}

/* decrease offset until adc reading is over a threshold */
static inline void
analog_baro_calibrate(void)
{
    RunOnceEvery(60, {
    if (altimeter_calibration_raw_filtered < 850 && altimeter_calibration_offset >= 1) {

        if (altimeter_calibration_raw_filtered == 0)
            altimeter_calibration_offset -= 15;
        else
            altimeter_calibration_offset--;

        AnalogSetDAC(altimeter_calibration_offset);
    } else {
        altimeter_system_status = STATUS_INITIALIZED;
    }
    });
}

void
altimeter_periodic_task(void)
{
    altimeter_calibration_raw = analog_read_channel(ANALOG_CHANNEL_PRESSURE);
    altimeter_calibration_raw_filtered = (3*altimeter_calibration_raw_filtered + altimeter_calibration_raw)/4;

    if (altimeter_system_status == STATUS_INITIALIZING)
        analog_baro_calibrate();
    else if (altimeter_system_status == STATUS_INITIALIZED)
        analog_baro_data_available = TRUE;
}

int32_t
altimeter_get_altitude(void)
{ 
    return (altimeter_calibration_raw * INS_BARO_SENS_NUM)/INS_BARO_SENS_DEN;
}

