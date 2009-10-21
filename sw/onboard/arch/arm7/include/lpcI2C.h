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
/******************************************************************************
 *
 * $RCSfile$
 * $Revision$
 *
 * Header file for Philips LPC ARM Processors.
 * Copyright 2004 R O SoftWare
 *
 * No guarantees, warrantees, or promises, implied or otherwise.
 * May be used for hobby or commercial purposes provided copyright
 * notice remains intact.
 *
 *****************************************************************************/
#ifndef INC_LPC_I2C_H
#define INC_LPC_I2C_H

// I2C Interface Registers
typedef struct
{
  REG_8 conset;                         // Control Set Register
  REG_8 _pad0[3];
  REG_8 stat;                           // Status Register
  REG_8 _pad1[3];
  REG_8 dat;                            // Data Register
  REG_8 _pad2[3];
  REG_8 adr;                            // Slave Address Register
  REG_8 _pad3[3];
  REG16 sclh;                           // SCL Duty Cycle Register (high half word)
  REG16 _pad4;
  REG16 scll;                           // SCL Duty Cycle Register (low half word)
  REG16 _pad5;
  REG_8 conclr;                         // Control Clear Register
  REG_8 _pad6[3];
} i2cRegs_t;

#endif
