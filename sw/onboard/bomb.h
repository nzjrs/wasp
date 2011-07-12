#ifndef BOMB_H
#define BOMB_H

#include "std.h"

void bomb_init_servo(uint8_t rc_channel, pprz_t rc_gt_val, uint8_t servo_id);
void bomb_drop(void);
void bomb_periodic_task(void);

#endif /* BOMB_H */
