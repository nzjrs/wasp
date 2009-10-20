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
/* This file has been generated from /home/john/Programming/paparazzi.git/conf/flight_plans/booz_test_1.xml */
/* Please DO NOT EDIT */

#ifndef FLIGHT_PLAN_H
#define FLIGHT_PLAN_H 

#include "std.h"
#define FLIGHT_PLAN_NAME "booz test 1"
#define NAV_UTM_EAST0 418964
#define NAV_UTM_NORTH0 5412633
#define NAV_UTM_ZONE0 31
#define NAV_LAT0 488613611
#define NAV_LON0 18951387
#define QFU 0.0
#define WP_dummy 0
#define WP_D1 1
#define WP_HOME 2
#define WP_D2 3
#define WP_p1 4
#define WP_p2 5
#define WP_p3 6
#define WP_p4 7
#define WP_p5 8
#define WP_p6 9
#define WAYPOINTS { \
 {42.0, 42.0, 250},\
 {-18.2, -24.6, 1.5},\
 {0.0, 0.0, 1.5},\
 {-53.7, -45.6, 1.5},\
 {-72.8, -70.0, 1.5},\
 {-132.2, -118.5, 1.5},\
 {-76.0, -137.9, 1.5},\
 {0.0, 100.0, 3.},\
 {100.0, 0.0, 6.},\
 {100.0, 100.0, 9.},\
};
#define WAYPOINTS_INT32 { \
 {10752, 10752, 64000},\
 {-4659, -6297, 384},\
 {0, 0, 384},\
 {-13747, -11673, 384},\
 {-18636, -17920, 384},\
 {-33843, -30336, 384},\
 {-19456, -35302, 384},\
 {0, 25600, 768},\
 {25600, 0, 1536},\
 {25600, 25600, 2304},\
};
#define NB_WAYPOINT 10
#define NB_BLOCK 8
#define GROUND_ALT 0.
#define GROUND_ALT_CM 0
#define SECURITY_HEIGHT 1.
#define SECURITY_ALT 1.
#define MAX_DIST_FROM_HOME 400.
#ifdef NAV_C

static inline void auto_nav(void) {
  switch (nav_block) {
    Block(0) // Geo init
    ; // pre_call
    switch(nav_stage) {
      Stage(0)
        NextBlock();
        break;
    }
    ; // post_call
    break;

    Block(1) // stay_p1
    ; // pre_call
    switch(nav_stage) {
      Stage(0)
        if (NavApproaching(4,CARROT)) NextStageAndBreakFrom(4) else {
          NavGotoWaypoint(4);
          NavVerticalAutoThrottleMode(RadOfDeg(0.000000));
          NavVerticalAltitudeMode(WaypointAlt(4), 0.);
        }
        break;
      Stage(1)
        NextBlock();
        break;
    }
    ; // post_call
    break;

    Block(2) // stay_p2
    ; // pre_call
    switch(nav_stage) {
      Stage(0)
        NavGotoWaypoint(5);
        NavVerticalAutoThrottleMode(RadOfDeg(0.000000));
        NavVerticalAltitudeMode(WaypointAlt(5), 0.);
        break;
      Stage(1)
        NextBlock();
        break;
    }
    ; // post_call
    break;

    Block(3) // stay_p4
    ; // pre_call
    switch(nav_stage) {
      Stage(0)
        NavGotoWaypoint(7);
        NavVerticalAutoThrottleMode(RadOfDeg(0.000000));
        NavVerticalAltitudeMode(WaypointAlt(7), 0.);
        break;
      Stage(1)
        NextBlock();
        break;
    }
    ; // post_call
    break;

    Block(4) // stay_p5
    ; // pre_call
    switch(nav_stage) {
      Stage(0)
        NavGotoWaypoint(8);
        NavVerticalAutoThrottleMode(RadOfDeg(0.000000));
        NavVerticalAltitudeMode(WaypointAlt(8), 0.);
        break;
      Stage(1)
        NextBlock();
        break;
    }
    ; // post_call
    break;

    Block(5) // line
    ; // pre_call
    switch(nav_stage) {
      Stage(0)
        if (NavApproachingFrom(9,8,CARROT)) NextStageAndBreakFrom(9) else {
          NavSegment(8, 9);
          NavVerticalAutoThrottleMode(RadOfDeg(0.000000));
          NavVerticalAltitudeMode(WaypointAlt(9), 0.);
        }
        break;
      Stage(1)
        NextBlock();
        break;
    }
    ; // post_call
    break;

    Block(6) // stay_p6
    ; // pre_call
    switch(nav_stage) {
      Stage(0)
        NavGotoWaypoint(9);
        NavVerticalAutoThrottleMode(RadOfDeg(0.000000));
        NavVerticalAltitudeMode(WaypointAlt(9), 0.);
        break;
      Stage(1)
        NextBlock();
        break;
    }
    ; // post_call
    break;

    Block(7) // HOME
    ; // pre_call
    switch(nav_stage) {
      Stage(0)
        nav_home();
        break;
      Stage(1)
        NextBlock();
        break;
    }
    ; // post_call
    break;

  }
}
#endif // NAV_C

#endif // FLIGHT_PLAN_H
