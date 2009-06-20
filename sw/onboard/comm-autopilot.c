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
        case MESSAGE_ID_STATUS:
            MESSAGE_SEND_STATUS(chan, &rc_status, &booz_gps_state.fix );
            break;
        default:
            ret = FALSE;
            break;
    }
            

    return ret;
}

