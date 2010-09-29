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
#ifndef _GUIDANCE_H_
#define _GUIDANCE_H_

#include "std.h"

#define BOOZ2_GUIDANCE_H_MODE_KILL      0
#define BOOZ2_GUIDANCE_H_MODE_RATE      1
#define BOOZ2_GUIDANCE_H_MODE_ATTITUDE  2
#define BOOZ2_GUIDANCE_H_MODE_HOVER     3

#define BOOZ2_GUIDANCE_V_MODE_KILL      0
#define BOOZ2_GUIDANCE_V_MODE_RC_DIRECT 1
#define BOOZ2_GUIDANCE_V_MODE_CLIMB     3
#define BOOZ2_GUIDANCE_V_MODE_HOVER     4

extern uint8_t booz2_guidance_h_mode;
extern uint8_t booz2_guidance_v_mode;

void guidance_init(void);

#endif /* _GUIDANCE_H_ */
