#include "debug.h"
#include "comm.h"
#include "generated/messages.h"

void debug_int (CommChannel_t chan, uint8_t i)
{
    MESSAGE_SEND_DEBUG (chan, &i);
}

void debug_float (CommChannel_t chan, float f)
{
    MESSAGE_SEND_DEBUG_FLOAT (chan, &f);
}
