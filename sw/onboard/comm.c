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
    /* Counting STX, LENGTH, ACID, MSGID, CRC1 and CRC2 */
    uint8_t total_len = len + NUM_NON_PAYLOAD_BYTES;

    comm_status[chan].ck_a = STX;
    comm_status[chan].ck_b = STX;
    comm_send_ch(chan, STX);

    COMM_SEND_CH(chan, total_len);
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


#define UPDATE_CHECKSUM(_x)                                                 \
    comm_status[chan].rx_ck_a += _x;                                        \
    comm_status[chan].rx_ck_b += comm_status[chan].rx_ck_a;                 \

#define ADD_CHAR(_x)                                                        \
    comm_status[chan].pprz_payload[comm_status[chan].payload_idx] = _x;     \
    comm_status[chan].payload_idx++;

bool_t
comm_parse ( CommChannel_t chan )
{
    while ( comm_ch_available(chan) && !comm_status[chan].pprz_msg_received ) 
    {
        uint8_t c = comm_get_ch(chan);
        switch (comm_status[chan].parse_state) 
        {
            case STATE_UNINIT:
                if (c == STX) {
                    comm_status[chan].parse_state++;
                    comm_status[chan].rx_ck_a = STX;
                    comm_status[chan].rx_ck_b = STX;
                }
                break;
            case STATE_GOT_STX:
                if (comm_status[chan].pprz_msg_received) {
                    comm_status[chan].pprz_ovrn++;
                    goto error;
                }
                /* Counting STX, LENGTH, ACID, MSGID, CRC1 and CRC2 */
                comm_status[chan].pprz_payload_len = c - NUM_NON_PAYLOAD_BYTES; 
                comm_status[chan].payload_idx = 0;
                UPDATE_CHECKSUM(c)
                comm_status[chan].parse_state++;
                break;
            case STATE_GOT_LENGTH:
                comm_status[chan].acid = c;
                UPDATE_CHECKSUM(c)
                comm_status[chan].parse_state++;
                break;
            case STATE_GOT_ACID:
                comm_status[chan].msgid = c;
                UPDATE_CHECKSUM(c)
                if (comm_status[chan].pprz_payload_len == 0)
                    comm_status[chan].parse_state = STATE_GOT_PAYLOAD;
                else
                    comm_status[chan].parse_state++;
                break;
            case STATE_GOT_MSGID:
                ADD_CHAR(c)
                UPDATE_CHECKSUM(c)
                if (comm_status[chan].payload_idx == comm_status[chan].pprz_payload_len)
                    comm_status[chan].parse_state++;
                break;
            case STATE_GOT_PAYLOAD:
                if (c != comm_status[chan].rx_ck_a)
                    goto error;
                comm_status[chan].parse_state++;
                break;
            case STATE_GOT_CRC1:
                if (c != comm_status[chan].rx_ck_b)
                    goto error;
                /* Successfully got message */
                comm_status[chan].pprz_msg_received = TRUE;
                comm_message[chan].len = comm_status[chan].pprz_payload_len;
                comm_message[chan].acid = comm_status[chan].acid;
                comm_message[chan].msgid = comm_status[chan].msgid;
                comm_message[chan].buffer = comm_status[chan].pprz_payload;
                goto restart;
        }
        break;
        error:
            comm_status[chan].pprz_error++;
        restart:
            comm_status[chan].parse_state = STATE_UNINIT;
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
        comm_status[chan].pprz_msg_received = FALSE;
    }
    else
        ret = FALSE;

    return ret;
}

void
comm_periodic_task ( CommChannel_t chan )
{
    static uint8_t u8 = 1;
    static uint8_t i8 = -1;
    static uint16_t u16 = 10;
    static int16_t i16 = -10;
    static uint32_t u32 = 100;
    static int32_t i32 = -100;
    static float f = 1.0;

/*
#include "periodic.h"
#define Booz2TelemetryPeriodic() {		\
    PeriodicSendMain();				\
  }
*/
//    MESSAGE_SEND_PONG();
    MESSAGE_SEND_COMM_STATUS( &comm_status[chan].pprz_ovrn, &comm_status[chan].pprz_error );
    MESSAGE_SEND_TEST_MESSAGE ( &u8, &i8, &u16, &i16, &u32, &i32, &f );


    u8 += 1;
    i8 -= 1;
    u16 += 10;
    i16 -= 10;
    u32 += 100;
    i32 -= 100;
    f += 15.0;

}
						

