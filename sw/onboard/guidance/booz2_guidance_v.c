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
#include "rc.h"
#include "guidance.h"
#include "booz2_guidance_v.h"
#include "stabilization/booz2_stabilization.h"

#include "generated/radio.h"

uint8_t booz2_guidance_v_mode;

/* direct throttle from radio control (range 0:200 */
int32_t booz2_guidance_v_rc_delta_t;

void booz2_guidance_v_init(void) {
  booz2_guidance_v_mode = BOOZ2_GUIDANCE_V_MODE_KILL;
}

void booz2_guidance_v_read_rc(void) {
  booz2_guidance_v_rc_delta_t = (int32_t)rc_values[RADIO_THROTTLE] * 200 / MAX_PPRZ;
}

void booz2_guidance_v_mode_changed(uint8_t new_mode) {
  
  if (new_mode == booz2_guidance_v_mode)
    return;

  switch (new_mode) {
  case BOOZ2_GUIDANCE_V_MODE_RC_DIRECT:
    break;
  }

  booz2_guidance_v_mode = new_mode;
}

void booz2_guidance_v_run(bool_t in_flight) {
  switch (booz2_guidance_v_mode) {

  case BOOZ2_GUIDANCE_V_MODE_RC_DIRECT:
    booz2_stabilization_cmd[COMMAND_THRUST] = booz2_guidance_v_rc_delta_t;
    break;

  }
}


