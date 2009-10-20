#ifndef AUTOPILOT_H
#define AUTOPILOT_H

#include "std.h"

#define BOOZ2_AP_MODE_FAILSAFE          0
#define BOOZ2_AP_MODE_KILL              1
#define BOOZ2_AP_MODE_RATE_DIRECT       2
#define BOOZ2_AP_MODE_ATTITUDE_DIRECT   3
#define BOOZ2_AP_MODE_RATE_RC_CLIMB     4
#define BOOZ2_AP_MODE_ATTITUDE_RC_CLIMB 5
#define BOOZ2_AP_MODE_ATTITUDE_CLIMB    6
#define BOOZ2_AP_MODE_RATE_Z_HOLD       7
#define BOOZ2_AP_MODE_ATTITUDE_Z_HOLD   8
#define BOOZ2_AP_MODE_HOVER_DIRECT      9
#define BOOZ2_AP_MODE_HOVER_CLIMB       10
#define BOOZ2_AP_MODE_HOVER_Z_HOLD      11
#define BOOZ2_AP_MODE_NAV               12

extern uint8_t      autopilot_mode;
extern uint8_t      autopilot_mode_auto2;
extern bool_t       autopilot_motors_on;
extern bool_t       autopilot_in_flight;
extern uint32_t     autopilot_motors_on_counter;
extern uint32_t     autopilot_in_flight_counter;

uint8_t
autopilot_mode_of_radio(pprz_t mode_channel);

/* Implementations must provide these */
void
autopilot_init(void);

void
autopilot_periodic(void);

void
autopilot_on_rc_event(void);

void
autopilot_set_mode(uint8_t new_autopilot_mode);

void
autopilot_set_actuators(void);

#endif /* AUTOPILOT_H */
