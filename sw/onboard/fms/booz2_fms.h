/*
 * 
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

#ifndef BOOZ2_FMS_H
#define BOOZ2_FMS_H

#include "std.h"
#include "gps.h"
#include "guidance.h"
#include "math/pprz_algebra_int.h"

#include "generated/settings.h"

#define BOOZ2_FMS_TYPE_NONE         0
#define BOOZ2_FMS_TYPE_DATALINK     1
#define BOOZ2_FMS_TYPE_TEST_SIGNAL  2

struct Booz_fms_imu_info {
  struct Int16Vect3 gyro;
  struct Int16Vect3 accel;
  struct Int16Vect3 mag;
};

struct Booz_fms_gps_info {
  struct Int32Vect3   pos;
  struct Int16Vect3   speed;
  int32_t                   pacc;
  uint8_t                   num_sv;
  GpsFix_t                  fix;
};

struct Booz_fms_ahrs_info {
  struct Int16Eulers euler;
  struct Int16Eulers  rate;
};

struct Booz_fms_info {
  struct Booz_fms_imu_info  imu;
  struct Booz_fms_gps_info  gps;
  struct Booz_fms_ahrs_info ahrs;
  //  struct Booz_fms_ins_info  ins;
};

struct Booz_fms_command {
  union {
    struct Int32Vect3  rate;
    struct Int32Eulers attitude;
    struct Int32Vect2 speed;
    struct Int32Vect3 pos; //FIXME Warning z is heading
  } h_sp;
  union {
    int32_t direct;
    int32_t climb;
    int32_t height;
  } v_sp;
  uint8_t h_mode;
  uint8_t v_mode;
};

extern bool_t  booz_fms_on;
extern bool_t  booz_fms_timeout;
extern uint8_t booz_fms_last_msg;

extern struct Booz_fms_info    booz_fms_info;
extern struct Booz_fms_command booz_fms_input;

extern void booz_fms_init(void);
extern void booz_fms_set_on_off(bool_t state);
extern void booz_fms_periodic(void);
extern void booz_fms_update_info(void);

#if BOOZ2_FMS_TYPE == BOOZ2_FMS_TYPE_DATALINK
#include "booz2_fms_datalink.h"
#elif BOOZ2_FMS_TYPE == BOOZ2_FMS_TYPE_TEST_SIGNAL
#include "booz2_fms_test_signal.h"
#endif

#define BOOZ2_FMS_SET_POS_SP(_pos_sp,_psi_sp) { \
  _pos_sp.x = booz_fms_input.h_sp.pos.x; \
  _pos_sp.y = booz_fms_input.h_sp.pos.y; \
  /*_psi_sp = booz_fms_input.h_sp.pos.z;*/ \
}

#define BOOZ2_FMS_POS_INIT(_pos_sp,_psi_sp) { \
  booz_fms_input.h_sp.pos.x = _pos_sp.x; \
  booz_fms_input.h_sp.pos.y = _pos_sp.y; \
  booz_fms_input.h_sp.pos.z = _psi_sp; \
}

#endif /* BOOZ2_FMS_H */


