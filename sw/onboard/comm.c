#include "comm.h"
#include "generated/messages.h"

CommMessageCallback_t    comm_callback[COMM_NB];
CommMessage_t            comm_message[COMM_NB];
CommStatus_t             comm_status[COMM_NB];
bool_t                   comm_channel_used[COMM_NB];

#define COMM_SEND_CH(_chan, _byte) {                    \
    comm_status[_chan].ck_a += _byte;	                \
    comm_status[_chan].ck_b += comm_status[_chan].ck_a;	\
    comm_send_ch(_chan, _byte);		                    \
}

#define DownlinkStartMessage(_n, _id, _len) comm_start_message(chan, _id, _len);
#define DownlinkCheckFreeSpace(_len) comm_check_free_space(chan, _len)
#define DownlinkEndMessage() comm_end_message(chan);
#define DownlinkOverrun() comm_status[chan].pprz_ovrn++;
#define DownlinkPutUint8(_ch) COMM_SEND_CH(chan, _ch);

void
comm_start_message ( CommChannel_t chan, uint8_t id, uint8_t len )
{
    comm_send_ch(chan, STX);
    comm_status[chan].ck_a = len;
    comm_status[chan].ck_b = len;
    COMM_SEND_CH(chan, len + 4 /*STX,LEN,CK_A,CK_B*/ + 2 /* ACID, MSGID */);
    COMM_SEND_CH(chan, ACID);
    COMM_SEND_CH(chan, id);
}

void
comm_end_message ( CommChannel_t chan )
{
    comm_send_ch(chan, comm_status[chan].ck_a);
    comm_send_ch(chan, comm_status[chan].ck_b);
}

void
comm_send_message ( CommChannel_t chan, CommMessage_t *message )
{
    uint8_t i;

    comm_send_ch(chan, STX);
    comm_send_ch(chan, message->len + 4);
    comm_send_ch(chan, message->acid);
    comm_send_ch(chan, message->msgid);

    for (i = 0; i < message->len; i++)
        comm_send_ch(chan, message->buffer[i]);

    comm_send_ch(chan, message->ck_a);
    comm_send_ch(chan, message->ck_b);
}

bool_t
comm_parse ( CommChannel_t chan )
{
    while ( comm_ch_available(chan) && !comm_status[chan].pprz_msg_received ) 
    {
        uint8_t c = comm_get_ch(chan);
        switch (comm_status[chan].pprz_status) 
        {
            case UNINIT:
                if (c == STX)
                    comm_status[chan].pprz_status++;
                break;
            case GOT_STX:
                if (comm_status[chan].pprz_msg_received) {
                    comm_status[chan].pprz_ovrn++;
                    goto error;
                }
                comm_status[chan].pprz_payload_len = c-4; /* Counting STX, LENGTH and CRC1 and CRC2 */
                comm_status[chan].rx_ck_a = comm_status[chan].rx_ck_b = c;
                comm_status[chan].pprz_status++;
                comm_status[chan].payload_idx = 0;
                break;
            case GOT_LENGTH:
                comm_status[chan].pprz_payload[comm_status[chan].payload_idx] = c;
                comm_status[chan].rx_ck_a += c; comm_status[chan].rx_ck_b += comm_status[chan].rx_ck_a;
                comm_status[chan].payload_idx++;
                if (comm_status[chan].payload_idx == comm_status[chan].pprz_payload_len)
                    comm_status[chan].pprz_status++;
                break;
            case GOT_PAYLOAD:
                if (c != comm_status[chan].rx_ck_a)
                    goto error;
                comm_status[chan].pprz_status++;
                break;
            case GOT_CRC1:
                if (c != comm_status[chan].rx_ck_b)
                    goto error;
                /* Successfully got message */
                comm_status[chan].pprz_msg_received = TRUE;
                comm_message[chan].len = comm_status[chan].pprz_payload_len;
                comm_message[chan].acid = comm_status[chan].pprz_payload[0];
                comm_message[chan].msgid = comm_status[chan].pprz_payload[1];
                comm_message[chan].buffer = &(comm_status[chan].pprz_payload[2]);
                goto restart;
        }
        break;
        error:
            comm_status[chan].pprz_error++;
        restart:
            comm_status[chan].pprz_status = UNINIT;
        break;
    }
    return comm_status[chan].pprz_msg_received;
}

bool_t
comm_event_task ( CommChannel_t chan ) 
{
/*

#define PprzBuffer() PprzLink(ChAvailable())
#define ReadPprzBuffer() { while (PprzLink(ChAvailable())&&!pprz_msg_received) parse_pprz(PprzLink(Getch())); }

#define DatalinkEvent() {			\
  if (PprzBuffer()) {				\
    ReadPprzBuffer();				\
    if (pprz_msg_received) {			\
      pprz_parse_payload();			\
      pprz_msg_received = FALSE;		\
    }						\
  }						\
  if (dl_msg_available) {			\
    dl_parse_msg();				\
    dl_msg_available = FALSE;			\
  }						\
}
*/
    uint8_t ret = TRUE;

    if ( comm_channel_used[chan] && comm_ch_available(chan) && comm_parse(chan) ) 
    {
        switch (comm_message[chan].msgid) 
        {
            case MESSAGE_ID_PONG:
                MESSAGE_SEND_PONG();
                break;
            case MESSAGE_ID_COMM_STATUS:
                MESSAGE_SEND_COMM_STATUS( &comm_status[chan].pprz_ovrn, &comm_status[chan].pprz_error )
                break;
            default:
                if (comm_callback[chan])
                    ret = comm_callback[chan](&comm_message[chan]);
                else
                    ret = FALSE;
                break;
        }
    }
    else
        ret = FALSE;

    return ret;
}

void
comm_periodic_task ( CommChannel_t chan )
{
/*
#include "periodic.h"
#define Booz2TelemetryPeriodic() {		\
    PeriodicSendMain();				\
  }
*/
//    MESSAGE_SEND_PONG();
    MESSAGE_SEND_COMM_STATUS( &comm_status[chan].pprz_ovrn, &comm_status[chan].pprz_error );
}
						

