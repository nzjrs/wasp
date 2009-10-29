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
#ifndef BOOZ2_INS_H
#define BOOZ2_INS_H

#include "std.h"
#include "config/config.h"
#include "booz_geometry_int.h"
#include "pprz_geodetic_int.h"

typedef struct __INS {
    /* gps transformed to LTP-NED  */
    struct LtpDef_i     ltp_def;
    bool_t              ltp_initialised;
    struct NedCoor_i    gps_pos_cm_ned;
    struct NedCoor_i    gps_speed_cm_s_ned;
#if USE_VFF
    /* barometer                   */
    int32_t             baro_alt;
    int32_t             qfe;
    bool_t              baro_initialised;
    bool_t              vff_realign; 
#endif
    /* output LTP NED               */
    struct NedCoor_i    ltp_pos;
    struct NedCoor_i    ltp_speed;
    struct NedCoor_i    ltp_accel;
    /* output LTP ENU               */
    struct EnuCoor_i    enu_pos;
    struct EnuCoor_i    enu_speed;
    struct EnuCoor_i    enu_accel;
} INS_t;

extern INS_t    ins;

void            ins_init( void );
void            ins_propagate( void );
void            ins_update_baro( void );
void            ins_update_gps( void );


#endif /* BOOZ2_INS_H */
