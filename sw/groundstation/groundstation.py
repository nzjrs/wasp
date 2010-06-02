#!/usr/bin/env python
import sys
import os.path
import logging
import optparse

try:
    import gs
except ImportError:
    #probbably running from the source dir
    sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
    import gs

import gs.groundstation as groundstation

#when running from py2exe, if anything is printed to stderr then the app
#shows an annoying dialog when closed
if gs.IS_WINDOWS:
    stream = sys.stdout
else:
    stream = sys.stderr
 
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(name)-20s][%(levelname)-7s] %(message)s (%(filename)s:%(lineno)d)",
    stream=stream
    )

if __name__ == "__main__":
    parser = gs.get_default_command_line_parser(True, True, True)
    options, args = parser.parse_args()
    if gs.IS_WINDOWS:
        import gtk.gdk
        gtk.gdk.threads_enter()    
    groundstation.Groundstation(options).main()
    if gs.IS_WINDOWS:
        import gtk.gdk
        gtk.gdk.threads_leave()
    sys.exit(1)
