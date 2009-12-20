#ifndef _TEST_SUPPORT_H
#define _TEST_SUPPORT_H

#define EPSILON 1e-6

#ifndef g_assert_cmpdelta
#define g_assert_cmpdelta(a,b,e)  g_assert_cmpfloat( fabs(a-b), <=, e ) 
#endif


/* Hm.  How do you test the test functions? */
#define G_ASSERT_VECT2_CMPFLOAT( a_, op_, x_, y_ ) { \
	g_assert_cmpfloat( (a_).x, op_, (x_) ); \
        g_assert_cmpfloat( (a_).y, op_, (y_) ); }

#define G_ASSERT_VECT2_VECT2_CMPFLOAT( a_, op_, b_ ) { \
        g_assert_cmpfloat( (a_).x, op_, (b_).x ); \
        g_assert_cmpfloat( (a_).y, op_, (b_).y ) }

#define G_ASSERT_VECT2_CMPDELTA( a_, x_, y_, e_ ) { \
        g_assert_cmpdelta( (a_).x, (x_), (e_) ); \
        g_assert_cmpdelta( (a_).y, (y_), (e_) ); }


#define G_ASSERT_VECT3_CMPFLOAT( a_, op_, x_, y_, z_ ) { \
	g_assert_cmpfloat( (a_).x, op_, (x_) ); \
	g_assert_cmpfloat( (a_).y, op_, (y_) ); \
	g_assert_cmpfloat( (a_).z, op_, (z_) ); }

#define G_ASSERT_VECT3_VECT3_CMPFLOAT(a_, op_, b_) { \
	g_assert_cmpfloat( (a_).x, op_, (b_).x ); \
	g_assert_cmpfloat( (a_).y, op_, (b_).y ); \
	g_assert_cmpfloat( (a_).z, op_, (b_).z ); } 

#define G_ASSERT_VECT3_CMPDELTA( a_, x_, y_, z_, e_ ) { \
        g_assert_cmpdelta( (a_).x, (x_), (e_) ); \
        g_assert_cmpdelta( (a_).y, (y_), (e_) ); \
	g_assert_cmpdelta( (a_).z, (z_), (e_) ); }


#endif
