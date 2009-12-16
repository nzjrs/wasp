
#include <glib.h>

#include "math/tests/test_support.h"
#include "math/pprz_algebra_double.h"

void math_pprz_algebra_square_tc( void )
{
	g_assert_cmpint( 36, ==, SQUARE(6) );
	g_assert_cmpdelta( 36.0, SQUARE( 6.00 ), EPSILON );
}


typedef struct {
	struct DoubleVect2 a;
	struct DoubleVect2 b;
} math_pprz_algebra_vect2_fixture;

void math_pprz_algebra_vect2_fixture_setup( math_pprz_algebra_vect2_fixture *fix,
                      		    gconstpointer test_data )
{
	fix->a.x = 1.0;
	fix->a.y = 1.0;
	
	fix->b.x = 5.0;
	fix->b.y = 5.0;
}

void math_pprz_algebra_vect2_fixture_teardown( math_pprz_algebra_vect2_fixture *fix,
                                    gconstpointer test_data )
{
        ;
}

void math_pprz_algebra_vect2_tc( math_pprz_algebra_vect2_fixture *fix, gconstpointer test_data )
{
	VECT2_ASSIGN( fix->a, 3.0, 4.5 );
	g_assert_cmpfloat( fix->a.x, ==, 3.0 );
	g_assert_cmpfloat( fix->a.y, ==, 4.5 );
}

/*
T2_ASSIGN(_a, _x, _y) {              \
    (_a).x = (_x);                              \
    (_a).y = (_y);                              \
  }

#define VECT2_COPY(_a, _b) {                    \
    (_a).x = (_b).x;                            \
    (_a).y = (_b).y;                            \
  }

#define VECT2_ADD(_a, _b) {                     \
    (_a).x += (_b).x;                           \
    (_a).y += (_b).y;                           \
  }

#define VECT2_SUB(_a, _b) {                     \
    (_a).x -= (_b).x;                           \
    (_a).y -= (_b).y;                           \
  }

#define VECT2_SUM(_c, _a, _b) {                 \
    (_c).x = (_a).x + (_b).x;                   \
    (_c).y = (_a).y + (_b).y;                   \
  }

#define VECT2_DIFF(_c, _a, _b) {                \
    (_c).x = (_a).x - (_b).x;                   \
    (_c).y = (_a).y - (_b).y;                   \
  }

#define VECT2_SMUL(_vo, _vi, _s) {              \
    (_vo).x =  (_vi).x * (_s);                  \
    (_vo).y =  (_vi).y * (_s);                  \
  }

#define VECT2_SDIV(_vo, _vi, _s) {              \
    (_vo).x =  (_vi).x / (_s);                  \
    (_vo).y =  (_vi).y / (_s);                  \
  }

#define VECT2_STRIM(_v, _min, _max) {                                   \
    (_v).x = (_v).x < _min ? _min : (_v).x > _max ? _max : (_v).x;      \
    (_v).y = (_v).y < _min ? _min : (_v).y > _max ? _max : (_v).y;      \
  }
*/
