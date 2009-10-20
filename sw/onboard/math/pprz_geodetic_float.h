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
#ifndef PPRZ_GEODETIC_FLOAT_H
#define PPRZ_GEODETIC_FLOAT_H

#include "pprz_geodetic.h"
#include "pprz_algebra_float.h"

/* Earth Centered Earth Fixed in meters */
struct EcefCoor_f {
  float x;
  float y;
  float z;
};

/* lon, lat in radians */
/* alt in meters       */
struct LlaCoor_f {
  float lon;
  float lat;
  float alt;
};

/* North East Down local tangeant plane */
struct NedCoor_f {
  float x;
  float y;
  float z;
};

/* East North Down local tangeant plane */
struct EnuCoor_f {
  float x;
  float y;
  float z;
};

/* Local tangeant plane reference */
struct LtpDef_f {
  struct EcefCoor_f ecef;
  struct LlaCoor_f  lla;
  struct FloatMat33 ltp_of_ecef;
};

extern void ltp_def_from_ecef_f(struct LtpDef_f* def, struct EcefCoor_f* ecef);
//extern void ltp_def_from_lla_f(struct LtpDef_f* def, struct LlaCoor_f* lla);
extern void lla_of_ecef_f(struct LlaCoor_f* out, struct EcefCoor_f* in);
extern void ecef_of_lla_f(struct EcefCoor_f* out, struct LlaCoor_f* in);
extern void enu_of_ecef_point_f(struct EnuCoor_f* enu, struct LtpDef_f* def, struct EcefCoor_f* ecef);
extern void ned_of_ecef_point_f(struct NedCoor_f* ned, struct LtpDef_f* def, struct EcefCoor_f* ecef);
extern void enu_of_ecef_vect_f(struct EnuCoor_f* enu, struct LtpDef_f* def, struct EcefCoor_f* ecef);
extern void ned_of_ecef_vect_f(struct NedCoor_f* ned, struct LtpDef_f* def, struct EcefCoor_f* ecef);

/*  not enought precision with floats - used the double version */
#if 0
extern void ecef_of_enu_point_f(struct EcefCoor_f* ecef, struct LtpDef_f* def, struct EnuCoor_f* enu);
extern void ecef_of_ned_point_f(struct EcefCoor_f* ecef, struct LtpDef_f* def, struct NedCoor_f* ned);
extern void ecef_of_enu_vect_f(struct EcefCoor_f* ecef, struct LtpDef_f* def, struct EnuCoor_f* enu);
extern void ecef_of_ned_vect_f(struct EcefCoor_f* ecef, struct LtpDef_f* def, struct NedCoor_f* ned);
#endif


#endif /* PPRZ_GEODETIC_FLOAT_H */
