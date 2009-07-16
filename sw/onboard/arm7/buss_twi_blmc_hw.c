#include "config/config.h"
#include "config/airframe.h"

#include "arm7/i2c_hw.h"
#include "arm7/buss_twi_blmc_hw.h"

#define BUSS_TWI_BLMC_STATUS_IDLE 0
#define BUSS_TWI_BLMC_STATUS_BUSY 1

uint8_t twi_blmc_nb_err;

uint8_t buss_twi_blmc_motor_power[BUSS_TWI_BLMC_NB];
volatile bool_t  buss_twi_blmc_status;
volatile bool_t  buss_twi_blmc_i2c_done;
volatile uint8_t buss_twi_blmc_idx;

const uint8_t buss_twi_blmc_addr[BUSS_TWI_BLMC_NB] = BUSS_BLMC_ADDR;

void buss_twi_blmc_next(void);

static inline void buss_twi_blmc_send(void)
{
    i2c_buf[0] = buss_twi_blmc_motor_power[buss_twi_blmc_idx];
    i2c_transmit(buss_twi_blmc_addr[buss_twi_blmc_idx], 1, &buss_twi_blmc_i2c_done);
}

void buss_twi_blmc_next(void)
{
    buss_twi_blmc_idx++;
    if (buss_twi_blmc_idx < BUSS_TWI_BLMC_NB) {
        buss_twi_blmc_send();
    }
    else {
        buss_twi_blmc_status = BUSS_TWI_BLMC_STATUS_IDLE;
    }
}

void buss_twi_blmc_init (void)
{
    uint8_t i;

    i2c_init();
    i2c_stop_callback = buss_twi_blmc_next;

    for (i=0; i<BUSS_TWI_BLMC_NB;i++)
        buss_twi_blmc_motor_power[i] = 0;

    buss_twi_blmc_status = BUSS_TWI_BLMC_STATUS_IDLE;
    twi_blmc_nb_err = 0;
    buss_twi_blmc_i2c_done = TRUE;
}

void buss_twi_blmc_commit(void)
{
    if ( buss_twi_blmc_status == BUSS_TWI_BLMC_STATUS_IDLE) 
    {
        buss_twi_blmc_idx = 0;
        buss_twi_blmc_status = BUSS_TWI_BLMC_STATUS_BUSY;
        buss_twi_blmc_send();
    }
    else
    {
        twi_blmc_nb_err++;
    }
}
