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
#include "std.h"
#include "settings.h"

static uint8_t settings_init_ok;

bool_t
settings_init(void)
{
    settings_init_ok = FALSE;
    return settings_init_ok;
}

bool_t
settings_load(uint8_t id, Type_t *type, void *data)
{
    return FALSE;
}

bool_t
settings_save(uint8_t id, Type_t type, void *data)
{
    return FALSE;
}

