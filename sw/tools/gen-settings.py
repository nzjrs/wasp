#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import xmlobject
import gentools

try:
    import ppz.settings as settings
except ImportError:
    import settings

import string
import optparse
import re
import os.path
import sys

if __name__ == "__main__":
    H = "SETTINGS_GENERATED_H"

    parser = optparse.OptionParser()
    parser.add_option("-s", "--settings",
                    default="settings.xml",
                    help="settings xml file", metavar="FILE")
    options, args = parser.parse_args()

    if not os.path.exists(options.settings):
        parser.error("could not find settings.xml")

    try:
        settings_path = os.path.abspath(options.settings)
        x = xmlobject.XMLFile(path=settings_path)

        settings = settings.Settings(x.root)

    except:
        import traceback
        parser.error("invalid xml\n%s" % traceback.format_exc())

    gentools.print_header(H, generatedfrom=settings_path)
    settings.print_ids()
    settings.print_defines()
    gentools.print_footer(H)
