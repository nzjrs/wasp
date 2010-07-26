#include "gps.h"
#include "imu.h"
#include "altimeter.h"
#include "ahrs.h"

#include "nps_fdm.h"
#include "nps_led.h"
#include "nps_state.h"

static bool_t bypass_ahrs;

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

void imu_init(void) {}
void imu_periodic_task ( void ) {}
uint8_t imu_event_task ( void )
{
    uint8_t valid = IMU_ACC | IMU_GYR | IMU_MAG;
    return valid;
}
void imu_adjust_alignment( float phi, float theta, float psi )
{
    ;
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
    } else {
      nps_log("FIXME\n");
    }

}

void nps_state_init(bool_t _bypass_ahrs)
{
    bypass_ahrs = _bypass_ahrs;
}
