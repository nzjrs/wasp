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
#ifndef PPRZ_GEODETIC_DOUBLE_H
#define PPRZ_GEODETIC_DOUBLE_H

#include "pprz_geodetic.h"
#include "pprz_algebra_double.h"

/* Earth Centered Earth Fixed in meters */
struct EcefCoor_d {
  double x;
  double y;
  double z;
};

/* lon, lat in radians */
/* alt in meters       */
struct LlaCoor_d {
  double lon;
  double lat;
  double alt;
};

/* North East Down local tangeant plane */
struct NedCoor_d {
  double x;
  double y;
  double z;
};

/* East North Down local tangeant plane */
struct EnuCoor_d {
  double x;
  double y;
  double z;
};

/* Local tangeant plane reference */
struct LtpDef_d {
  struct EcefCoor_d  ecef;
  struct LlaCoor_d   lla;
  struct DoubleMat33 ltp_of_ecef;
};

extern void ltp_def_from_ecef_d(struct LtpDef_d* def, struct EcefCoor_d* ecef);
extern void lla_of_ecef_d(struct LlaCoor_d* out, struct EcefCoor_d* in);
extern void ecef_of_lla_d(struct EcefCoor_d* out, struct LlaCoor_d* in);

extern void enu_of_ecef_point_d(struct EnuCoor_d* ned, struct LtpDef_d* def, struct EcefCoor_d* ecef);
extern void ned_of_ecef_point_d(struct NedCoor_d* ned, struct LtpDef_d* def, struct EcefCoor_d* ecef);

extern void enu_of_ecef_vect_d(struct EnuCoor_d* ned, struct LtpDef_d* def, struct EcefCoor_d* ecef);
extern void ned_of_ecef_vect_d(struct NedCoor_d* ned, struct LtpDef_d* def, struct EcefCoor_d* ecef);

extern void ecef_of_enu_point_d(struct EcefCoor_d* ecef, struct LtpDef_d* def, struct EnuCoor_d* enu);
extern void ecef_of_ned_point_d(struct EcefCoor_d* ecef, struct LtpDef_d* def, struct NedCoor_d* ned);

extern void ecef_of_enu_vect_d(struct EcefCoor_d* ecef, struct LtpDef_d* def, struct EnuCoor_d* enu);
extern void ecef_of_ned_vect_d(struct EcefCoor_d* ecef, struct LtpDef_d* def, struct NedCoor_d* ned);



#endif /* PPRZ_GEODETIC_DOUBLE_H */
