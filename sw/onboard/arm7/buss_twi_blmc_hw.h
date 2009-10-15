#ifndef BUSS_TWI_BLMC_HW_H
#define BUSS_TWI_BLMC_HW_H

#include "std.h"

#define BUSS_TWI_BLMC_NB    4
#define BUSS_BLMC_ADDR      {0x52, 0x54, 0x56, 0x58}

extern uint8_t buss_twi_blmc_motor_power[BUSS_TWI_BLMC_NB];

void buss_twi_blmc_init(void);

void buss_twi_blmc_commit(void);

#endif /* BUSS_TWI_BLMC_HW_H */
