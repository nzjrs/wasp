#ifndef GPS_H
#define GPS_H

#include "std.h"
#include "config/config.h"
#include "math/pprz_geodetic_int.h"

typedef enum {
    GPS_FIX_NONE,
    GPS_FIX_2D,
    GPS_FIX_3D,
} GpsFix_t;

struct Booz_gps_state {
  struct EcefCoor_i ecef_pos;    /* pos ECEF in cm        */
  struct EcefCoor_i ecef_speed;  /* speed ECEF in cm/s    */
  uint32_t pacc;                 /* position accuracy     */
  uint32_t sacc;                 /* speed accuracy        */
  uint16_t pdop;                 /* dilution of precision */
  uint8_t  num_sv;               /* number of sat in fix  */
  GpsFix_t fix;                  /* status of fix         */
  /* UBX NAV POSLLH */
  int32_t  booz2_gps_lon;
  int32_t  booz2_gps_lat;
  int32_t  booz2_gps_hmsl;       /* height above mean seal level (mm)   */
  uint32_t booz2_gps_vacc;       /* vertical accuracy (mm)              */
  uint32_t booz2_gps_hacc;       /* horizontal accuracy (mm)            */
  /* UBX NAV VELNED */
  int32_t  booz2_gps_vel_n;
  int32_t  booz2_gps_vel_e;
};

extern 
struct Booz_gps_state booz_gps_state;

void 
gps_init(void);

/**
 * return true if a gps packet has been processed
 */
bool_t
gps_event_task(void);

#endif /* BOOZ2_GPS_H */


