#ifndef I2C_HW_H
#define I2C_HW_H

#include "LPC21xx.h"
#include "std.h"
#include "config/config.h"
#include "interrupt_hw.h"

#define I2C_BUF_LEN     16
#define I2C1_BUF_LEN    16

/**
 * Callback for when the I2C state machine reaches the STOP state
 */
typedef void (*I2cStopCallback_t)(void);

#if USE_I2C0

extern volatile uint8_t i2c_status;
extern volatile uint8_t i2c_buf[I2C_BUF_LEN];
extern volatile I2cStopCallback_t i2c_stop_callback;

void i2c_init(void);
void i2c_receive(uint8_t slave_addr, uint8_t len, volatile bool_t* finished);
void i2c_transmit(uint8_t slave_addr, uint8_t len, volatile bool_t* finished);

#endif  /* USE_I2C1 */

#if USE_I2C1

extern volatile uint8_t i2c1_status;
extern volatile uint8_t i2c1_buf[I2C1_BUF_LEN];
extern volatile I2cStopCallback_t i2c1_stop_callback;

void i2c1_init(void);
void i2c1_receive(uint8_t slave_addr, uint8_t len, volatile bool_t* finished);
void i2c1_transmit(uint8_t slave_addr, uint8_t len, volatile bool_t* finished);

#endif /* USE_I2C1 */

#endif /* I2C_HW_H */
