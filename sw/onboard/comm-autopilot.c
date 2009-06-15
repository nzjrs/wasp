#include "comm-autopilot.h"

#include "rc.h"
#include "gps.h"

bool_t
comm_autopilot_send ( CommChannel_t chan, uint8_t msgid )
{
    uint8_t ret = TRUE;

    switch (msgid)
    {
        case MESSAGE_ID_WASP_GPS:
            MESSAGE_SEND_WASP_GPS( chan, &booz_gps_state.fix, &booz_gps_state.num_sv );
            break;
        default:
            ret = FALSE;
            break;
    }
            

    return ret;
/*
extern pprz_t   rc_values[RADIO_CTL_NB];
extern uint8_t  rc_status;
extern int32_t  avg_rc_values[RADIO_CTL_NB];
extern uint8_t  rc_values_contains_avg_channels;

extern uint8_t  time_since_last_ppm;
extern uint8_t  ppm_cpt, last_ppm_cpt;
extern uint16_t ppm_pulses[RADIO_CTL_NB];
extern bool_t   ppm_valid;
*/

}

