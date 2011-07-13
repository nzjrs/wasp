#ifndef BOMB_H
#define BOMB_H

#include "std.h"

/**
 * initialises the bomb system to watch the specified rc channel, and when it
 * meets the condition, release the bomb actuating the supplied servo
 *
 * @param rc_channel the RC channel to watch, name from radio.xml
 * @param rc_lt_val when the RC channel is less than this value the bomb is dropped
 * @param servo_id the ID of the actuator connected to the bomb.
 */
void bomb_init_servo(uint8_t rc_channel, pprz_t rc_lt_val, uint8_t servo_id);

/**
 * drops the bomb immediately, latches, so one only needs to call this once
 */
void bomb_drop(void);

/**
 * To be called at periodic frequency. Backend dependant
 */
void bomb_periodic_task(void);

#endif /* BOMB_H */
