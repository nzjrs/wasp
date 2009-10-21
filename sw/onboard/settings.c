/*
 * Copyright (C) 2008 Antoine Drouin
 * Copyright (C) 2009 John Stowers
 *
 * This file is part of wasp, some code taken from paparazzi (GPL)
 *
 * wasp is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * wasp is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, write to
 * the Free Software Foundation, 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 */
#include "settings.h"

#include "comm.h"
#include "imu.h"

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
    bool_t ret = TRUE;

    switch (id)
    {
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_PHI:
            imu_adjust_alignment(val, booz_imu.body_to_imu_theta, booz_imu.body_to_imu_psi);
            break;
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_THETA:
            imu_adjust_alignment(booz_imu.body_to_imu_phi, val, booz_imu.body_to_imu_psi);
            break;
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_PSI:
            imu_adjust_alignment(booz_imu.body_to_imu_phi, booz_imu.body_to_imu_theta, val);
            break;
        default:
            ret = FALSE;
    }

    return ret;
}

static inline bool_t
get_setting(CommChannel_t chan, uint8_t id)
{
    Type_t type = TYPE_FLOAT;
    float *value = NULL;
    bool_t ret = TRUE;

    switch (id)
    {
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_PHI:
            value = &booz_imu.body_to_imu_phi;
            break;
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_THETA:
            value = &booz_imu.body_to_imu_theta;
            break;
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_PSI:
            value = &booz_imu.body_to_imu_psi;
            break;
        default:
            ret = FALSE;
            break;
    }

    if (value != NULL)
        MESSAGE_SEND_SETTING_FLOAT(chan, &id, &type, value);
        
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
