#include <glib.h>

void math_difference_tc( void )
{
	g_assert_cmpint( 2-1, ==, 1 );
}
