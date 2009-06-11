/* This file has been generated from /home/john/Programming/paparazzi.git/conf/settings/settings_booz2.xml */
/* Please DO NOT EDIT */

#ifndef SETTINGS_H
#define SETTINGS_H 

#define RCSettings(mode_changed) { \
}

#include "booz2_analog_baro.h"
#include "booz2_autopilot.h"
#include "booz2_filter_attitude_cmpl_euler.h"
#include "booz2_fms.h"
#include "booz2_guidance_h.h"
#include "booz2_guidance_v.h"
#include "booz2_ins.h"
#include "booz2_stabilization_attitude.h"
#include "booz2_stabilization_rate.h"
#include "booz2_telemetry.h"

#define DlSetting(_idx, _value) { \
  switch (_idx) { \
    case 0: telemetry_mode_Main = _value; break;\
    case 1: booz2_fms_SetOnOff( _value ); _value = booz_fms_on; break;\
    case 2: booz2_autopilot_mode_auto2 = _value; break;\
    case 3: booz2_autopilot_SetTol( _value ); _value = booz2_autopilot_tol; break;\
    case 4: booz2_stabilization_rate_gain.p = _value; break;\
    case 5: booz2_stabilization_rate_gain.q = _value; break;\
    case 6: booz2_stabilization_rate_gain.r = _value; break;\
    case 7: booz_stabilization_pgain.x = _value; break;\
    case 8: booz_stabilization_pgain.y = _value; break;\
    case 9: booz_stabilization_pgain.z = _value; break;\
    case 10: booz_stabilization_dgain.x = _value; break;\
    case 11: booz_stabilization_dgain.y = _value; break;\
    case 12: booz_stabilization_dgain.z = _value; break;\
    case 13: booz_stabilization_igain.x = _value; break;\
    case 14: booz_stabilization_igain.y = _value; break;\
    case 15: booz_stabilization_igain.z = _value; break;\
    case 16: booz_stabilization_ddgain.x = _value; break;\
    case 17: booz_stabilization_ddgain.y = _value; break;\
    case 18: booz_stabilization_ddgain.z = _value; break;\
    case 19: booz2_guidance_v_kp = _value; break;\
    case 20: booz2_guidance_v_kd = _value; break;\
    case 21: booz2_guidance_v_z_sp = _value; break;\
    case 22: booz_ins_vff_realign = _value; break;\
    case 23: booz2_guidance_h_pos_sp.x = _value; break;\
    case 24: booz2_guidance_h_pos_sp.y = _value; break;\
    case 25: booz2_guidance_h_psi_sp = _value; break;\
    case 26: booz2_guidance_h_pgain = _value; break;\
    case 27: booz2_guidance_h_dgain = _value; break;\
    case 28: booz2_guidance_h_SetKi( _value ); _value = booz2_guidance_h_igain; break;\
    case 29: booz2_face_reinj_1 = _value; break;\
    case 30: booz2_analog_baro_SetOffset( _value ); _value = booz2_analog_baro_offset; break;\
  }\
}
#define PeriodicSendDlValue() { \
  static uint8_t i;\
  float var;\
  if (i >= 31) i = 0;;\
  switch (i) { \
    case 0: var = telemetry_mode_Main; break;\
    case 1: var = booz_fms_on; break;\
    case 2: var = booz2_autopilot_mode_auto2; break;\
    case 3: var = booz2_autopilot_tol; break;\
    case 4: var = booz2_stabilization_rate_gain.p; break;\
    case 5: var = booz2_stabilization_rate_gain.q; break;\
    case 6: var = booz2_stabilization_rate_gain.r; break;\
    case 7: var = booz_stabilization_pgain.x; break;\
    case 8: var = booz_stabilization_pgain.y; break;\
    case 9: var = booz_stabilization_pgain.z; break;\
    case 10: var = booz_stabilization_dgain.x; break;\
    case 11: var = booz_stabilization_dgain.y; break;\
    case 12: var = booz_stabilization_dgain.z; break;\
    case 13: var = booz_stabilization_igain.x; break;\
    case 14: var = booz_stabilization_igain.y; break;\
    case 15: var = booz_stabilization_igain.z; break;\
    case 16: var = booz_stabilization_ddgain.x; break;\
    case 17: var = booz_stabilization_ddgain.y; break;\
    case 18: var = booz_stabilization_ddgain.z; break;\
    case 19: var = booz2_guidance_v_kp; break;\
    case 20: var = booz2_guidance_v_kd; break;\
    case 21: var = booz2_guidance_v_z_sp; break;\
    case 22: var = booz_ins_vff_realign; break;\
    case 23: var = booz2_guidance_h_pos_sp.x; break;\
    case 24: var = booz2_guidance_h_pos_sp.y; break;\
    case 25: var = booz2_guidance_h_psi_sp; break;\
    case 26: var = booz2_guidance_h_pgain; break;\
    case 27: var = booz2_guidance_h_dgain; break;\
    case 28: var = booz2_guidance_h_igain; break;\
    case 29: var = booz2_face_reinj_1; break;\
    case 30: var = booz2_analog_baro_offset; break;\
    default: var = 0.; break;\
  }\
  DOWNLINK_SEND_DL_VALUE(&i, &var);\
  i++;\
}

#endif // SETTINGS_H
