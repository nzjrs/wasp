#ifndef SETTINGS_H
#define SETTINGS_H

#include "std.h"

void
settings_init(void);

bool_t
settings_get(uint8_t id, Type_t *type, void *data);

bool_t
settings_set(uint8_t id, Type_t type, void *data);

#endif


