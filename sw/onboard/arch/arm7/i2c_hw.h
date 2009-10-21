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
#ifndef I2C_HW_H
#define I2C_HW_H

#include "LPC21xx.h"
#include "std.h"
#include "config/config.h"

#define I2C_BUF_LEN     16
#define I2C1_BUF_LEN    16

/**
 * Callback for when the I2C state machine reaches the STOP state
 */
typedef void (*I2cStopCallback_t)(void);

#if USE_I2C0

extern volatile uint8_t i2c_status;
extern volatile uint8_t i2c_buf[I2C_BUF_LEN];
extern volatile I2cStopCallback_t i2c_stop_callback;

void i2c_init(void);
void i2c_receive(uint8_t slave_addr, uint8_t len, volatile bool_t* finished);
void i2c_transmit(uint8_t slave_addr, uint8_t len, volatile bool_t* finished);

#endif  /* USE_I2C1 */

#if USE_I2C1

extern volatile uint8_t i2c1_status;
extern volatile uint8_t i2c1_buf[I2C1_BUF_LEN];
extern volatile I2cStopCallback_t i2c1_stop_callback;

void i2c1_init(void);
void i2c1_receive(uint8_t slave_addr, uint8_t len, volatile bool_t* finished);
void i2c1_transmit(uint8_t slave_addr, uint8_t len, volatile bool_t* finished);

#endif /* USE_I2C1 */

#endif /* I2C_HW_H */
