#ifndef _GUIDANCE_H_
#define _GUIDANCE_H_

#include "std.h"

#define BOOZ2_GUIDANCE_H_MODE_KILL      0
#define BOOZ2_GUIDANCE_H_MODE_RATE      1
#define BOOZ2_GUIDANCE_H_MODE_ATTITUDE  2
#define BOOZ2_GUIDANCE_H_MODE_HOVER     3
#define BOOZ2_GUIDANCE_H_MODE_NAV       4

#define BOOZ2_GUIDANCE_V_MODE_KILL      0
#define BOOZ2_GUIDANCE_V_MODE_RC_DIRECT 1
#define BOOZ2_GUIDANCE_V_MODE_RC_CLIMB  2
#define BOOZ2_GUIDANCE_V_MODE_CLIMB     3
#define BOOZ2_GUIDANCE_V_MODE_HOVER     4
#define BOOZ2_GUIDANCE_V_MODE_NAV       5

extern uint8_t booz2_guidance_h_mode;
extern uint8_t booz2_guidance_v_mode;

void guidance_init(void);

#endif /* _GUIDANCE_H_ */
