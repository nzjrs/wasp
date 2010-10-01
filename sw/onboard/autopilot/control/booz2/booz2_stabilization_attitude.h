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
#ifndef BOOZ2_STABILIZATION_ATTITUDE_H
#define BOOZ2_STABILIZATION_ATTITUDE_H

#include "math/pprz_algebra_int.h"

void booz2_stabilization_attitude_init(void);
void booz2_stabilization_attitude_read_rc(struct Int32Eulers *sp, bool_t in_flight);
void booz2_stabilization_attitude_reset_psi_ref(struct Int32Eulers *sp);
void booz2_stabilization_attitude_enter(void);
void booz2_stabilization_attitude_run(bool_t in_flight, int32_t *stabilization_cmd);

extern struct Int32Eulers booz_stabilization_att_sp;

#endif /* BOOZ2_STABILIZATION_ATTITUDE_H */
