#include "fms.h"
#include "rc.h"
#include "generated/messages.h"

FMS_t fms;
SystemStatus_t fms_system_status = STATUS_UNINITIAIZED;

void fms_init(void)
{
    fms.enabled_rc = FALSE;
    fms.enabled_msg = FALSE;
    fms_system_status = STATUS_INITIALIZED;
}

void fms_periodic_task(void)
{
    if (rc_status == RC_OK) {
        if (rc_values[RADIO_FMS] > 0)
            fms.enabled_rc = TRUE;
        else
            fms.enabled_rc = FALSE;
    } else {
        fms.enabled_rc = FALSE;
    }
}

void fms_set(CommMessage_t *message)
{
    if ( message->msgid == MESSAGE_ID_FMS_ATTITUDE ) {
        float r = MESSAGE_FMS_ATTITUDE_GET_FROM_BUFFER_roll(message->payload);
        float p = MESSAGE_FMS_ATTITUDE_GET_FROM_BUFFER_pitch(message->payload);
        float y = MESSAGE_FMS_ATTITUDE_GET_FROM_BUFFER_heading(message->payload);

        struct Int32Eulers att = {
            ANGLE_BFP_OF_REAL( r ),
            ANGLE_BFP_OF_REAL( p ),
            ANGLE_BFP_OF_REAL( y )
        };

        EULERS_COPY (fms.command.h_sp.attitude, att);

        fms.command.v_sp.direct = MESSAGE_FMS_ATTITUDE_GET_FROM_BUFFER_thrust(message->payload);
    }
}

bool_t fms_is_enabled(void)
{
    return fms.enabled_rc && fms.enabled_msg;
}

void fms_msg_enable(bool_t enabled)
{
    fms.enabled_msg = enabled;
}
