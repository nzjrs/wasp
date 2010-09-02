#include "fms.h"
#include "rc.h"

FMS_t fms;
SystemStatus_t fms_system_status = STATUS_UNINITIAIZED;

void fms_init(void)
{
    fms.enabled = FMS_OFF;
    fms_system_status = STATUS_INITIALIZED;
}

void fms_periodic_task(void)
{
    if (rc_status == RC_OK) {
        if (rc_values[RADIO_FMS] > 0)
            fms.enabled = FMS_RC_ENABLED;
        else
            fms.enabled = FMS_OFF;
    } else {
        fms.enabled = FMS_OFF;
    }
}
