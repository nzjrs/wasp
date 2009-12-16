#ifndef _TEST_SUPPORT_H
#define _TEST_SUPPORT_H

#define EPSILON 1e-6

#ifndef g_assert_cmpdelta
#define g_assert_cmpdelta(a,b,e)  g_assert_cmpfloat( fabs(a-b), <=, e ) 
#endif


#endif
