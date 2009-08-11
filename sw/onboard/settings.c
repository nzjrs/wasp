#include "settings.h"
#include "comm.h"
#include "generated/messages.h"

void
settings_load_all(void)
{
    ;
}

bool_t
settings_handle_message_received(CommChannel_t chan, CommMessage_t *msg)
{
    Type_t type;
    uint8_t id;
    void *value;
    bool_t ret = TRUE;

    switch (msg->msgid)
    {
        case MESSAGE_ID_GET_SETTING:
            id = MESSAGE_GET_SETTING_GET_FROM_BUFFER_id(msg->payload);
            break;
        case MESSAGE_ID_SETTING_UINT8:
            {
            uint8_t u8;

            id = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_id(msg->payload);
            type = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_type(msg->payload);
            u8 = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_value(msg->payload);

            MESSAGE_SEND_DEBUG(chan, &u8);

            break;
            }
        case MESSAGE_ID_SETTING_FLOAT:
            {
            float f;
            uint8_t u8;

            id = MESSAGE_SETTING_FLOAT_GET_FROM_BUFFER_id(msg->payload);
            type = MESSAGE_SETTING_FLOAT_GET_FROM_BUFFER_type(msg->payload);
            f = MESSAGE_SETTING_FLOAT_GET_FROM_BUFFER_value(msg->payload);

            u8 = (uint8_t)f;
            MESSAGE_SEND_DEBUG(chan, &u8);

            break;
            }
        default:
            ret = FALSE;
            break;
    }

    return ret;
}
