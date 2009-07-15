#include "std.h"

#include "config/config.h"
#include "config/airframe.h"

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

static void     SSP_ISR(void) __attribute__((naked));

void 
imu_init(void)
{
    /* initialises neutrals */
    RATES_ASSIGN(booz_imu.gyro_neutral,  IMU_GYRO_P_NEUTRAL,  IMU_GYRO_Q_NEUTRAL,  IMU_GYRO_R_NEUTRAL);
    VECT3_ASSIGN(booz_imu.accel_neutral, IMU_ACCEL_X_NEUTRAL, IMU_ACCEL_Y_NEUTRAL, IMU_ACCEL_Z_NEUTRAL);
    VECT3_ASSIGN(booz_imu.mag_neutral,   IMU_MAG_X_NEUTRAL,   IMU_MAG_Y_NEUTRAL,   IMU_MAG_Z_NEUTRAL);

    /*
    Compute quaternion and rotation matrix
    for conversions between body and imu frame
    */
    struct booz_ieuler body_to_imu_eulers = {IMU_BODY_TO_IMU_PHI, IMU_BODY_TO_IMU_THETA, IMU_BODY_TO_IMU_PSI};
    INT32_QUAT_OF_EULERS(booz_imu.body_to_imu_quat, body_to_imu_eulers);
    INT32_QUAT_NORMALISE(booz_imu.body_to_imu_quat);
    INT32_RMAT_OF_EULERS(booz_imu.body_to_imu_rmat, body_to_imu_eulers);

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

        Booz2ImuScaleGyro();
        Booz2ImuScaleAccel();

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

        Booz2ImuScaleMag();

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


