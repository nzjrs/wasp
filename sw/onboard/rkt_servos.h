/*  
 * Written by the rocket project team "Flying Kiwi" 2009
 */

/** \file rkt_servos.h
 *  \brief API for the servos on the rocket
 *
 */
#ifndef RKT_SERVOS_H
#define RKT_SERVOS_H

#include "std.h"

typedef uint8_t ServoID_t;

void servos_init( void );

void servos_set_speed( ServoID_t id, uint16_t pos, uint16_t speed );

/**
 * The servo will go to the specified position when this function is executed
 */
void servos_set_position( ServoID_t id, uint16_t value );


#endif /* RKT_SERVOS_H */
