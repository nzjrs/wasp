
#include <glib.h>

#include "math/tests/test_support.h"
#include "math/pprz_algebra_double.h"

static void math_pprz_algebra_square_tc( void )
{
	g_assert_cmpint( 36, ==, SQUARE(6) );
	g_assert_cmpdelta( 36.0, SQUARE( 6.00 ), EPSILON );
}

static const double AX = 1.0;
static const double AY = 1.0;
static const double AZ = -5.5;

static const double BX = 2.0;
static const double BY = 5.0;
static const double BZ = 13.0;

typedef struct {
	struct DoubleVect2 a;
	struct DoubleVect2 b;
} math_pprz_algebra_double_vect2_fixture;

static void math_pprz_algebra_double_vect2_fixture_setup( math_pprz_algebra_double_vect2_fixture *fix,
                      		    gconstpointer test_data )
{
	fix->a.x = AX;
	fix->a.y = AY;
	
	fix->b.x = BX;
	fix->b.y = BY;
}

static void math_pprz_algebra_double_vect2_fixture_teardown( math_pprz_algebra_double_vect2_fixture *fix,
                                    gconstpointer test_data )
{
	;
}

/*
 * Test functions for the 2-vector functions from pprz_algebra.h
 */
static void math_pprz_algebra_double_vect2_fixture_tc( math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{
	G_ASSERT_VECT2_CMPFLOAT( fix->a, ==, AX, AY );
	G_ASSERT_VECT2_CMPFLOAT( fix->b, ==, BX, BY );
}

static void math_pprz_algebra_double_vect2_assign_tc( math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{
	VECT2_ASSIGN( fix->a, 3.0, 4.5 );
	G_ASSERT_VECT2_CMPFLOAT( fix->a, ==, 3.0, 4.5 );
}

static void math_pprz_algebra_double_vect2_copy_tc( math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{

        VECT2_COPY( fix->a, fix->b );
	G_ASSERT_VECT2_CMPFLOAT( fix->a, ==, BX, BY );
	G_ASSERT_VECT2_CMPFLOAT( fix->b, ==, BX, BY );
}

static void math_pprz_algebra_double_vect2_add_tc( math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{

        VECT2_ADD( fix->a, fix->b );

	G_ASSERT_VECT2_CMPFLOAT( fix->a, ==, AX+BX, AY+BY );
        G_ASSERT_VECT2_CMPFLOAT( fix->b, ==, BX, BY );
}

static void math_pprz_algebra_double_vect2_sub_tc(  math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{
        VECT2_SUB( fix->a, fix->b );

	G_ASSERT_VECT2_CMPDELTA( fix->a, AX-BX, AY-BY, EPSILON );
	G_ASSERT_VECT2_CMPFLOAT( fix->b, ==, BX, BY );
}

static void math_pprz_algebra_double_vect2_sum_tc(  math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{
	struct DoubleVect2 c;
	c.x = 0.0;
	c.y = 0.0;	

	VECT2_SUM( c, fix->a, fix->b );

	G_ASSERT_VECT2_CMPFLOAT( fix->a, ==, AX, AY );
	G_ASSERT_VECT2_CMPFLOAT( fix->b, ==, BX, BY );

	G_ASSERT_VECT2_CMPFLOAT( c, ==, AX+BX, AY+BY );
}

static void math_pprz_algebra_double_vect2_diff_tc(  math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect2 c;
        c.x = 0.0;
        c.y = 0.0;

        VECT2_DIFF( c, fix->a, fix->b );

        G_ASSERT_VECT2_CMPFLOAT( fix->a, ==, AX, AY );
        G_ASSERT_VECT2_CMPFLOAT( fix->b, ==, BX, BY );

        G_ASSERT_VECT2_CMPFLOAT( c, ==, AX-BX, AY-BY );
}

static void math_pprz_algebra_double_vect2_smul_tc( math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect2 c;
        c.x = 0.0;
        c.y = 0.0;
	const double SCALE = 6.5;

	VECT2_SMUL( c, fix->a, SCALE );
	
	G_ASSERT_VECT2_CMPDELTA( c, fix->a.x*SCALE, fix->a.y*SCALE, EPSILON );
        G_ASSERT_VECT2_CMPFLOAT( fix->a, ==, AX, AY );
}


static void math_pprz_algebra_double_vect2_sdiv_tc( math_pprz_algebra_double_vect2_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect2 c;
        c.x = 0.0;
        c.y = 0.0;
        const double SCALE = 6.5;

        VECT2_SDIV( c, fix->a, SCALE );

        G_ASSERT_VECT2_CMPDELTA( c, fix->a.x/SCALE, fix->a.y/SCALE, EPSILON );
        G_ASSERT_VECT2_CMPFLOAT( fix->a, ==, AX, AY );
}

static void  math_pprz_algebra_double_vect2_strim_tc( void )
{
	struct DoubleVect2 c;
	c.x = 1.0;
	c.y = 6.0;

	const double MIN = 3.0;
	const double MAX = 4.0;

	VECT2_STRIM( c, MIN, MAX );
	G_ASSERT_VECT2_CMPFLOAT( c, >=, MIN, MIN );
	G_ASSERT_VECT2_CMPFLOAT( c, <=, MAX, MAX );
}

/* 
 * Test functions for the 3-vector functions from pprz_algebra.h
 */
typedef struct {
        struct DoubleVect3 a;
        struct DoubleVect3 b;
} math_pprz_algebra_double_vect3_fixture;

static void math_pprz_algebra_double_vect3_fixture_setup( math_pprz_algebra_double_vect3_fixture *fix,
                                    gconstpointer test_data )
{
        fix->a.x = AX;
        fix->a.y = AY;
	fix->a.z = AZ;

        fix->b.x = BX;
        fix->b.y = BY;
	fix->b.z = BZ;
}

static void math_pprz_algebra_double_vect3_fixture_teardown( math_pprz_algebra_double_vect3_fixture *fix,
                                    gconstpointer test_data )
{
}

/* I feel dirty doing this but it syntactically much nicer than an inline function */
#ifdef G_ASSERT_A_UNCHANGED
#undef G_ASSERT_A_UNCHANGED
#endif
#define G_ASSERT_A_UNCHANGED G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, AX, AY, AZ )

#ifdef G_ASSERT_B_UNCHANGED 
#undef G_ASSERT_B_UNCHANGED
#endif
#define G_ASSERT_B_UNCHANGED G_ASSERT_VECT3_CMPFLOAT( fix->b, ==, BX, BY, BZ )

static void math_pprz_algebra_double_vect3_fixture_tc(  math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
	G_ASSERT_A_UNCHANGED;
	G_ASSERT_B_UNCHANGED;

	G_ASSERT_VECT3_CMPFLOAT( fix->a, !=, BX, BY, BZ );

	G_ASSERT_VECT3_VECT3_CMPFLOAT( fix->a, !=, fix->b );
}

static void math_pprz_algebra_double_vect3_assign_tc(  math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
	const double NEWX = 14.0;
	const double NEWY = -43.2;
	const double NEWZ = 12e3;

	VECT3_ASSIGN( fix->a, NEWX, NEWY, NEWZ );

	G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, NEWX, NEWY, NEWZ );

}
	

static void math_pprz_algebra_double_vect3_copy_tc( math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
	VECT3_COPY( fix->a, fix->b );

	G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, BX, BY, BZ );
	G_ASSERT_VECT3_CMPFLOAT( fix->b, ==, BX, BY, BZ );
}

static void math_pprz_algebra_double_vect3_add_tc( math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
        VECT3_ADD( fix->a, fix->b );
	G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, AX+BX, AY+BY, AZ+BZ );
        G_ASSERT_VECT3_CMPFLOAT( fix->b, ==, BX, BY, BZ );
}

static void math_pprz_algebra_double_vect3_sub_tc( math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
        VECT3_SUB( fix->a, fix->b );
        G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, AX-BX, AY-BY, AZ-BZ );
        G_ASSERT_VECT3_CMPFLOAT( fix->b, ==, BX, BY, BZ );
}

static void math_pprz_algebra_double_vect3_sum_tc(  math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect3 c;
        c.x = 0.0;
        c.y = 0.0;
	c.z = 0.0;

        VECT3_SUM( c, fix->a, fix->b );

        G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, AX, AY, AZ );
        G_ASSERT_VECT3_CMPFLOAT( fix->b, ==, BX, BY, BZ );

        G_ASSERT_VECT3_CMPFLOAT( c, ==, AX+BX, AY+BY, AZ+BZ );
}

static void math_pprz_algebra_double_vect3_diff_tc(  math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect3 c;
        c.x = 0.0;
        c.y = 0.0;
	c.z = 0.0;

        VECT3_DIFF( c, fix->a, fix->b );

        G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, AX, AY, AZ );
        G_ASSERT_VECT3_CMPFLOAT( fix->b, ==, BX, BY, BZ );

        G_ASSERT_VECT3_CMPFLOAT( c, ==, AX-BX, AY-BY, AZ-BZ );
}

static void math_pprz_algebra_double_vect3_smul_tc( math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect3 c;
        c.x = 0.0;
        c.y = 0.0;
	c.z = 0.0;
        const double SCALE = 6.5;

        VECT3_SMUL( c, fix->a, SCALE );

        G_ASSERT_VECT3_CMPDELTA( c, AX*SCALE, AY*SCALE, AZ*SCALE, EPSILON );
        G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, AX, AY, AZ );
}

static void math_pprz_algebra_double_vect3_sdiv_tc( math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect3 c;
        c.x = 0.0;
        c.y = 0.0;
	c.z = 0.0;
        const double SCALE = 6.5;

        VECT3_SDIV( c, fix->a, SCALE );

        G_ASSERT_VECT3_CMPDELTA( c, AX/SCALE, AY/SCALE, AZ/SCALE, EPSILON );
        G_ASSERT_VECT3_CMPFLOAT( fix->a, ==, AX, AY, AZ );
}

static void  math_pprz_algebra_double_vect3_strim_tc( void )
{
        struct DoubleVect3 c;
        c.x = 1.0;
        c.y = 6.0;
	c.z = -32.4;

        const double MIN = 3.0;
        const double MAX = 4.0;

        VECT3_STRIM( c, MIN, MAX );
        G_ASSERT_VECT3_CMPFLOAT( c, >=, MIN, MIN, MIN );
        G_ASSERT_VECT3_CMPFLOAT( c, <=, MAX, MAX, MAX );
}

static void math_pprz_algebra_double_vect3_ewdiv_tc( math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect3 c;
        c.x = 0.0;
        c.y = 0.0;
        c.z = 0.0;

        VECT3_EW_DIV( c, fix->a, fix->b );

        G_ASSERT_VECT3_CMPDELTA( c, AX/BX, AY/BY, AZ/BZ, EPSILON );
	G_ASSERT_A_UNCHANGED;
	G_ASSERT_B_UNCHANGED;
}

static void math_pprz_algebra_double_vect3_ew2mul_tc( math_pprz_algebra_double_vect3_fixture *fix, gconstpointer test_data )
{
        struct DoubleVect3 c;
        c.x = 0.0;
        c.y = 0.0;
        c.z = 0.0;

        VECT3_EW_MUL( c, fix->a, fix->b );

        G_ASSERT_VECT3_CMPDELTA( c, AX*BX, AY*BY, AZ*BZ, EPSILON );
        G_ASSERT_A_UNCHANGED;
        G_ASSERT_B_UNCHANGED;
}

/* Not clear to me how this is different from strim */
static void  math_pprz_algebra_double_vect3_bound_cube_tc( void )
{
        struct DoubleVect3 c;
        c.x = 1.0;
        c.y = 6.0;
        c.z = -32.4;

        const double MIN = 3.0;
        const double MAX = 4.0;

        VECT3_BOUND_CUBE( c, MIN, MAX );
        G_ASSERT_VECT3_CMPFLOAT( c, >=, MIN, MIN, MIN );
        G_ASSERT_VECT3_CMPFLOAT( c, <=, MAX, MAX, MAX );
}


/*

#define VECT3_BOUND_CUBE(_v, _min, _max) {                              \
    if ((_v).x > (_max)) (_v).x = (_max); else if ((_v).x < (_min)) (_v).x = (_min); \
    if ((_v).y > (_max)) (_v).y = (_max); else if ((_v).y < (_min)) (_v).y = (_min); \
    if ((_v).z > (_max)) (_v).z = (_max); else if ((_v).z < (_min)) (_v).z = (_min); \
  }


-- And not clear to me whether the transposition of y's and z's on the last two lines are
-- intentional... 
#define VECT3_BOUND_BOX(_v, _v_min, _v_max) {                           \
    if ((_v).x > (_v_max.x)) (_v).x = (_v_max.x); else if ((_v).x < (_v_min.x)) (_v).x = (_v_min.x); \
    if ((_v).y > (_v_max.y)) (_v).y = (_v_max.y); else if ((_v).y < (_v_min.y)) (_v).y = (_v_min.z); \
    if ((_v).z > (_v_max.y)) (_v).z = (_v_max.z); else if ((_v).z < (_v_min.z)) (_v).z = (_v_min.z); \
  }
*/
