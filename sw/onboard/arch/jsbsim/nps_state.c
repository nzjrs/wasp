#include "gps.h"
#include "imu.h"
#include "altimeter.h"
#include "ahrs.h"
#include "led.h"

#include "generated/settings.h"

#include "nps_fdm.h"
#include "nps_state.h"
#include "nps_sensors.h"

static bool_t bypass_ahrs;
static bool_t bypass_gps;

/***** Altimeter
 The state is always valid and we get an update from the FDM of every sensor */
SystemStatus_t altimeter_system_status;
uint16_t altimeter_calibration_offset;
uint16_t altimeter_calibration_raw;

void altimeter_init(void)
{
    altimeter_system_status = STATUS_INITIALIZED;
}

void altimeter_periodic_task(void) {}
uint8_t altimeter_event_task ( void ) { return 0; }
int32_t altimeter_get_altitude( void ) { return 0; }
void altimeter_recalibrate( void ) {}

/***** IMU
 The state is always valid and we get an update from the FDM of every sensor */
IMU_t booz_imu;

void imu_init(void)
{
    /* initialises neutrals */
    RATES_ASSIGN(booz_imu.gyro_neutral,  IMU_NEUTRAL_GYRO_P,  IMU_NEUTRAL_GYRO_Q,  IMU_NEUTRAL_GYRO_R);
    VECT3_ASSIGN(booz_imu.accel_neutral, IMU_NEUTRAL_ACCEL_X, IMU_NEUTRAL_ACCEL_Y, IMU_NEUTRAL_ACCEL_Z);
    VECT3_ASSIGN(booz_imu.mag_neutral,   IMU_NEUTRAL_MAG_X,   IMU_NEUTRAL_MAG_Y,   IMU_NEUTRAL_MAG_Z);

    /* initialise IMU alignment */
    imu_adjust_alignment(IMU_ALIGNMENT_BODY_TO_IMU_PHI, IMU_ALIGNMENT_BODY_TO_IMU_THETA, IMU_ALIGNMENT_BODY_TO_IMU_PSI);
}

void imu_periodic_task ( void )
{

}

uint8_t imu_event_task ( void )
{
    uint8_t valid = 0;

    if (sensors.gyro.data_available) {
        valid |= IMU_GYR;
        /* copy the gyro values across, x,y,z = p,q,r */
        booz_imu.gyro_unscaled.p = sensors.gyro.value.x;
        booz_imu.gyro_unscaled.q = sensors.gyro.value.y;
        booz_imu.gyro_unscaled.r = sensors.gyro.value.z;
    }

    if (sensors.accel.data_available) {
        valid |= IMU_ACC;
        /* copy the accel values across, x,y,z = p,q,r */
        booz_imu.accel_unscaled.x = sensors.accel.value.x;
        booz_imu.accel_unscaled.y = sensors.accel.value.y;
        booz_imu.accel_unscaled.z = sensors.accel.value.z;
    }

    if (sensors.mag.data_available) {
        valid |= IMU_MAG;
        /* copy the mag values across, x,y,z = p,q,r */
        booz_imu.mag_unscaled.x = sensors.gyro.value.x;
        booz_imu.mag_unscaled.y = sensors.gyro.value.y;
        booz_imu.mag_unscaled.z = sensors.gyro.value.z;
    }

    return valid;
}

/***** GPS
 The state is always valid and we always get an update from the FDM */
SystemStatus_t gps_system_status;
GPS_t gps_state;
void gps_init(void)
{
    gps_system_status = STATUS_ALIVE;
}
bool_t gps_event_task(void)
{
    gps_state.fix = GPS_FIX_3D;
    return TRUE;
}

void nps_state_update(void)
{
    ahrs.enabled = !bypass_ahrs;
    /* if the AHRS is disabled then just copy the state from the fdm */
    if (bypass_ahrs) {
        ahrs_status = STATUS_INITIALIZED;

        ahrs.ltp_to_body_euler.phi   = ANGLE_BFP_OF_REAL(fdm.ltp_to_body_eulers.phi);
        ahrs.ltp_to_body_euler.theta = ANGLE_BFP_OF_REAL(fdm.ltp_to_body_eulers.theta);
        ahrs.ltp_to_body_euler.psi   = ANGLE_BFP_OF_REAL(fdm.ltp_to_body_eulers.psi);

        ahrs.ltp_to_body_quat.qi = QUAT1_BFP_OF_REAL(fdm.ltp_to_body_quat.qi);
        ahrs.ltp_to_body_quat.qx = QUAT1_BFP_OF_REAL(fdm.ltp_to_body_quat.qx);
        ahrs.ltp_to_body_quat.qy = QUAT1_BFP_OF_REAL(fdm.ltp_to_body_quat.qy);
        ahrs.ltp_to_body_quat.qz = QUAT1_BFP_OF_REAL(fdm.ltp_to_body_quat.qz);

        ahrs.body_rate.p = RATE_BFP_OF_REAL(fdm.body_ecef_rotvel.p);
        ahrs.body_rate.q = RATE_BFP_OF_REAL(fdm.body_ecef_rotvel.q);
        ahrs.body_rate.r = RATE_BFP_OF_REAL(fdm.body_ecef_rotvel.r);

        INT32_RMAT_OF_QUAT(ahrs.ltp_to_body_rmat, ahrs.ltp_to_body_quat);
    }

    if (bypass_gps) {
        gps_state.lat = DegOfRad(fdm.lla_pos.lat)/1e-7;
        gps_state.lon = DegOfRad(fdm.lla_pos.lon)/1e-7;
        gps_state.hmsl = fdm.lla_pos.alt * 1000.0; /* convert to mm */
    }
}

void nps_state_init(bool_t _bypass_ahrs)
{
    bypass_ahrs = _bypass_ahrs;
    bypass_gps = _bypass_ahrs;
}
