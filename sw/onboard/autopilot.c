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
#include "autopilot.h"
#include "generated/settings.h"

#define TRESHOLD_1_PPRZ (MIN_PPRZ / 2)
#define TRESHOLD_2_PPRZ (MAX_PPRZ / 2)

AutopilotMode_t autopilot_mode_of_radio(pprz_t rc)
{
    if (rc > TRESHOLD_2_PPRZ)
        return autopilot.mode_auto2;
    else if (rc > TRESHOLD_1_PPRZ)
        return AUTOPILOT_MODE_AUTO1;
    else
        return AUTOPILOT_MODE_MANUAL;
}

void autopilot_kill(void)
{
    autopilot_set_mode(AP_MODE_KILL);
}
