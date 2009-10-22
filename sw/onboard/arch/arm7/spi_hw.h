/*
 * Copyright (C) 2003-2005  Pascal Brisset, Antoine Drouin
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

/** \brief handling of arm7 SPI hardware
 *  for now only SPI1 ( aka SSP )
 */

#ifndef SPI_HW_H
#define SPI_HW_H

#include "std.h"
#include "LPC21xx.h"
#include "config/config.h"

#define SpiEnable() {		\
    SetBit(SSPCR1, SSE);	\
  }

#define SpiDisable() {		\
    ClearBit(SSPCR1, SSE);	\
  }

#define SpiEnableRti() {	\
    SetBit(SSPIMSC, RTIM);	\
  }

#define SpiDisableRti() {	\
    ClearBit(SSPIMSC, RTIM);	\
  }

#define SpiClearRti() {         \
    SetBit(SSPICR, RTIC);	\
  }

#define SpiEnableTxi() {	\
    SetBit(SSPIMSC, TXIM);	\
  }

#define SpiDisableTxi() {	\
    ClearBit(SSPIMSC, TXIM);	\
  }

#define SpiEnableRxi() {	\
    SetBit(SSPIMSC, RXIM);	\
  }

#define SpiDisableRxi() {	\
    ClearBit(SSPIMSC, RXIM);	\
  }

#define SpiSend(a) {            \
    SSPDR = a;			\
  }

#define SpiRead() SSPDR;

#endif /* SPI_HW_H */
