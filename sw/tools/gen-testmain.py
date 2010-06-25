#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import sys
import fileinput
import re

if __name__ == "__main__":
    EXE = "fgfs"

    simple_list = []

    # Process command line args
    for fname in sys.argv[1:]:

        for line in fileinput.input( fname ):

            func = re.search("void\s*(main_[\w_]*).*",line)
            if func:
               simple_list.append( func.group(1) )

    print """
/* Auto-generated test program.  Do not edit */
#include <glib.h>
"""
 
    for func in simple_list:
        print "void %s(void);" % func

    print """
int main( int argc, char **argv )
{
        g_test_init( &argc, &argv, NULL );

"""

    for func in simple_list:
	print "\t%s();" % func

    print """

        return g_test_run();
}
    """

