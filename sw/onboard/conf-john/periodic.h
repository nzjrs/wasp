/* This file has been generated from /home/john/Programming/paparazzi.git/conf/messages.xml and /home/john/Programming/paparazzi.git/conf/telemetry/telemetry_booz2.xml */
/* Please DO NOT EDIT */


/* Macros for Main process */
#define TELEMETRY_MODE_Main_default 0
#define PERIOD_DL_VALUE_0 (1.1)
#define PERIOD_BOOZ_STATUS_0 (1.2)
#define PERIOD_BOOZ2_FP_0 (0.25)
#define PERIOD_ALIVE_0 (2.1)
#define PERIOD_BOOZ2_NAV_REF_0 (5.)
#define PERIOD_BOOZ2_NAV_STATUS_0 (1.6)
#define PERIOD_WP_MOVED_0 (1.3)
#define TELEMETRY_MODE_Main_ppm 1
#define PERIOD_PPM_1 (0.5)
#define PERIOD_RC_1 (0.5)
#define PERIOD_BOOZ_STATUS_1 (1)
#define TELEMETRY_MODE_Main_raw_sensors 2
#define PERIOD_BOOZ_STATUS_2 (1.2)
#define PERIOD_DL_VALUE_2 (0.5)
#define PERIOD_ALIVE_2 (2.1)
#define PERIOD_IMU_ACCEL_RAW_2 (.05)
#define PERIOD_IMU_GYRO_RAW_2 (.05)
#define PERIOD_IMU_MAG_RAW_2 (.05)
#define TELEMETRY_MODE_Main_scaled_sensors 3
#define PERIOD_BOOZ_STATUS_3 (1.2)
#define PERIOD_DL_VALUE_3 (0.5)
#define PERIOD_ALIVE_3 (2.1)
#define PERIOD_BOOZ2_GYRO_3 (.075)
#define PERIOD_BOOZ2_ACCEL_3 (.075)
#define PERIOD_BOOZ2_MAG_3 (.1)
#define TELEMETRY_MODE_Main_ahrs 4
#define PERIOD_BOOZ_STATUS_4 (1.2)
#define PERIOD_DL_VALUE_4 (0.5)
#define PERIOD_ALIVE_4 (2.1)
#define PERIOD_BOOZ2_FILTER_4 (.5)
#define PERIOD_BOOZ2_AHRS_EULER_4 (.1)
#define TELEMETRY_MODE_Main_rate_loop 5
#define PERIOD_BOOZ_STATUS_5 (1.2)
#define PERIOD_DL_VALUE_5 (0.5)
#define PERIOD_ALIVE_5 (2.1)
#define PERIOD_BOOZ2_RATE_LOOP_5 (.02)
#define TELEMETRY_MODE_Main_attitude_loop 6
#define PERIOD_BOOZ_STATUS_6 (1.2)
#define PERIOD_DL_VALUE_6 (0.5)
#define PERIOD_ALIVE_6 (0.9)
#define PERIOD_BOOZ2_STAB_ATTITUDE_6 (.03)
#define PERIOD_BOOZ2_STAB_ATTITUDE_REF_6 (.2)
#define TELEMETRY_MODE_Main_vert_loop 7
#define PERIOD_BOOZ_STATUS_7 (1.2)
#define PERIOD_DL_VALUE_7 (0.5)
#define PERIOD_ALIVE_7 (0.9)
#define PERIOD_BOOZ2_VERT_LOOP_7 (.05)
#define PERIOD_BOOZ2_INS_7 (.05)
#define PERIOD_BOOZ2_INS_REF_7 (5.1)
#define TELEMETRY_MODE_Main_h_loop 8
#define PERIOD_ALIVE_8 (0.9)
#define PERIOD_BOOZ2_HOVER_LOOP_8 (0.25)
#define PERIOD_BOOZ2_STAB_ATTITUDE_8 (.2)
#define PERIOD_BOOZ2_STAB_ATTITUDE_REF_8 (.2)
#define PERIOD_BOOZ2_FP_8 (0.25)
#define PERIOD_BOOZ_STATUS_8 (1.2)
#define PERIOD_BOOZ2_NAV_REF_8 (5.)
#define TELEMETRY_MODE_Main_aligner 9
#define PERIOD_ALIVE_9 (0.9)
#define PERIOD_BOOZ2_FILTER_ALIGNER_9 (0.02)
#define TELEMETRY_MODE_Main_hs_att_roll 10
#define PERIOD_BOOZ_STATUS_10 (1.2)
#define PERIOD_ALIVE_10 (0.9)
#define PERIOD_DL_VALUE_10 (0.5)
#define PERIOD_BOOZ2_STAB_ATTITUDE_HS_ROLL_10 (0.02)
#define TELEMETRY_MODE_Main_tune_hover 11
#define PERIOD_BOOZ2_TUNE_HOVER_11 (.05)
#define PeriodicSendMain() {  /* 60Hz */ \
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_default) {\
    static uint8_t i15; i15++; if (i15>=15) i15=0;\
    static uint8_t i66; i66++; if (i66>=66) i66=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    static uint8_t i78; i78++; if (i78>=78) i78=0;\
    static uint8_t i96; i96++; if (i96>=96) i96=0;\
    static uint8_t i126; i126++; if (i126>=126) i126=0;\
    static uint16_t i300; i300++; if (i300>=300) i300=0;\
    if (i15 == 0) {\
      PERIODIC_SEND_BOOZ2_FP();\
    } \
    if (i66 == 6) {\
      PERIODIC_SEND_DL_VALUE();\
    } \
    if (i72 == 12) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
    if (i78 == 18) {\
      PERIODIC_SEND_WP_MOVED();\
    } \
    if (i96 == 24) {\
      PERIODIC_SEND_BOOZ2_NAV_STATUS();\
    } \
    if (i126 == 30) {\
      PERIODIC_SEND_ALIVE();\
    } \
    if (i300 == 36) {\
      PERIODIC_SEND_BOOZ2_NAV_REF();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_ppm) {\
    static uint8_t i30; i30++; if (i30>=30) i30=0;\
    static uint8_t i60; i60++; if (i60>=60) i60=0;\
    if (i30 == 0) {\
      PERIODIC_SEND_PPM();\
    } \
    else if (i30 == 6) {\
      PERIODIC_SEND_RC();\
    } \
    if (i60 == 12) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_raw_sensors) {\
    static uint8_t i3; i3++; if (i3>=3) i3=0;\
    static uint8_t i30; i30++; if (i30>=30) i30=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    static uint8_t i126; i126++; if (i126>=126) i126=0;\
    if (i3 == 0) {\
      PERIODIC_SEND_IMU_ACCEL_RAW();\
    } \
    if (i3 == 0) {\
      PERIODIC_SEND_IMU_GYRO_RAW();\
    } \
    if (i3 == 0) {\
      PERIODIC_SEND_IMU_MAG_RAW();\
    } \
    if (i30 == 6) {\
      PERIODIC_SEND_DL_VALUE();\
    } \
    if (i72 == 12) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
    if (i126 == 18) {\
      PERIODIC_SEND_ALIVE();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_scaled_sensors) {\
    static uint8_t i4; i4++; if (i4>=4) i4=0;\
    static uint8_t i6; i6++; if (i6>=6) i6=0;\
    static uint8_t i30; i30++; if (i30>=30) i30=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    static uint8_t i126; i126++; if (i126>=126) i126=0;\
    if (i4 == 0) {\
      PERIODIC_SEND_BOOZ2_GYRO();\
    } \
    else if (i4 == 2) {\
      PERIODIC_SEND_BOOZ2_ACCEL();\
    } \
    if (i6 == 2) {\
      PERIODIC_SEND_BOOZ2_MAG();\
    } \
    if (i30 == 8) {\
      PERIODIC_SEND_DL_VALUE();\
    } \
    if (i72 == 14) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
    if (i126 == 20) {\
      PERIODIC_SEND_ALIVE();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_ahrs) {\
    static uint8_t i6; i6++; if (i6>=6) i6=0;\
    static uint8_t i30; i30++; if (i30>=30) i30=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    static uint8_t i126; i126++; if (i126>=126) i126=0;\
    if (i6 == 0) {\
      PERIODIC_SEND_BOOZ2_AHRS_EULER();\
    } \
    if (i30 == 6) {\
      PERIODIC_SEND_DL_VALUE();\
    } \
    else if (i30 == 12) {\
      PERIODIC_SEND_BOOZ2_FILTER();\
    } \
    if (i72 == 18) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
    if (i126 == 24) {\
      PERIODIC_SEND_ALIVE();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_rate_loop) {\
    static uint8_t i1; i1++; if (i1>=1) i1=0;\
    static uint8_t i30; i30++; if (i30>=30) i30=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    static uint8_t i126; i126++; if (i126>=126) i126=0;\
    if (i1 == 0) {\
      PERIODIC_SEND_BOOZ2_RATE_LOOP();\
    } \
    if (i30 == 6) {\
      PERIODIC_SEND_DL_VALUE();\
    } \
    if (i72 == 12) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
    if (i126 == 18) {\
      PERIODIC_SEND_ALIVE();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_attitude_loop) {\
    static uint8_t i1; i1++; if (i1>=1) i1=0;\
    static uint8_t i12; i12++; if (i12>=12) i12=0;\
    static uint8_t i30; i30++; if (i30>=30) i30=0;\
    static uint8_t i54; i54++; if (i54>=54) i54=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    if (i1 == 0) {\
      PERIODIC_SEND_BOOZ2_STAB_ATTITUDE();\
    } \
    if (i12 == 6) {\
      PERIODIC_SEND_BOOZ2_STAB_ATTITUDE_REF();\
    } \
    if (i30 == 12) {\
      PERIODIC_SEND_DL_VALUE();\
    } \
    if (i54 == 18) {\
      PERIODIC_SEND_ALIVE();\
    } \
    if (i72 == 24) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_vert_loop) {\
    static uint8_t i3; i3++; if (i3>=3) i3=0;\
    static uint8_t i30; i30++; if (i30>=30) i30=0;\
    static uint8_t i54; i54++; if (i54>=54) i54=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    static uint16_t i306; i306++; if (i306>=306) i306=0;\
    if (i3 == 0) {\
      PERIODIC_SEND_BOOZ2_VERT_LOOP();\
    } \
    if (i3 == 0) {\
      PERIODIC_SEND_BOOZ2_INS();\
    } \
    if (i30 == 6) {\
      PERIODIC_SEND_DL_VALUE();\
    } \
    if (i54 == 12) {\
      PERIODIC_SEND_ALIVE();\
    } \
    if (i72 == 18) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
    if (i306 == 24) {\
      PERIODIC_SEND_BOOZ2_INS_REF();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_h_loop) {\
    static uint8_t i12; i12++; if (i12>=12) i12=0;\
    static uint8_t i15; i15++; if (i15>=15) i15=0;\
    static uint8_t i54; i54++; if (i54>=54) i54=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    static uint16_t i300; i300++; if (i300>=300) i300=0;\
    if (i12 == 0) {\
      PERIODIC_SEND_BOOZ2_STAB_ATTITUDE();\
    } \
    else if (i12 == 6) {\
      PERIODIC_SEND_BOOZ2_STAB_ATTITUDE_REF();\
    } \
    if (i15 == 12) {\
      PERIODIC_SEND_BOOZ2_HOVER_LOOP();\
    } \
    else if (i15 == 3) {\
      PERIODIC_SEND_BOOZ2_FP();\
    } \
    if (i54 == 9) {\
      PERIODIC_SEND_ALIVE();\
    } \
    if (i72 == 15) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
    if (i300 == 21) {\
      PERIODIC_SEND_BOOZ2_NAV_REF();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_aligner) {\
    static uint8_t i1; i1++; if (i1>=1) i1=0;\
    static uint8_t i54; i54++; if (i54>=54) i54=0;\
    if (i1 == 0) {\
      PERIODIC_SEND_BOOZ2_FILTER_ALIGNER();\
    } \
    if (i54 == 6) {\
      PERIODIC_SEND_ALIVE();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_hs_att_roll) {\
    static uint8_t i1; i1++; if (i1>=1) i1=0;\
    static uint8_t i30; i30++; if (i30>=30) i30=0;\
    static uint8_t i54; i54++; if (i54>=54) i54=0;\
    static uint8_t i72; i72++; if (i72>=72) i72=0;\
    if (i1 == 0) {\
      PERIODIC_SEND_BOOZ2_STAB_ATTITUDE_HS_ROLL();\
    } \
    if (i30 == 6) {\
      PERIODIC_SEND_DL_VALUE();\
    } \
    if (i54 == 12) {\
      PERIODIC_SEND_ALIVE();\
    } \
    if (i72 == 18) {\
      PERIODIC_SEND_BOOZ_STATUS();\
    } \
  }\
  if (telemetry_mode_Main == TELEMETRY_MODE_Main_tune_hover) {\
    static uint8_t i3; i3++; if (i3>=3) i3=0;\
    if (i3 == 0) {\
      PERIODIC_SEND_BOOZ2_TUNE_HOVER();\
    } \
  }\
}
