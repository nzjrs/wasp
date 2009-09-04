#ifndef BOOZ2_SUPERVISION_H
#define BOOZ2_SUPERVISION_H

#include "config/airframe.h"

#define FRONT   0
#define BACK    1
#define RIGHT   2
#define LEFT    3

#if defined SUPERVISION_FRONT_ROTOR_CW
#define TRIM_FRONT ( SUPERVISION_TRIM_E-SUPERVISION_TRIM_R)
#define TRIM_RIGHT (-SUPERVISION_TRIM_A+SUPERVISION_TRIM_R)
#define TRIM_BACK  (-SUPERVISION_TRIM_E-SUPERVISION_TRIM_R)
#define TRIM_LEFT  ( SUPERVISION_TRIM_A+SUPERVISION_TRIM_R)
#define SUPERVISION_MIX(_mot_cmd, _da, _de, _dr, _dt) {		\
    _mot_cmd[FRONT] = _dt + _de - _dr + TRIM_FRONT;	\
    _mot_cmd[RIGHT] = _dt - _da + _dr + TRIM_RIGHT;	\
    _mot_cmd[BACK]  = _dt - _de - _dr + TRIM_BACK;	\
    _mot_cmd[LEFT]  = _dt + _da + _dr + TRIM_LEFT;	\
  }
#else
#define TRIM_FRONT ( SUPERVISION_TRIM_E+SUPERVISION_TRIM_R)
#define TRIM_RIGHT (-SUPERVISION_TRIM_A-SUPERVISION_TRIM_R)
#define TRIM_BACK  (-SUPERVISION_TRIM_E+SUPERVISION_TRIM_R)
#define TRIM_LEFT  ( SUPERVISION_TRIM_A-SUPERVISION_TRIM_R)
#define SUPERVISION_MIX(_mot_cmd, _da, _de, _dr, _dt) {		\
    _mot_cmd[FRONT] = _dt + _de + _dr + TRIM_FRONT;	\
    _mot_cmd[RIGHT] = _dt - _da - _dr + TRIM_RIGHT;	\
    _mot_cmd[BACK]  = _dt - _de + _dr + TRIM_BACK;	\
    _mot_cmd[LEFT]  = _dt + _da - _dr + TRIM_LEFT;	\
  }
#endif

#define SUPERVISION_FIND_MAX_MOTOR(_mot_cmd, _max_mot) {	\
    _max_mot = (-32767-1); /* INT16_MIN;*/			\
    if (_mot_cmd[FRONT] > _max_mot)			\
      max_mot = _mot_cmd[FRONT];				\
    if (_mot_cmd[RIGHT] > _max_mot)			\
      max_mot = _mot_cmd[RIGHT];				\
    if (_mot_cmd[BACK] > _max_mot)			\
      max_mot = _mot_cmd[BACK];				\
    if (_mot_cmd[LEFT] > _max_mot)			\
      max_mot = _mot_cmd[LEFT];				\
  }

#define SUPERVISION_FIND_MIN_MOTOR(_mot_cmd, _min_mot) {	\
    _min_mot = (32767); /*INT16_MAX;*/				\
    if (_mot_cmd[FRONT] < _min_mot)			\
      min_mot = _mot_cmd[FRONT];				\
    if (_mot_cmd[RIGHT] < _min_mot)			\
      min_mot = _mot_cmd[RIGHT];				\
    if (_mot_cmd[BACK] < _min_mot)			\
      min_mot = _mot_cmd[BACK];				\
    if (_mot_cmd[LEFT] < _min_mot)			\
      min_mot = _mot_cmd[LEFT];				\
  }

#define SUPERVISION_OFFSET_MOTORS(_mot_cmd, _offset) {	\
    _mot_cmd[FRONT] += _offset;			\
    _mot_cmd[RIGHT] += _offset;			\
    _mot_cmd[BACK]  += _offset;			\
    _mot_cmd[LEFT]  += _offset;			\
  }

#define SUPERVISION_BOUND_MOTORS(_mot_cmd) {				\
    Bound(_mot_cmd[FRONT], SUPERVISION_MIN_MOTOR, SUPERVISION_MAX_MOTOR); \
    Bound(_mot_cmd[RIGHT], SUPERVISION_MIN_MOTOR, SUPERVISION_MAX_MOTOR); \
    Bound(_mot_cmd[BACK] , SUPERVISION_MIN_MOTOR, SUPERVISION_MAX_MOTOR); \
    Bound(_mot_cmd[LEFT] , SUPERVISION_MIN_MOTOR, SUPERVISION_MAX_MOTOR); \
  }


#define BOOZ2_SUPERVISION_RUN(_out, _in,_motors_on) {			\
    if (_motors_on) {							\
      SUPERVISION_MIX(_out, _in[COMMAND_ROLL], _in[COMMAND_PITCH], _in[COMMAND_YAW], _in[COMMAND_THRUST]); \
      pprz_t min_mot;							\
      SUPERVISION_FIND_MIN_MOTOR(_out, min_mot);			\
      if (min_mot < SUPERVISION_MIN_MOTOR) {				\
	pprz_t offset = -(min_mot - SUPERVISION_MIN_MOTOR);		\
	SUPERVISION_OFFSET_MOTORS(_out, offset) ;			\
      }									\
      pprz_t max_mot;							\
      SUPERVISION_FIND_MAX_MOTOR(_out, max_mot);			\
      if (max_mot > SUPERVISION_MAX_MOTOR) {				\
	pprz_t offset = -(max_mot - SUPERVISION_MAX_MOTOR);		\
	SUPERVISION_OFFSET_MOTORS(_out, offset) ;			\
      }									\
      SUPERVISION_BOUND_MOTORS(_out);					\
    }									\
    else {								\
      _out[FRONT] = 0;						\
      _out[RIGHT] = 0;						\
      _out[BACK]  = 0;						\
      _out[LEFT]  = 0;						\
    }									\
  }




#endif /* BOOZ2_SUPERVISION_H */
