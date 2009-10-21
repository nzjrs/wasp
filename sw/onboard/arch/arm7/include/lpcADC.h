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
#ifndef INC_LPC_ADC_H
#define INC_LPC_ADC_H

// A/D Converter Registers
typedef struct
{
  REG32 cr;                           // Control Register
  REG32 gdr;                          // Global Data Register
  REG32 gsr;                          // Global Start Register
  REG32 inten;                        // Interrupt Enable Register
  REG32 dr0;                          // Channel 0 Data Register
  REG32 dr1;                          // Channel 1 Data Register
  REG32 dr2;                          // Channel 2 Data Register
  REG32 dr3;                          // Channel 3 Data Register
  REG32 dr4;                          // Channel 4 Data Register
  REG32 dr5;                          // Channel 5 Data Register
  REG32 dr6;                          // Channel 6 Data Register
  REG32 dr7;                          // Channel 7 Data Register
  REG32 stat;                         // Status Register
} adcRegs_t;

#endif
