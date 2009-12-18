#include "std.h"
#include "messages.h"
#include "messages_types.h"
#include "comm.h"

CommStatus_t    comm_status[COMM_NB];

CommStatus_t    rxstatus;
CommMessage_t   rxmsg;

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

#define UPDATE_CHECKSUM(_msg, _x)           \
    _msg.ck_a += _x;                       \
    _msg.ck_b += _msg.ck_a;               \

#define ADD_CHAR(_msg, _x)                  \
    _msg.payload[_msg.idx] = _x;          \
    _msg.idx++;

const CommMessage_t *
comm_parse (uint8_t *data, uint8_t len)
{
    uint8_t i = 0;
    uint8_t msg_received = FALSE;

    while ( (i < len) && !msg_received ) 
    {
        uint8_t c = data[i++];
        switch (rxstatus.parse_state) 
        {
            case STATE_UNINIT:
                if (c == COMM_STX) {
                    rxstatus.parse_state++;
                    rxmsg.ck_a = COMM_STX;
                    rxmsg.ck_b = COMM_STX;
                }
                break;
            case STATE_GOT_STX:
                if (msg_received) {
                    rxstatus.buffer_overrun++;
                    goto error;
                }
                /* Counting STX, LENGTH, ACID, MSGID, CRC1 and CRC2 */
                rxmsg.len = c - COMM_NUM_NON_PAYLOAD_BYTES; 
                rxmsg.idx = 0;
                UPDATE_CHECKSUM(rxmsg, c)
                rxstatus.parse_state++;
                break;
            case STATE_GOT_LENGTH:
                rxmsg.acid = c;
                UPDATE_CHECKSUM(rxmsg, c)
                rxstatus.parse_state++;
                break;
            case STATE_GOT_ACID:
                rxmsg.msgid = c;
                UPDATE_CHECKSUM(rxmsg, c)
                if (rxmsg.len == 0)
                    rxstatus.parse_state = STATE_GOT_PAYLOAD;
                else
                    rxstatus.parse_state++;
                break;
            case STATE_GOT_MSGID:
                ADD_CHAR(rxmsg, c)
                UPDATE_CHECKSUM(rxmsg, c)
                if (rxmsg.idx == rxmsg.len)
                    rxstatus.parse_state++;
                break;
            case STATE_GOT_PAYLOAD:
                if (c != rxmsg.ck_a)
                    goto error;
                rxstatus.parse_state++;
                break;
            case STATE_GOT_CRC1:
                if (c != rxmsg.ck_b)
                    goto error;
                /* Successfully got message */
                msg_received = TRUE;
                goto restart;
        }
        continue;
        error:
            rxstatus.parse_error++;
        restart:
            rxstatus.parse_state = STATE_UNINIT;
        break;
    }
    return (msg_received ? &rxmsg : NULL);
}

void
comm_init (void)
{
    uint8_t i;

    for (i = 0; i < COMM_NB; i++) {
        comm_status[i].parse_state = STATE_UNINIT;
        comm_status[i].msg_received = FALSE;
        comm_status[i].buffer_overrun = 0;
        comm_status[i].parse_error = 0;
    }

    rxstatus.parse_state = STATE_UNINIT;
    rxstatus.msg_received = FALSE;
    rxstatus.buffer_overrun = 0;
    rxstatus.parse_error = 0;
}

