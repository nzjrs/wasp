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

