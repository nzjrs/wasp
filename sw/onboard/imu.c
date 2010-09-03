#include "std.h"
#include "imu.h"
#include "math/pprz_algebra_int.h"

void
imu_adjust_alignment( float phi, float theta, float psi )
{
    booz_imu.body_to_imu_phi = phi;
    booz_imu.body_to_imu_theta = theta;
    booz_imu.body_to_imu_psi = psi;

    /*
    Compute quaternion and rotation matrix
    for conversions between body and imu frame
    */
    struct Int32Eulers body_to_imu_eulers = {
            ANGLE_BFP_OF_REAL(RadOfDeg(phi)),
            ANGLE_BFP_OF_REAL(RadOfDeg(theta)),
            ANGLE_BFP_OF_REAL(RadOfDeg(psi))
    };

    INT32_QUAT_OF_EULERS(booz_imu.body_to_imu_quat, body_to_imu_eulers);
    INT32_QUAT_NORMALISE(booz_imu.body_to_imu_quat);
    INT32_RMAT_OF_EULERS(booz_imu.body_to_imu_rmat, body_to_imu_eulers);
}

