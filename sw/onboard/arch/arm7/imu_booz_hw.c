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
#include "std.h"

#include "config/config.h"
#include "generated/settings.h"

#include "imu.h"
#include "arm7/armVIC.h"
#include "arm7/imu_booz_hw.h"
#include "arm7/max1168.h"
#include "arm7/micromag.h"

typedef enum {
    SPI_NONE,
    SPI_SLAVE_MAX1168,
    SPI_SLAVE_MM
} ImuSelected_t;

uint8_t         do_max1168_read;
uint8_t         imu_spi_selected;
IMU_t           booz_imu;

static void         SSP_ISR(void) __attribute__((naked));
static inline void  imu_scale_gyro(void);
static inline void  imu_scale_accel(void);
static inline void  imu_scale_mag(void);

void 
imu_init(void)
{
    /* initialises neutrals */
    RATES_ASSIGN(booz_imu.gyro_neutral,  IMU_NEUTRAL_GYRO_P,  IMU_NEUTRAL_GYRO_Q,  IMU_NEUTRAL_GYRO_R);
    VECT3_ASSIGN(booz_imu.accel_neutral, IMU_NEUTRAL_ACCEL_X, IMU_NEUTRAL_ACCEL_Y, IMU_NEUTRAL_ACCEL_Z);
    VECT3_ASSIGN(booz_imu.mag_neutral,   IMU_NEUTRAL_MAG_X,   IMU_NEUTRAL_MAG_Y,   IMU_NEUTRAL_MAG_Z);

    /* initialise IMU alignment */
    imu_adjust_alignment(IMU_ALIGNMENT_BODY_TO_IMU_PHI, IMU_ALIGNMENT_BODY_TO_IMU_THETA, IMU_ALIGNMENT_BODY_TO_IMU_PSI);

    imu_spi_selected = SPI_NONE;
    do_max1168_read = FALSE;

    /* setup pins for SSP (SCK, MISO, MOSI) */
    PINSEL1 |= SSP_PINSEL1_SCK  | SSP_PINSEL1_MISO | SSP_PINSEL1_MOSI;

    /* setup SSP */
    SSPCR0 = SSPCR0_VAL;;
    SSPCR1 = SSPCR1_VAL;
    SSPCPSR = 0x02;

    /* initialize interrupt vector */
    VICIntSelect &= ~VIC_BIT( VIC_SPI1 );  /* SPI1 selected as IRQ */
    VICIntEnable = VIC_BIT( VIC_SPI1 );    /* enable it            */
    _VIC_CNTL(SSP_VIC_SLOT) = VIC_ENABLE | VIC_SPI1;
    _VIC_ADDR(SSP_VIC_SLOT) = (uint32_t)SSP_ISR;      /* address of the ISR   */

    max1168_init();
    micromag_init();
}

static void SSP_ISR(void) {
    ISR_ENTRY();

    switch (imu_spi_selected) 
    {
        case SPI_SLAVE_MAX1168:
            max1168_got_interrupt_retrieve_values();
            imu_spi_selected = SPI_NONE;
            break;
        case SPI_SLAVE_MM:
            micromag_got_interrupt_retrieve_values();
            if (micromag_status == MM_DATA_AVAILABLE)
                imu_spi_selected = SPI_NONE;
            break;
    }

    VICVectAddr = 0x00000000; /* clear this interrupt from the VIC */
    ISR_EXIT();
}

uint8_t
imu_event_task(void)
{
    uint8_t valid = 0;

    if ( max1168_event() )
    {
        valid = IMU_ACC | IMU_GYR;

        booz_imu.gyro_unscaled.p = max1168_values[IMU_GYRO_P_CHAN];
        booz_imu.gyro_unscaled.q = max1168_values[IMU_GYRO_Q_CHAN];
        booz_imu.gyro_unscaled.r = max1168_values[IMU_GYRO_R_CHAN];
        booz_imu.accel_unscaled.x = max1168_values[IMU_ACCEL_X_CHAN];
        booz_imu.accel_unscaled.y = max1168_values[IMU_ACCEL_Y_CHAN];
        booz_imu.accel_unscaled.z = max1168_values[IMU_ACCEL_Z_CHAN];

        imu_scale_gyro();
        imu_scale_accel();

        max1168_reset();
    }

    if (do_max1168_read && imu_spi_selected == SPI_NONE) 
    {
        Booz2ImuSetSpi16bits();
        imu_spi_selected = SPI_SLAVE_MAX1168;
        do_max1168_read = FALSE;

        max1168_read();
    }
    if (do_micromag_read && imu_spi_selected == SPI_NONE) 
    {
        Booz2ImuSetSpi8bits();
        imu_spi_selected = SPI_SLAVE_MM;
        do_micromag_read = FALSE;
    }
    if (imu_spi_selected == SPI_SLAVE_MM)
        micromag_read();


    if ( micromag_event() )
    {
        valid |= IMU_MAG;

        booz_imu.mag_unscaled.x = micromag_values[IMU_MAG_X_CHAN];
        booz_imu.mag_unscaled.y = micromag_values[IMU_MAG_Y_CHAN];
        booz_imu.mag_unscaled.z = micromag_values[IMU_MAG_Z_CHAN];

        imu_scale_mag();

        micromag_reset();
    }

    return valid;
}

void
imu_periodic_task(void)
{

    RunOnceEvery(10, {
        micromag_schedule_read();
    });


    do_max1168_read = TRUE;

}

void
imu_adjust_alignment( float phi, float theta, float psi )
{
    booz_imu.body_to_imu_phi = phi;
    booz_imu.body_to_imu_theta = theta;
    booz_imu.body_to_imu_psi = psi;

    /*
    Compute quaternion and rotation matrix
    for conversions between body and imu frame
    */
    struct booz_ieuler body_to_imu_eulers = {
            ANGLE_BFP_OF_REAL(RadOfDeg(phi)),
            ANGLE_BFP_OF_REAL(RadOfDeg(theta)),
            ANGLE_BFP_OF_REAL(RadOfDeg(psi))
    };

    INT32_QUAT_OF_EULERS(booz_imu.body_to_imu_quat, body_to_imu_eulers);
    INT32_QUAT_NORMALISE(booz_imu.body_to_imu_quat);
    INT32_RMAT_OF_EULERS(booz_imu.body_to_imu_rmat, body_to_imu_eulers);
}

static inline void
imu_scale_gyro(void)
{
    RATES_COPY(booz_imu.gyro_prev, booz_imu.gyro);
    booz_imu.gyro.p = ((booz_imu.gyro_unscaled.p - booz_imu.gyro_neutral.p)*IMU_SENS_GYRO_P_NUM)/IMU_SENS_GYRO_P_DEN;
    booz_imu.gyro.q = ((booz_imu.gyro_unscaled.q - booz_imu.gyro_neutral.q)*IMU_SENS_GYRO_Q_NUM)/IMU_SENS_GYRO_Q_DEN;
    booz_imu.gyro.r = ((booz_imu.gyro_unscaled.r - booz_imu.gyro_neutral.r)*IMU_SENS_GYRO_R_NUM)/IMU_SENS_GYRO_R_DEN;
}

static inline void
imu_scale_accel(void)
{
    VECT3_COPY(booz_imu.accel_prev, booz_imu.accel);
    booz_imu.accel.x = ((booz_imu.accel_unscaled.x - booz_imu.accel_neutral.x)*IMU_SENS_ACCEL_X_NUM)/IMU_SENS_ACCEL_X_DEN;
    booz_imu.accel.y = ((booz_imu.accel_unscaled.y - booz_imu.accel_neutral.y)*IMU_SENS_ACCEL_Y_NUM)/IMU_SENS_ACCEL_Y_DEN;
    booz_imu.accel.z = ((booz_imu.accel_unscaled.z - booz_imu.accel_neutral.z)*IMU_SENS_ACCEL_Z_NUM)/IMU_SENS_ACCEL_Z_DEN;
}

static inline void
imu_scale_mag(void)
{
    booz_imu.mag.x = ((booz_imu.mag_unscaled.x - booz_imu.mag_neutral.x) * IMU_SENS_MAG_X_NUM) / IMU_SENS_MAG_X_DEN;
    booz_imu.mag.y = ((booz_imu.mag_unscaled.y - booz_imu.mag_neutral.y) * IMU_SENS_MAG_Y_NUM) / IMU_SENS_MAG_Y_DEN;
    booz_imu.mag.z = ((booz_imu.mag_unscaled.z - booz_imu.mag_neutral.z) * IMU_SENS_MAG_Z_NUM) / IMU_SENS_MAG_Z_DEN;
}
