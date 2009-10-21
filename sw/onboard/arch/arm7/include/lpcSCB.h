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
#ifndef INC_LPC_SCB_H
#define INC_LPC_SCB_H

// System Control Block Registers
typedef struct
{
  // Memory Accelerator Module Registers (MAM)
  struct
    {
    REG_8 cr;                           // Control Register
    REG_8 _pad0[3];
    REG_8 tim;                          // Timing Control Register
    REG32 _pad1[14];
    } mam;

  // Memory Mapping Control Register
  REG_8 memmap;
  REG32 _pad0[15];

  // Phase Locked Loop Registers (PLL)
  struct
    {
    REG_8 con;                          // Control Register
    REG_8 _pad0[3];
    REG_8 cfg;                          // Configuration Register
    REG_8 _pad1[3];
    REG16 stat;                         // Status Register
    REG16 _pad2;
    REG_8 feed;                         // Feed Register
    REG32 _pad3[12];
    } pll;

  // Power Control Registers
  struct
    {
    REG_8 con;                          // Control Register
    REG_8 _pad0[3];
    REG32 conp;                         // Peripherals Register
    REG32 _pad1[14];
    } p;

  // VPB Divider Register
  REG_8 vpbdiv;
  REG32 _pad1[15];

  // External Interrupt Registers
  struct
    {
    REG_8 flag;                         // Flag Register
    REG_8 _pad0[3];
    REG_8 wake;                         // Wakeup Register
    REG_8 _pad1[3];
    REG_8 mode;                         // Mode Register
    REG_8 _pad2[3];
    REG_8 polar;                        // Polarity Register
    REG32 _pad3[12];
    } ext;
} scbRegs_t;


///////////////////////////////////////////////////////////////////////////////
// MAM defines
#define MAMCR_OFF     0
#define MAMCR_PART    1
#define MAMCR_FULL    2

#define MAMTIM_CYCLES (((CCLK) + 19999999) / 20000000)

///////////////////////////////////////////////////////////////////////////////
// MEMMAP defines
#define MEMMAP_BBLK   0                 // Interrupt Vectors in Boot Block
#define MEMMAP_FLASH  1                 // Interrupt Vectors in Flash
#define MEMMAP_SRAM   2                 // Interrupt Vectors in SRAM

///////////////////////////////////////////////////////////////////////////////
// PLL defines & computations
// Compute the value of PLL_DIV and test range validity
// FOSC & PLL_MUL should be defined in project configuration file (config.h)
#ifndef CCLK
#define CCLK          (FOSC * PLL_MUL)  // CPU Clock Freq.
#endif

#define FCCO_MAX      (320000000)       // Max CC Osc Freq.
#define PLL_DIV       (FCCO_MAX / (2 * CCLK)) // PLL Divider
#define FCCO          (FOSC * PLL_MUL * 2 * PLL_DIV) // CC Osc. Freq.

// PLLCON Register Bit Definitions
#define PLLCON_PLLE   (1 << 0)          // PLL Enable
#define PLLCON_PLLC   (1 << 1)          // PLL Connect

// PLLCFG Register Bit Definitions
#define PLLCFG_MSEL   ((PLL_MUL - 1) << 0) // PLL Multiplier
#define PLLCFG_PSEL   ((PLL_DIV - 1) << 5) // PLL Divider

// PLLSTAT Register Bit Definitions
#define PLLSTAT_LOCK  (1 << 10)         // PLL Lock Status Bit

///////////////////////////////////////////////////////////////////////////////
// VPBDIV defines & computations
#define VPBDIV_VALUE  (PBSD_BITS & 0x03)     // VPBDIV value

#endif
