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
#include "comm_autopilot.h"

#include "led.h"
#include "rc.h"
#include "gps.h"
#include "gpio.h"
#include "imu.h"
#include "ins.h"
#include "fms.h"
#include "ahrs.h"
#include "analog.h"
#include "altimeter.h"
#include "settings.h"
#include "sys_time.h"
#include "autopilot.h"
#include "guidance.h"

#include "generated/messages.h"

bool_t
comm_autopilot_message_send ( CommChannel_t chan, uint8_t msgid )
{
    uint8_t ret = TRUE;

    switch (msgid)
    {
        case MESSAGE_ID_GPS_LLH:
            MESSAGE_SEND_GPS_LLH(
                    chan, 
                    &gps_state.fix,
                    &gps_state.num_sv,
                    &gps_state.lat,
                    &gps_state.lon,
                    &gps_state.hmsl,
                    &gps_state.hacc,
                    &gps_state.vacc);
            break;
        case MESSAGE_ID_GPS_STATUS:
            MESSAGE_SEND_GPS_STATUS(
                    chan,
                    &gps_state.buffer_overrun,
                    &gps_state.parse_error,
                    &gps_state.parse_ignored);
            break;
        case MESSAGE_ID_GPS_GSV:
            {
#if RECORD_NUM_SAT_INFO
            static uint8_t selected_sat_info = 0;
            if (selected_sat_info < gps_state.num_sat_info) {
                GPSSatellite_t *sat = &gps_state.sat_info[selected_sat_info];
                MESSAGE_SEND_GPS_GSV(
                    chan,
                    &gps_state.num_sat_info,
                    &sat->sat_id,
                    &sat->elevation,
                    &sat->azimuth,
                    &sat->signal_strength);
                selected_sat_info += 1;
            } else
                selected_sat_info = 0;
#endif
            }
            break;
        case MESSAGE_ID_IMU_GYRO_RAW:
            MESSAGE_SEND_IMU_GYRO_RAW(
                    chan,
                    &booz_imu.gyro_unscaled.p,
                    &booz_imu.gyro_unscaled.q,
                    &booz_imu.gyro_unscaled.r);
            break;
        case MESSAGE_ID_IMU_ACCEL_RAW:
            MESSAGE_SEND_IMU_ACCEL_RAW(
                    chan,
                    &booz_imu.accel_unscaled.x,
			        &booz_imu.accel_unscaled.y,
			        &booz_imu.accel_unscaled.z);
            break;
        case MESSAGE_ID_IMU_MAG_RAW:
            MESSAGE_SEND_IMU_MAG_RAW(
                    chan,
                    &booz_imu.mag_unscaled.x,
			        &booz_imu.mag_unscaled.y,
			        &booz_imu.mag_unscaled.z);
            break;
        case MESSAGE_ID_IMU_GYRO:
            MESSAGE_SEND_IMU_GYRO(
                    chan,
                    &booz_imu.gyro.p,
                    &booz_imu.gyro.q,
                    &booz_imu.gyro.r);
            break;
        case MESSAGE_ID_IMU_ACCEL:
            MESSAGE_SEND_IMU_ACCEL(
                    chan,
                    &booz_imu.accel.x,
                    &booz_imu.accel.y,
                    &booz_imu.accel.z);
            break;
        case MESSAGE_ID_IMU_MAG:
            MESSAGE_SEND_IMU_MAG(
                    chan,
                    &booz_imu.mag.x,
			        &booz_imu.mag.y,
			        &booz_imu.mag.z);
            break;
        case MESSAGE_ID_PPM:
            MESSAGE_SEND_PPM(chan, ppm_pulses);
            break;
        case MESSAGE_ID_RC:
            MESSAGE_SEND_RC(chan, rc_values);
            break;
        case MESSAGE_ID_STATUS:
            {
            uint8_t bat = analog_read_battery();
            MESSAGE_SEND_STATUS(
                    chan,
                    &rc_status,
                    &gps_state.fix,
                    &bat,
                    &autopilot.in_flight,
                    &autopilot.motors_on,
                    &autopilot.mode,
                    &cpu_usage,
                    &fms.enabled,
                    &fms.mode);
            }
            break;
        case MESSAGE_ID_ALTIMETER:
            {
            int32_t alt = altimeter_get_altitude();
            MESSAGE_SEND_ALTIMETER(
                    chan,
                    &alt,
                    &altimeter_system_status,
                    &altimeter_calibration_offset,
                    &altimeter_calibration_raw);
            }
            break;
        case MESSAGE_ID_AUTOPILOT:
            MESSAGE_SEND_AUTOPILOT(
                    chan,
                    &autopilot.mode,
                    &booz2_guidance_h_mode,
                    &booz2_guidance_v_mode);
            break;
        case MESSAGE_ID_STATUS_LOWLEVEL:
            MESSAGE_SEND_STATUS_LOWLEVEL(
                    chan,
                    &rc_system_status,
                    &gps_system_status,
                    &altimeter_system_status,
                    &comm_system_status,
                    &ahrs_status);
            break;
        case MESSAGE_ID_ANALOG:
            {
            uint16_t c1 = analog_read_channel(ANALOG_CHANNEL_BATTERY);
            uint16_t c2 = analog_read_channel(ANALOG_CHANNEL_PRESSURE);
            uint16_t c3 = analog_read_channel(ANALOG_CHANNEL_ADC_SPARE);
            MESSAGE_SEND_ANALOG(
                    chan,
                    &c1,
                    &c2,
                    &c3);
            }
            break;
        case MESSAGE_ID_AHRS_QUAT:
            MESSAGE_SEND_AHRS_QUAT(
                    chan,
                    &ahrs.ltp_to_imu_quat.qi,
                    &ahrs.ltp_to_imu_quat.qx,
                    &ahrs.ltp_to_imu_quat.qy,
                    &ahrs.ltp_to_imu_quat.qz,
                    &ahrs.ltp_to_body_quat.qi,
                    &ahrs.ltp_to_body_quat.qx,
                    &ahrs.ltp_to_body_quat.qy,
                    &ahrs.ltp_to_body_quat.qz);
            break;
        case MESSAGE_ID_AHRS_EULER:
            MESSAGE_SEND_AHRS_EULER(
                    chan,
                    &ahrs.ltp_to_imu_euler.phi,
                    &ahrs.ltp_to_imu_euler.theta,
                    &ahrs.ltp_to_imu_euler.psi,
                    &ahrs.ltp_to_body_euler.phi,
                    &ahrs.ltp_to_body_euler.theta,
                    &ahrs.ltp_to_body_euler.psi);
            break;
        case MESSAGE_ID_SUPERVISION:
            MESSAGE_SEND_SUPERVISION(
                    chan,
                    &autopilot.motor_commands[0],
                    &autopilot.motor_commands[1],
                    &autopilot.motor_commands[2],
                    &autopilot.motor_commands[3],
                    &autopilot.commands[0],
                    &autopilot.commands[1],
                    &autopilot.commands[2],
                    &autopilot.commands[3]);
            break;
        default:
            ret = FALSE;
            break;
    }

    return ret;
}

bool_t 
comm_autopilot_message_received (CommChannel_t chan, CommMessage_t *message)
{
    bool_t ret = TRUE;
    bool_t need_ack = TRUE;

    switch (message->msgid)
    {
        case MESSAGE_ID_GET_SETTING:
        case MESSAGE_ID_SETTING_UINT8:
        case MESSAGE_ID_SETTING_INT32:
        case MESSAGE_ID_SETTING_FLOAT:
            ret = settings_handle_message_received(chan, message);
            need_ack = FALSE;
            break;
        case MESSAGE_ID_ALTIMETER_RESET:
            altimeter_recalibrate();
            break;
        case MESSAGE_ID_MOTORS_START:
            autopilot_set_motors(TRUE);
            break;
        case MESSAGE_ID_MOTORS_STOP:
            autopilot_set_motors(FALSE);
            break;
        case MESSAGE_ID_KILL:
            autopilot_kill();
            break;
        case MESSAGE_ID_GPIO_ON:
            gpio_on( MESSAGE_GPIO_ON_GET_FROM_BUFFER_id(message->payload) );
            break;
        case MESSAGE_ID_GPIO_OFF:
            gpio_off( MESSAGE_GPIO_OFF_GET_FROM_BUFFER_id(message->payload) );
            break;
        default:
            ret = FALSE;
            break;
    }

    /* commands need to be ACK'd or NACK'd (not implemented...) */
    if (need_ack)
        comm_send_command_ack (chan, message->msgid);

    return ret;
}

