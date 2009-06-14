/*
 * vim: ai ts=4 sts=4 et sw=4
 */

#include "comm.h"

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
#define DownlinkOverrun() comm_status[chan].buffer_overrun++;
#define DownlinkPutUint8(_ch) COMM_SEND_CH(chan, _ch);

void
comm_start_message ( CommChannel_t chan, uint8_t id, uint8_t len )
{
    /* Counting STX, LENGTH, ACID, MSGID, CRC1 and CRC2 */
    uint8_t total_len = len + COMM_NUM_NON_PAYLOAD_BYTES;

    comm_status[chan].ck_a = COMM_STX;
    comm_status[chan].ck_b = COMM_STX;
    comm_send_ch(chan, COMM_STX);

    COMM_SEND_CH(chan, total_len);
    COMM_SEND_CH(chan, COMM_DEFAULT_ACID);
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

    comm_send_ch(chan, COMM_STX);
    comm_send_ch(chan, message->len + 4);
    comm_send_ch(chan, message->acid);
    comm_send_ch(chan, message->msgid);

    for (i = 0; i < message->len; i++)
        comm_send_ch(chan, message->payload[i]);

    comm_send_ch(chan, message->ck_a);
    comm_send_ch(chan, message->ck_b);
}


#define UPDATE_CHECKSUM(_x)                                                 \
    rxmsg->ck_a += _x;                                        \
    rxmsg->ck_b += rxmsg->ck_a;                 \

#define ADD_CHAR(_x)                                                        \
    rxmsg->payload[rxmsg->idx] = _x;     \
    rxmsg->idx++;

bool_t
comm_parse ( CommChannel_t chan )
{
    CommMessage_t *rxmsg = &comm_message[chan];

    while ( comm_ch_available(chan) && !comm_status[chan].msg_received ) 
    {
        uint8_t c = comm_get_ch(chan);
        switch (comm_status[chan].parse_state) 
        {
            case STATE_UNINIT:
                if (c == COMM_STX) {
                    comm_status[chan].parse_state++;
                    rxmsg->ck_a = COMM_STX;
                    rxmsg->ck_b = COMM_STX;
                }
                break;
            case STATE_GOT_STX:
                if (comm_status[chan].msg_received) {
                    comm_status[chan].buffer_overrun++;
                    goto error;
                }
                /* Counting STX, LENGTH, ACID, MSGID, CRC1 and CRC2 */
                rxmsg->len = c - COMM_NUM_NON_PAYLOAD_BYTES; 
                rxmsg->idx = 0;
                UPDATE_CHECKSUM(c)
                comm_status[chan].parse_state++;
                break;
            case STATE_GOT_LENGTH:
                rxmsg->acid = c;
                UPDATE_CHECKSUM(c)
                comm_status[chan].parse_state++;
                break;
            case STATE_GOT_ACID:
                rxmsg->msgid = c;
                UPDATE_CHECKSUM(c)
                if (rxmsg->len == 0)
                    comm_status[chan].parse_state = STATE_GOT_PAYLOAD;
                else
                    comm_status[chan].parse_state++;
                break;
            case STATE_GOT_MSGID:
                ADD_CHAR(c)
                UPDATE_CHECKSUM(c)
                if (rxmsg->idx == rxmsg->len)
                    comm_status[chan].parse_state++;
                break;
            case STATE_GOT_PAYLOAD:
                if (c != rxmsg->ck_a)
                    goto error;
                comm_status[chan].parse_state++;
                break;
            case STATE_GOT_CRC1:
                if (c != rxmsg->ck_b)
                    goto error;
                /* Successfully got message */
                comm_status[chan].msg_received = TRUE;
                goto restart;
        }
        break;
        error:
            comm_status[chan].parse_error++;
        restart:
            comm_status[chan].parse_state = STATE_UNINIT;
        break;
    }
    return comm_status[chan].msg_received;
}

bool_t
comm_send_message_by_id (CommChannel_t chan, uint8_t msgid)
{
    static uint8_t u8 = 1;
    static uint8_t i8 = -1;
    static uint16_t u16 = 10;
    static int16_t i16 = -10;
    static uint32_t u32 = 100;
    static int32_t i32 = -100;
    static float f = 0.0;

    switch(msgid) 
    {
        case MESSAGE_ID_PONG:
            MESSAGE_SEND_PONG();
            break;
        case MESSAGE_ID_COMM_STATUS:
            MESSAGE_SEND_COMM_STATUS( &comm_status[chan].buffer_overrun, &comm_status[chan].parse_error )
            break;
        case MESSAGE_ID_TEST_MESSAGE:
            MESSAGE_SEND_TEST_MESSAGE ( &u8, &i8, &u16, &i16, &u32, &i32, &f );
            u8 += 1; i8 -= 1;
            u16 += 10; i16 -= 10;
            u32 += 100; i32 -= 100;
            f += 15.0;
            break;
        default:
            return FALSE;
            break;
    }
    return TRUE;
}

bool_t
comm_event_task ( CommChannel_t chan ) 
{
    bool_t handled;
    bool_t ret = TRUE;

    if ( comm_channel_used[chan] && comm_ch_available(chan) && comm_parse(chan) ) 
    {
        handled = comm_send_message_by_id(chan, comm_message[chan].msgid);
        if ( !handled ) {
            if (comm_callback[chan])
                ret = comm_callback[chan](&comm_message[chan]);
            else
                ret = FALSE;
        }
        comm_status[chan].msg_received = FALSE;
    }
    else
        ret = FALSE;

    return ret;
}

void
comm_periodic_task ( CommChannel_t chan )
{
    static PeriodicMessage_t periodic[NUM_PERIODIC_MESSAGES] = PERIODIC_MESSAGE_INITIALIZER;

    uint8_t i;
    PeriodicMessage_t *p;

    for (i = 0; i < NUM_PERIODIC_MESSAGES; i++) 
    {
        p = &periodic[i];

        if (p->cnt == p->target) {
            comm_send_message_by_id(chan, p->msgid);
            p->cnt = 0;
        } else
            p->cnt += 1;
    }
            
}




