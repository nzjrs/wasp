#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import sys
import fileinput
import re

if __name__ == "__main__":
    EXE = "fgfs"

    list = []
    
    # Process command line args
    for fname in sys.argv[1:]:
	for line in fileinput.input( fname ):
    	    func = re.search("void\s*(.*)_tc.*",line)	
	    if func:
		list.append( func.group(1) )

    print """
/* Auto-generated test program.  Do not edit */
#include <glib.h>
"""
 
    for func in list:
	print "void %s_tc(void);" % func
    

    print """
int main( int argc, char **argv )
{
        g_test_init( &argc, &argv, NULL );

"""

    for func in list:
	print "\tg_test_add_func(\"%s\", %s_tc);" % (('/' + func.replace('_','/') ),func)

    print """

        return g_test_run();
}
    """

#    gentools.print_header(H, generatedfrom=settings_path)
#    print '#include "std.h"\n'
#    settings.print_typedefs()
#    settings.print_defines()
#    settings.print_values()
#    gentools.print_footer(H)
