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

/** \file rc.h
 *  \brief Remote Control API
 *
 *  Manages the acquisition of RC signals. Channel assignment is handled
 *  by the radio XML.
 */

#ifndef RC_H
#define RC_H

#include "std.h"
#include "generated/radio.h"

extern SystemStatus_t rc_system_status;

/**
 * Connectivity of RC. The RC_LOST and RC_REALLY_LOST state seperation is
 * designed to act as hysteresis for intermittant signal loss. Backends may
 * switch between RC_OK and RC_REALLY_LOST if they wish.
 */
typedef enum {
    RC_OK,              /**< RC is connected and data is being received */
    RC_LOST,            /**< RC was connected, recently lost */
    RC_REALLY_LOST      /**< RC not connected, completely lost */
} RCStatus_t;

/**
 * Array of values of each of the RC channels. Scaled from -9600 - +9600. The
 * index in the array is determined from the radio.xml
 */
extern pprz_t       rc_values[RADIO_CTL_NB];

/**
 * FIXME
 */
extern uint8_t      rc_values_contains_avg_channels;

/**
 * Connectivity of RC
 */
extern RCStatus_t   rc_status;
/**
 * Raw unscaled RC values. Backend dependent
 */
extern uint16_t     ppm_pulses[RADIO_CTL_NB];

/**
 * To be called at startup. Backend dependant
 */
void    rc_init ( void );

/**
 * To be called at periodic frequency. Backend dependant
 */
void    rc_periodic_task ( void );

/**
 * Return TRUE if there is a valid RC signal.
 */
bool_t  rc_event_task ( void );

#endif /* RC_H */
