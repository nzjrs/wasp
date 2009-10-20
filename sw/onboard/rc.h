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
#ifndef RC_H
#define RC_H

#include "std.h"
#include "config/config.h"

#include "generated/radio.h"

typedef enum {
    RC_OK,
    RC_LOST,
    RC_REALLY_LOST
} RCStatus_t;

extern pprz_t       rc_values[RADIO_CTL_NB];
extern RCStatus_t   rc_status;

extern SystemStatus_t rc_system_status;

extern uint8_t  rc_values_contains_avg_channels;
extern uint8_t  time_since_last_ppm;
extern uint8_t  ppm_cpt, last_ppm_cpt;
extern uint16_t ppm_pulses[RADIO_CTL_NB];
extern bool_t   ppm_valid;

void
rc_init ( void );

void
rc_periodic_task ( void );

/**
 * @return: TRUE if there is a valid RC signal
 */
bool_t
rc_event_task ( void );

#endif /* RC_H */
