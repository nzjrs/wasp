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
#ifndef LPC_CAN_H
#define LPC_CAN_H

typedef struct
{
  REG32 afmr;
  REG32 sff_sa;
  REG32 sff_grp_sa;
  REG32 eff_sa;
  REG32 eff_grp_sa;
  REG32 end_of_table;
  REG32 lut_err_ad;
  REG32 lut_err_reg;
} can_accept_Regs_t;


typedef struct
{
  REG32 tx_sr;
  REG32 rx_sr;
  REG32 m_sr;
} can_central_Regs_t;



typedef struct
{
  REG32 can_mod;
  REG32 can_cmr;
  REG32 can_gsr;
  REG32 can_icr;
  REG32 can_ier;
  REG32 can_btr;
  REG32 can_ewl;
  REG32 can_sr;
  REG32 can_rfs;
  REG32 can_rid;
  REG32 can_rda;
  REG32 can_rdb;
  REG32 can_tfi1;
  REG32 can_tid1;
  REG32 can_tda1;
  REG32 can_tdb1;
  REG32 can_tfi2;
  REG32 can_tid2;
  REG32 can_tda2;
  REG32 can_tdb2;
  REG32 can_tfi3;
  REG32 can_tid3;
  REG32 can_tda3;
  REG32 can_tdb3;
} can_Regs_t;


#endif /* LPC_CAN_H */


