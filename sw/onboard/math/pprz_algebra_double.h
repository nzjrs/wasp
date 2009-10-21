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
#ifndef PPRZ_ALGEBRA_DOUBLE_H
#define PPRZ_ALGEBRA_DOUBLE_H

#include "pprz_algebra.h"

struct DoubleVect2 {
  float x;
  float y;
};

struct DoubleVect3 {
  float x;
  float y;
  float z;
};

struct DoubleQuat {
  float qi;
  float qx;
  float qy;
  float qz;
};

struct DoubleMat33 {
  float m[3*3];
};

struct DoubleEulers {
  float phi;
  float theta;
  float psi;
};

struct DoubleRates {
  float p;
  float q;
  float r;
};



/* multiply _vin by _mat, store in _vout */
#define DOUBLE_MAT33_VECT3_MUL(_vout, _mat, _vin) {		\
    (_vout).x = (_mat)[0]*(_vin).x + (_mat)[1]*(_vin).y + (_mat)[2]*(_vin).z;	\
    (_vout).y = (_mat)[3]*(_vin).x + (_mat)[4]*(_vin).y + (_mat)[5]*(_vin).z;	\
    (_vout).z = (_mat)[6]*(_vin).x + (_mat)[7]*(_vin).y + (_mat)[8]*(_vin).z;	\
  }

/* multiply _vin by the transpose of _mat, store in _vout */
#define DOUBLE_MAT33_VECT3_TRANSP_MUL(_vout, _mat, _vin) {		\
    (_vout).x = (_mat)[0]*(_vin).x + (_mat)[3]*(_vin).y + (_mat)[6]*(_vin).z;	\
    (_vout).y = (_mat)[1]*(_vin).x + (_mat)[4]*(_vin).y + (_mat)[7]*(_vin).z;	\
    (_vout).z = (_mat)[2]*(_vin).x + (_mat)[5]*(_vin).y + (_mat)[8]*(_vin).z;	\
  }


#endif /* PPRZ_ALGEBRA_DOUBLE_H */
