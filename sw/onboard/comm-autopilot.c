#include "comm-autopilot.h"

#include "rc.h"
#include "gps.h"
#include "imu.h"
#include "analog.h"
#include "altimeter.h"
#include "settings.h"

#include "booz2_autopilot.h"
#include "booz2_ins.h"

bool_t
comm_autopilot_send ( CommChannel_t chan, uint8_t msgid )
{
    uint8_t ret = TRUE;

    switch (msgid)
    {
        case MESSAGE_ID_GPS_LLH:
            MESSAGE_SEND_GPS_LLH( COMM_1, 
                &booz_gps_state.fix,
                &booz_gps_state.num_sv,
                &booz_gps_state.booz2_gps_lat,
                &booz_gps_state.booz2_gps_lon,
                &booz_gps_state.booz2_gps_hmsl);
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
                    COMM_1,
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
                    &booz_gps_state.fix,
                    &bat,
                    &booz2_autopilot_in_flight,
                    &booz2_autopilot_motors_on,
                    &booz2_autopilot_mode);
            }
            break;
        case MESSAGE_ID_ALTIMETER:
            {
            int32_t alt = altimeter_get_altitude();
            MESSAGE_SEND_ALTIMETER(COMM_1,
                    &alt,
                    &altimeter_status,
                    &booz2_analog_baro_offset,
                    &booz2_analog_baro_value);
            }
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
    if (message)
    {
        void *value;
        Type_t type;
        uint8_t id, u8;
        uint8_t *payload = message->payload;

        id = 0;
        value = NULL;
        switch (message->msgid)
        {
            case MESSAGE_ID_GET_SETTING:
                id = MESSAGE_GET_SETTING_GET_FROM_BUFFER_id(payload);
                if ( settings_get(id, &type, value) )
                {
                    ;
                }
                return TRUE;
                break;
            case MESSAGE_ID_SETTING_UINT8:
                id = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_id(payload);
                type = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_type(payload);
                u8 = MESSAGE_SETTING_UINT8_GET_FROM_BUFFER_value(payload);
                value = &u8;
                break;
            default:
                return FALSE;
                break;
        }
        settings_set(id, type, value);
        return TRUE;
    }
    return FALSE;
}

