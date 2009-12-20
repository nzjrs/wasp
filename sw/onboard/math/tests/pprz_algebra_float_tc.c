
#include <glib.h>

#include "math/tests/test_support.h"
#include "math/pprz_algebra_float.h"

static void math_pprz_algebra_square_tc( void )
{
	g_assert_cmpint( 36, ==, SQUARE(6) );
	g_assert_cmpdelta( 36.0, SQUARE( 6.00 ), EPSILON );
}

static const float AX = 1.0;
static const float AY = 1.0;

static const float BX = 2.0;
static const float BY = 5.0;

typedef struct {
	struct FloatVect2 a;
	struct FloatVect2 b;
} math_pprz_algebra_float_vect2_fixture;

static void math_pprz_algebra_float_vect2_fixture_setup( math_pprz_algebra_float_vect2_fixture *fix,
                      		    gconstpointer test_data )
{
	fix->a.x = AX;
	fix->a.y = AY;
	
	fix->b.x = BX;
	fix->b.y = BY;
}

static void math_pprz_algebra_float_vect2_fixture_teardown( math_pprz_algebra_float_vect2_fixture *fix,
                                    gconstpointer test_data )
{
}

static void math_pprz_algebra_float_vect2_fixture_tc( math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{
        g_assert_cmpfloat( fix->a.x, ==, AX );
        g_assert_cmpfloat( fix->a.y, ==, AY );
        g_assert_cmpfloat( fix->b.x, ==, BX );
        g_assert_cmpfloat( fix->b.y, ==, BY );
}

static void math_pprz_algebra_float_vect2_assign_tc( math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{
	VECT2_ASSIGN( fix->a, 3.0, 4.5 );
	g_assert_cmpfloat( fix->a.x, ==, 3.0 );
	g_assert_cmpfloat( fix->a.y, ==, 4.5 );
}

static void math_pprz_algebra_float_vect2_copy_tc( math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{

        VECT2_COPY( fix->a, fix->b );
        g_assert_cmpfloat( fix->a.x, ==, BX );
        g_assert_cmpfloat( fix->a.y, ==, BY );
        g_assert_cmpfloat( fix->b.x, ==, BX );
        g_assert_cmpfloat( fix->b.y, ==, BY );
}

static void math_pprz_algebra_float_vect2_add_tc( math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{

        VECT2_ADD( fix->a, fix->b );
        g_assert_cmpfloat( fix->a.x, ==, AX+BX );
        g_assert_cmpfloat( fix->a.y, ==, AY+BY );
        g_assert_cmpfloat( fix->b.x, ==, BX );
        g_assert_cmpfloat( fix->b.y, ==, BY );
}

static void math_pprz_algebra_float_vect2_sub_tc(  math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{
        VECT2_ADD( fix->a, fix->b );
	g_assert_cmpdelta( fix->a.x, AX-BX, EPSILON );
	g_assert_cmpdelta( fix->a.y, AY-BY, EPSILON );
	g_assert_cmpfloat( fix->b.x, ==, BX );
	g_assert_cmpfloat( fix->b.y, ==, BY );
}

static void math_pprz_algebra_float_vect2_sum_tc(  math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{
	struct FloatVect2 c;
	c.x = 0.0;
	c.y = 0.0;	

	VECT2_SUM( c, fix->a, fix->b );
        g_assert_cmpfloat( fix->a.x, ==, AX );
        g_assert_cmpfloat( fix->a.y, ==, AY );
        g_assert_cmpfloat( fix->b.x, ==, BX );
        g_assert_cmpfloat( fix->b.y, ==, BY );
	g_assert_cmpfloat( c.x, ==, AX+BX );
	g_assert_cmpfloat( c.y, ==, AY+BY );
}

static void math_pprz_algebra_float_vect2_diff_tc(  math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{
        struct FloatVect2 c;
        c.x = 0.0;
        c.y = 0.0;

        VECT2_DIFF( c, fix->a, fix->b );
        g_assert_cmpfloat( fix->a.x, ==, AX );
        g_assert_cmpfloat( fix->a.y, ==, AY );
        g_assert_cmpfloat( fix->b.x, ==, BX );
        g_assert_cmpfloat( fix->b.y, ==, BY );
        g_assert_cmpfloat( c.x, ==, AX-BX );
        g_assert_cmpfloat( c.y, ==, AY-BY );
}

static void math_pprz_albebra_float_vect2_smul_tc( math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{
        struct FloatVect2 c;
        c.x = 0.0;
        c.y = 0.0;
	const float SCALE = 6.5;

	VECT2_SMUL( c, fix->a, SCALE );
	g_assert_cmpdelta( c.x, fix->a.x*SCALE, EPSILON );
	g_assert_cmpdelta( c.y, fix->a.y*SCALE, EPSILON );

        g_assert_cmpfloat( fix->a.x, ==, AX );
        g_assert_cmpfloat( fix->a.y, ==, AY );
}


static void math_pprz_albebra_float_vect2_sdiv_tc( math_pprz_algebra_float_vect2_fixture *fix, gconstpointer test_data )
{
        struct FloatVect2 c;
        c.x = 0.0;
        c.y = 0.0;
        const float SCALE = 6.5;

        VECT2_SDIV( c, fix->a, SCALE );
        g_assert_cmpdelta( c.x, fix->a.x/SCALE, EPSILON );
        g_assert_cmpdelta( c.y, fix->a.y/SCALE, EPSILON );

        g_assert_cmpfloat( fix->a.x, ==, AX );
        g_assert_cmpfloat( fix->a.y, ==, AY );
}

static void  math_pprz_albebra_float_vect2_strim_tc( void )
{
	struct FloatVect2 c;
	c.x = 1.0;
	c.y = 6.0;

	const float MIN = 3.0;
	const float MAX = 4.0;

	VECT2_STRIM( c, MIN, MAX );
	g_assert_cmpfloat( c.x, >=, MIN );
	g_assert_cmpfloat( c.x, <=, MAX );
	
	g_assert_cmpfloat( c.y, >=, MIN );
	g_assert_cmpfloat( c.y, <=, MAX );
}
