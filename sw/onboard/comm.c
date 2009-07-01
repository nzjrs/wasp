/*
 * vim: ai ts=4 sts=4 et sw=4
 */

#include "comm.h"
#include "sys_time.h"
#include "generated/build.h"

CommRXMessageCallback_t  comm_callback_rx[COMM_NB];
CommTXMessageCallback_t  comm_callback_tx[COMM_NB];
CommMessage_t            comm_message[COMM_NB];
CommStatus_t             comm_status[COMM_NB];
bool_t                   comm_channel_used[COMM_NB];

#define UPDATE_CHECKSUM(_msg, _x)           \
    _msg->ck_a += _x;                       \
    _msg->ck_b += _msg->ck_a;               \

#define ADD_CHAR(_msg, _x)                  \
    _msg->payload[_msg->idx] = _x;          \
    _msg->idx++;

void
comm_send_message_ch ( CommChannel_t chan, uint8_t c )
{
    comm_status[chan].ck_a += c;
    comm_status[chan].ck_b += comm_status[chan].ck_a;
    comm_send_ch(chan, c);
}

void
comm_start_message ( CommChannel_t chan, uint8_t id, uint8_t len )
{
    /* Counting STX, LENGTH, ACID, MSGID, CRC1 and CRC2 */
    uint8_t total_len = len + COMM_NUM_NON_PAYLOAD_BYTES;

    comm_status[chan].ck_a = COMM_STX;
    comm_status[chan].ck_b = COMM_STX;
    comm_send_ch(chan, COMM_STX);

    comm_send_message_ch(chan, total_len);
    comm_send_message_ch(chan, COMM_DEFAULT_ACID);
    comm_send_message_ch(chan, id);
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
    /* Counting STX, LENGTH, ACID, MSGID, CRC1 and CRC2 */
    uint8_t total_len = message->len + COMM_NUM_NON_PAYLOAD_BYTES;

    /* Calculate the checksum for the message */
    message->ck_a = COMM_STX;
    message->ck_b = COMM_STX;
    comm_send_ch(chan, COMM_STX);

    UPDATE_CHECKSUM(message, total_len)
    comm_send_ch(chan, total_len);

    UPDATE_CHECKSUM(message, message->acid)
    comm_send_ch(chan, message->acid);

    UPDATE_CHECKSUM(message, message->msgid)
    comm_send_ch(chan, message->msgid);

    for (i = 0; i < message->len; i++) {
        UPDATE_CHECKSUM(message, message->payload[i])
        comm_send_ch(chan, message->payload[i]);
    }

    comm_send_ch(chan, message->ck_a);
    comm_send_ch(chan, message->ck_b);
}

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
                UPDATE_CHECKSUM(rxmsg, c)
                comm_status[chan].parse_state++;
                break;
            case STATE_GOT_LENGTH:
                rxmsg->acid = c;
                UPDATE_CHECKSUM(rxmsg, c)
                comm_status[chan].parse_state++;
                break;
            case STATE_GOT_ACID:
                rxmsg->msgid = c;
                UPDATE_CHECKSUM(rxmsg, c)
                if (rxmsg->len == 0)
                    comm_status[chan].parse_state = STATE_GOT_PAYLOAD;
                else
                    comm_status[chan].parse_state++;
                break;
            case STATE_GOT_MSGID:
                ADD_CHAR(rxmsg, c)
                UPDATE_CHECKSUM(rxmsg, c)
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
#if INCLUDE_BUILD_INFO == 1
    static char build_revision[BUILD_STRING_LEN] =  BUILD_REV;
    static char build_branch[BUILD_STRING_LEN] =    BUILD_BRANCH;
    static char build_target[BUILD_STRING_LEN] =    BUILD_TARGET;
    static uint8_t build_dirty =                    BUILD_DIRTY;
    static uint32_t build_time =                    BUILD_TIME;
#else
    static char build_revision[BUILD_STRING_LEN] =  "N/A";
    static char build_branch[BUILD_STRING_LEN] =    "N/A";
    static char build_target[BUILD_STRING_LEN] =    "N/A";
    static uint8_t build_dirty =                    0;
    static uint32_t build_time =                    0;
#endif

    bool_t ret = TRUE;

    switch (msgid)
    {
        case MESSAGE_ID_TIME:
            MESSAGE_SEND_TIME(chan, &cpu_time_sec );
            break;
        case MESSAGE_ID_COMM_STATUS:
            MESSAGE_SEND_COMM_STATUS(chan, &comm_status[chan].buffer_overrun, &comm_status[chan].parse_error )
            break;
        case MESSAGE_ID_BUILD_INFO:
            MESSAGE_SEND_BUILD_INFO(chan, build_revision, build_branch, build_target, &build_dirty, &build_time )
            break;
        default:
            if (comm_callback_tx[chan])
                ret = comm_callback_tx[chan](chan, msgid);
            else
                ret = FALSE;
            break;
    }
    return ret;
}

bool_t
comm_event_task ( CommChannel_t chan ) 
{
    bool_t ret = TRUE;

    if ( comm_channel_used[chan] && comm_ch_available(chan) && comm_parse(chan) ) 
    {
        uint8_t msgid = comm_message[chan].msgid;
        CommMessage_t *msg = &comm_message[chan];

        /* handle standard messages directly in the comm layer */
        switch ( comm_message[chan].msgid )
        {
            case MESSAGE_ID_PING:
                MESSAGE_SEND_PONG(chan);
                break;
            case MESSAGE_ID_REQUEST_MESSAGE:
                msgid = MESSAGE_REQUEST_MESSAGE_GET_FROM_BUFFER_msgid(msg->payload);
                ret = comm_send_message_by_id(chan, msgid);
                break;
            case MESSAGE_ID_TIME:
            case MESSAGE_ID_STATUS:
            case MESSAGE_ID_COMM_STATUS:
                ret = comm_send_message_by_id(chan, msgid);
                break;
            default:
                if (comm_callback_rx[chan])
                    ret = comm_callback_rx[chan](chan, &comm_message[chan]);
                else
                    ret = FALSE;
                break;
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

void
comm_add_rx_callback ( CommChannel_t chan, CommRXMessageCallback_t cb)
{
    if (chan < COMM_NB && cb)
        comm_callback_rx[chan] = cb;
}

void
comm_add_tx_callback ( CommChannel_t chan, CommTXMessageCallback_t cb)
{
    if (chan < COMM_NB && cb)
        comm_callback_tx[chan] = cb;
}



