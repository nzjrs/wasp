#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import sys
import fileinput
import re

if __name__ == "__main__":
    EXE = "fgfs"

    simple_list = []
    fixtured_test_list = []
    fixture_list = []
 
    # Process command line args
    for fname in sys.argv[1:]:

	# Right now this parser will only accept function definitions which are
	# all on one line.  Which is a pity because fixtured functions tend to be
	# pretty verbose.  hmm....
	for line in fileinput.input( fname ):
    	    func = re.search("void\s*(.*)_tc\s*\(([A-Za-z0-9\_,\*\s]*)\)",line)	
	    if func:
		if re.search("void", func.group(2) ):
		    simple_list.append( func.group(1) )
		else:
                    values =re.split("[\W]*", func.group(2) )
                    if values:
		    	fixtured_test_list.append( {'name': func.group(1), 
                        	                  'fixture': values[1] } )
			fixture_list.append( values[1] )

    print """
/* Auto-generated test program.  Do not edit */
#include <glib.h>
"""
 
    for func in simple_list:
	print "void %s_tc(void);" % func

    for func in fixture_list:
	print "void %s_setup( %s *, gconstpointer );" % (func, func)
        print "void %s_teardown( %s *, gconstpointer );" % (func, func)

    for func in fixtured_test_list:
        print "void %s_tc( %s *, gconstpointer );" % (func['name'], func['fixture'] )

    print """
int main( int argc, char **argv )
{
        g_test_init( &argc, &argv, NULL );

"""

    for func in simple_list:
	print "\tg_test_add_func(\"%s\", %s_tc);" % (('/' + func.replace('_','/') ),func)

    for func in fixtured_test_list:
	print "\tg_test_add(\"%s\", %s, (gconstpointer)NULL, %s_setup, %s_tc, %s_teardown);" % (('/' + func['name'].replace('_','/') ), func['fixture'], func['fixture'], func['name'], func['fixture'])

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
