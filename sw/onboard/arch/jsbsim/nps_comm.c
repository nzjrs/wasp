#include "std.h"
#include "comm.h"

#include "lib/comm_fifo.h"

SystemStatus_t comm_system_status = STATUS_UNINITIAIZED;

static bool_t check_chan ( CommChannel_t chan )
{
    return ((chan == COMM_TELEMETRY) && (comm_system_status == STATUS_INITIALIZED));
}

void comm_init ( CommChannel_t chan )
{
    /* make sure to do this once */
    if (comm_system_status == STATUS_UNINITIAIZED) {
        int i;
        for (i = 0; i < COMM_NB; i++) {
            comm_callback_rx[i] = 0;
            comm_callback_tx[i] = 0;
        
            comm_status[i].parse_state = STATE_UNINIT;
            comm_status[i].msg_received = FALSE;
            comm_status[i].buffer_overrun = 0;
            comm_status[i].parse_error = 0;

            comm_channel_used[i] = FALSE;
        }
    }

    if (chan == COMM_TELEMETRY) {
        if ( comm_fifo_init () ) {
            comm_system_status = STATUS_INITIALIZED;
            comm_channel_used[chan] = TRUE;
        } else {
            comm_system_status = STATUS_FAIL;
        }
    }
}

bool_t comm_ch_available ( CommChannel_t chan )
{
    if ( check_chan() )
        return comm_fifo_ch_available ();
    return FALSE;
}

void comm_send_ch (CommChannel_t chan, uint8_t c)
{
    if ( check_chan() )
        comm_fifo_send_ch (c);
}

uint8_t comm_get_ch(CommChannel_t chan)
{
    if ( check_chan() )
        return comm_fifo_get_ch ();
    return '\0';
}

bool_t  comm_check_free_space ( CommChannel_t chan, uint8_t len ) { return TRUE; }
void    comm_overrun ( CommChannel_t chan ) {}
void    comm_start_message_hw ( void ) {}
void    comm_end_message_hw ( void ) {}

