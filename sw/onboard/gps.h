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
#ifndef _GPS_H_
#define _GPS_H_

#include "std.h"
#include "math/pprz_geodetic_int.h"

typedef enum {
    GPS_FIX_NONE,
    GPS_FIX_2D,
    GPS_FIX_3D,
} GpsFix_t;

typedef struct __GPS {
    struct EcefCoor_i ecef_pos;     /* pos ECEF in cm        */
    struct EcefCoor_i ecef_speed;   /* speed ECEF in cm/s    */
    uint32_t pacc;                  /* position accuracy     */
    uint32_t sacc;                  /* speed accuracy        */
    uint16_t pdop;                  /* dilution of precision */
    uint8_t  num_sv;                /* number of sat in fix  */
    GpsFix_t fix;                   /* status of fix         */
    /* UBX NAV POSLLH */
    int32_t  lon;
    int32_t  lat;
    int32_t  hmsl;                  /* height above mean seal level (mm)   */
    uint32_t vacc;                  /* vertical accuracy (mm)              */
    uint32_t hacc;                  /* horizontal accuracy (mm)            */
    /* UBX NAV VELNED */
    int32_t  vel_n;
    int32_t  vel_e;
    /* Status */
    uint8_t buffer_overrun;
    uint8_t parse_error;
    uint8_t parse_ignored;
} GPS_t;

extern GPS_t            gps_state;
extern SystemStatus_t   gps_system_status;

void 
gps_init(void);

/**
 * return true if a gps packet has been processed
 */
bool_t
gps_event_task(void);

#endif /* _GPS_H_ */


