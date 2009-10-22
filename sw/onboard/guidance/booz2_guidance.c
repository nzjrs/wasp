#include "guidance.h"
#include "booz2_guidance_h.h"
#include "booz2_guidance_v.h"

void guidance_init(void)
{
    booz2_guidance_h_init();
    booz2_guidance_v_init();
}
