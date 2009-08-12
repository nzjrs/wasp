#include "comm-autopilot.h"

#include "led.h"
#include "rc.h"
#include "gps.h"
#include "imu.h"
#include "analog.h"
#include "altimeter.h"
#include "settings.h"

#include "booz2_autopilot.h"
#include "booz2_ins.h"
#include "booz2_guidance_h.h"
#include "booz2_guidance_v.h"

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
                    &booz_gps_state.booz2_gps_hmsl,
                    &booz_gps_state.booz2_gps_hacc,
                    &booz_gps_state.booz2_gps_vacc);
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
        case MESSAGE_ID_AUTOPILOT:
            MESSAGE_SEND_AUTOPILOT(COMM_1,
                    &booz2_autopilot_mode,
                    &booz2_guidance_h_mode,
                    &booz2_guidance_v_mode);
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
    bool_t ret = FALSE;

    switch (message->msgid)
    {
        case MESSAGE_ID_GET_SETTING:
        case MESSAGE_ID_SETTING_UINT8:
        case MESSAGE_ID_SETTING_FLOAT:
            ret = settings_handle_message_received(chan, message);
            break;
        default:
            break;
    }

    return ret;
}

