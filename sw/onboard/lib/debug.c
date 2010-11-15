#include "debug.h"
#include "comm.h"
#include "generated/messages.h"

CommChannel_t debug_chan = COMM_TELEMETRY;

void debug_uint8 (uint8_t i)
{
    MESSAGE_SEND_DEBUG_UINT8 (debug_chan, &i);
}

void debug_float (float f)
{
    MESSAGE_SEND_DEBUG_FLOAT (debug_chan, &f);
}

void debug_int32 (int32_t i)
{
    MESSAGE_SEND_DEBUG_INT32 (debug_chan, &i);
}
