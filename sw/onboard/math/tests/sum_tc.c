#include <glib.h>

void math_sum_tc( void )
{
	g_assert_cmpint( 1+2, ==, 2+1 );
}
