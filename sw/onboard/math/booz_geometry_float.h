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

