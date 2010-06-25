#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import sys
import fileinput
import re
import os

if __name__ == "__main__":
    EXE = "fgfs"

    simple_list = []
    fixtured_test_list = []
    fixture_list = []
 
    # Process command line args
    for fname in sys.argv[1:]:

	base_filename = os.path.splitext( os.path.split( fname )[1] )[0]

	# Right now this parser will only accept function definitions which are
	# all on one line.  Which is a pity because fixtured functions tend to be
	# pretty verbose.  hmm....
	for line in fileinput.input( fname ):
	    print line,

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
/* Begin auto-generated test suite */

void main_%s( void )
{
""" % (base_filename)
	
	for func in simple_list:
            print "\tg_test_add_func(\"%s\", %s_tc);" % (('/' + func.replace('_','/') ),func)

        for func in fixtured_test_list:
            print "\tg_test_add(\"%s\", %s, (gconstpointer)NULL, %s_setup, %s_tc, %s_teardown);" % (('/' + func['name'].replace('_','/') ), func['fixture'], func['fixture'], func['name'], func['fixture'])

	print
        print "}"
