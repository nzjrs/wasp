#ifndef BOOZ_GEOMETRY_FLOAT_H
#define BOOZ_GEOMETRY_FLOAT_H

#include <math.h>

#ifndef RadOfDeg
#define RadOfDeg(d) ( (d)*M_PI/180. )
#define DegOfRad(r) ( (r)/M_PI*180. )
#endif

#if 0
struct booz_fquat {
  float qi;
  float qx;
  float qy;
  float qz;
};

struct booz_fvect {
  float x;
  float y;
  float z;
};

struct booz_feuler {
  float phi;
  float theta;
  float psi;
};
#endif




#if 0
#define BOOZ_FEULER_OF_QUAT_ALT(e,q) {					\
    const float qi2 = q.qi*q.qi;					\
    const float qx2 = q.qx*q.qx;					\
    const float qy2 = q.qy*q.qy;					\
    const float qz2 = q.qz*q.qz;					\
    const float qiqx = q.qi*q.qx;					\
    const float qiqy = q.qi*q.qy;					\
    const float qiqz = q.qi*q.qz;					\
    const float qxqy = q.qx*q.qy;					\
    const float qxqz = q.qx*q.qz;					\
    const float qyqz = q.qy*q.qz;					\
    e.phi   =  atan2( 2.*(qiqx + qyqz), qi2-qx2-qy2+qz2 );		\
    e.theta =  asin( 2.*(qiqy - qxqz ));				\
    e.psi   =  atan2( 2.*(qiqz + qxqy), qi2+qx2-qy2-qz2 );		\
  }
#endif

#if 0
#define BOOZ_FEULER_ASSIGN_DEG(e, _phi, _theta, _psi) {			\
    BOOZ_FEULER_ASSIGN(e, RadOfDeg(_phi), RadOfDeg(_theta), RadOfDeg(_psi)); \
  }
#endif

#endif /* BOOZ_GEOMETRY_FLOAT_H */

