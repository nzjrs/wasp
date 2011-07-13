#include "rc.h"
#include "bomb.h"
#include "actuators.h"

#include "generated/settings.h"

typedef struct {
    uint8_t rc_channel;
    pprz_t  rc_lt_val;
    uint8_t servo_id;
    uint8_t is_dropping;    /* 0 when the bomb is held, !=0 otherwise */
} BombState_t;

BombState_t bombstate;

void bomb_init_servo(uint8_t rc_channel, pprz_t rc_lt_val, uint8_t servo_id)
{
    bombstate.rc_channel = rc_channel;
    bombstate.rc_lt_val = rc_lt_val;
    bombstate.servo_id = servo_id;
    bombstate.is_dropping = 0;

    actuators_init(ACTUATOR_BANK_SERVOS);
    actuators_set(ACTUATOR_BANK_SERVOS | bombstate.servo_id, BOMB_HOLD_VALUE);
    actuators_commit(ACTUATOR_BANK_SERVOS);
}

void bomb_drop(void)
{
    bombstate.is_dropping = BOMB_PERIODIC_TICKS;
    actuators_set(ACTUATOR_BANK_SERVOS | bombstate.servo_id, BOMB_RELEASE_VALUE);
    actuators_commit(ACTUATOR_BANK_SERVOS);
}

void bomb_periodic_task(void)
{
    if (rc_status == RC_OK) {
        if (rc_values[bombstate.rc_channel] < bombstate.rc_lt_val)
            bomb_drop();
    }

    if (bombstate.is_dropping == 0) {
        actuators_set(ACTUATOR_BANK_SERVOS | bombstate.servo_id, BOMB_HOLD_VALUE);
        actuators_commit(ACTUATOR_BANK_SERVOS);
    } else {
        bombstate.is_dropping -= 1;
    }
}

