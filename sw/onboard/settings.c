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
#include "supervision.h"

#include "generated/messages.h"
#include "generated/settings.h"

static inline bool_t
set_setting_i32(uint8_t id, int32_t val)
{
    bool_t ret = TRUE;

    switch (id)
    {
        case SETTING_ID_SUPERVISION_TRIM_A:
            supervision_set_trim(val, supervision_trim.trim_e, supervision_trim.trim_r, supervision_trim.trim_t); 
            break;
        case SETTING_ID_SUPERVISION_TRIM_E:
            supervision_set_trim(supervision_trim.trim_a, val, supervision_trim.trim_r, supervision_trim.trim_t); 
            break;
        case SETTING_ID_SUPERVISION_TRIM_R:
            supervision_set_trim(supervision_trim.trim_a, supervision_trim.trim_e, val, supervision_trim.trim_t); 
            break;
        case SETTING_ID_SUPERVISION_TRIM_T:
            supervision_set_trim(supervision_trim.trim_a, supervision_trim.trim_e, supervision_trim.trim_r, val); 
            break;
        default:
            ret = FALSE;
    }
    return ret;
}

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
    Type_t type;
    bool_t ret = TRUE;

    switch (id)
    {
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_PHI:
            type = SETTING_TYPE_IMU_ALIGNMENT_BODY_TO_IMU_PHI;
            MESSAGE_SEND_SETTING_FLOAT(chan, &id, &type,
                &booz_imu.body_to_imu_phi);
            break;
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_THETA:
            type = SETTING_TYPE_IMU_ALIGNMENT_BODY_TO_IMU_THETA;
            MESSAGE_SEND_SETTING_FLOAT(chan, &id, &type,
                &booz_imu.body_to_imu_theta);
            break;
        case SETTING_ID_IMU_ALIGNMENT_BODY_TO_IMU_PSI:
            type = SETTING_TYPE_IMU_ALIGNMENT_BODY_TO_IMU_PSI;
            MESSAGE_SEND_SETTING_FLOAT(chan, &id, &type,
                &booz_imu.body_to_imu_psi);
            break;
        case SETTING_ID_SUPERVISION_TRIM_A:
            type = SETTING_TYPE_SUPERVISION_TRIM_A;
            MESSAGE_SEND_SETTING_INT32(chan, &id, &type, 
                &supervision_trim.trim_a);
            break;
        case SETTING_ID_SUPERVISION_TRIM_E:
            type = SETTING_TYPE_SUPERVISION_TRIM_E;
            MESSAGE_SEND_SETTING_INT32(chan, &id, &type, 
                &supervision_trim.trim_e);
            break;
        case SETTING_ID_SUPERVISION_TRIM_R:
            type = SETTING_TYPE_SUPERVISION_TRIM_R;
            MESSAGE_SEND_SETTING_INT32(chan, &id, &type, 
                &supervision_trim.trim_r);
            break;
        case SETTING_ID_SUPERVISION_TRIM_T:
            type = SETTING_TYPE_SUPERVISION_TRIM_T;
            MESSAGE_SEND_SETTING_INT32(chan, &id, &type, 
                &supervision_trim.trim_t);
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
        case MESSAGE_ID_SETTING_INT32:
        case MESSAGE_ID_SETTING_FLOAT:
            {
            float f;
            uint8_t u8;
            int32_t i32;

            id = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_id(msg->payload);
            type = (Type_t)MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_type(msg->payload);

            switch (type) 
            {
                case TYPE_UINT8:
                    u8 = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_value(msg->payload);
                    ret = set_setting_u8(id, u8);
                    break;
                case TYPE_FLOAT:
                    f = MESSAGE_SETTING_FLOAT_GET_FROM_BUFFER_value(msg->payload);
                    ret = set_setting_float(id, f);
                    break;
                case TYPE_INT32:
                    i32 = MESSAGE_SETTING_INT32_GET_FROM_BUFFER_value(msg->payload);
                    ret = set_setting_i32(id, i32);
                    break;
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
