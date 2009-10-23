#include "guidance.h"
#include "fixedwing_guidance.h"

uint8_t booz2_guidance_h_mode;
uint8_t booz2_guidance_v_mode;

void guidance_init(void)
{
    booz2_guidance_h_mode = 0;
    booz2_guidance_v_mode = 0;
}

void guidance_fixedwing_run(int32_t autopilot_commands[])
{
    ;
}
