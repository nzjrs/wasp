#include "settings.h"
#include "comm.h"
#include "generated/messages.h"
#include "generated/settings.h"

static inline bool_t
set_setting_u8(uint8_t id, uint8_t val)
{
    return TRUE;
}

static inline bool_t
set_setting_float(uint8_t id, float val)
{
    return TRUE;
}

static inline bool_t
get_setting(CommChannel_t chan, uint8_t id)
{
    bool_t ret = TRUE;

    switch (id)
    {
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_PHI:
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_THETA:
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_PSI:
            break;
        default:
            ret = FALSE;
            break;
    }
        
    return ret;
}

bool_t
settings_handle_message_received(CommChannel_t chan, CommMessage_t *msg)
{
    Type_t type;
    uint8_t id;
    bool_t ret = TRUE;

    switch (msg->msgid)
    {
        case MESSAGE_ID_GET_SETTING:
            id = MESSAGE_GET_SETTING_GET_FROM_BUFFER_id(msg->payload);
            ret = get_setting(chan, id);
            break;
        case MESSAGE_ID_SETTING_UINT8:
        case MESSAGE_ID_SETTING_FLOAT:
            {
            float f;
            uint8_t u8;

            id = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_id(msg->payload);
            type = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_type(msg->payload);

            switch (type) {
                case TYPE_UINT8:
                    u8 = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_value(msg->payload);
                    ret = set_setting_u8(id, u8);
                    break;
                case TYPE_FLOAT:
                    f = MESSAGE_SETTING_FLOAT_GET_FROM_BUFFER_value(msg->payload);
                    ret = set_setting_float(id, f);
                    break;
                case TYPE_INT8:
                case TYPE_UINT16:
                case TYPE_INT16:
                case TYPE_UINT32:
                case TYPE_INT32:
                default:
                    ret = FALSE;
                    break;
            }
            break;
            }
        default:
            ret = FALSE;
            break;
    }

    return ret;
}
