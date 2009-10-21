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
#ifndef _BOOZ_IMU_BABY_H_
#define _BOOZ_IMU_BABY_H_

/* Pin allocations for channels */
#define IMU_GYRO_P_CHAN     1
#define IMU_GYRO_Q_CHAN     0
#define IMU_GYRO_R_CHAN     2
#define IMU_ACCEL_X_CHAN    3
#define IMU_ACCEL_Y_CHAN    5
#define IMU_ACCEL_Z_CHAN    6
#define IMU_MAG_X_CHAN      0
#define IMU_MAG_Y_CHAN      1
#define IMU_MAG_Z_CHAN      2

/* SSPCR0 settings */
#define SSP_DDS  0x0F << 0  /* data size         : 16 bits        */
#define SSP_FRF  0x00 << 4  /* frame format      : SPI           */
#define SSP_CPOL 0x00 << 6  /* clock polarity    : data captured on first clock transition */  
#define SSP_CPHA 0x00 << 7  /* clock phase       : SCK idles low */
#define SSP_SCR  0x0F << 8  /* serial clock rate : divide by 16  */

/* SSPCR1 settings */
#define SSP_LBM  0x00 << 0  /* loopback mode     : disabled                  */
#define SSP_SSE  0x00 << 1  /* SSP enable        : disabled                  */
#define SSP_MS   0x00 << 2  /* master slave mode : master                    */
#define SSP_SOD  0x00 << 3  /* slave output disable : don't care when master */

#define SSPCR0_VAL (SSP_DDS |  SSP_FRF | SSP_CPOL | SSP_CPHA | SSP_SCR )
#define SSPCR1_VAL (SSP_LBM |  SSP_SSE | SSP_MS | SSP_SOD )

#define SSP_PINSEL1_SCK  (2<<2)
#define SSP_PINSEL1_MISO (2<<4)
#define SSP_PINSEL1_MOSI (2<<6)

#define Booz2ImuSetSpi8bits() { \
  SSPCR0 &= (~(0xF << 0)); \
  SSPCR0 |= (0x07 << 0); /* data size : 8 bits */ \
}

#define Booz2ImuSetSpi16bits() { \
  SSPCR0 &= (~(0xF << 0)); \
  SSPCR0 |= (0x0F << 0); /* data size : 16 bits */ \
}

#endif /* _BOOZ_IMU_BABY_H_ */
