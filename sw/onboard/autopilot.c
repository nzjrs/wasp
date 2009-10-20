#include "autopilot.h"
#include "generated/settings.h"

#define TRESHOLD_1_PPRZ (MIN_PPRZ / 2)
#define TRESHOLD_2_PPRZ (MAX_PPRZ / 2)

uint8_t autopilot_mode_auto2;

uint8_t autopilot_mode_of_radio(pprz_t rc)
{
    if (rc > TRESHOLD_2_PPRZ)
        return autopilot_mode_auto2;
    else if (rc > TRESHOLD_1_PPRZ)
        return AUTOPILOT_MODE_AUTO1;
    else
        return AUTOPILOT_MODE_MANUAL;

}

