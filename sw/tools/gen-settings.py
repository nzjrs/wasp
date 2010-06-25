#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import gentools

try:
    import wasp.settings as settings
    import wasp.xmlobject as xmlobject
except ImportError:
    import settings
    import xmlobject

import string
import optparse
import re
import os.path
import sys

class SettingsWriter(settings.SettingsFile):

    def print_typedefs(self):
        print "typedef bool_t (*SettingSetterCallback_t)(uint8_t chan, void *data);"
        print "typedef bool_t (*SettingGetterCallback_t)(uint8_t chan, void *data);"
        print

    def print_defines(self):
        min_ = -1
        max_ = 0

        for sect in self.all_sections:
            for s in sect.settings:
                if s.dynamic:
                    s.print_id()
                    s.print_type()
                    if min_ == -1:
                        min_ = s.id
                    max_ = max(s.id, max_)

        print
        print "#define SETTING_ID_MIN %s" % min_
        print "#define SETTING_ID_MAX %d" % max_
        print

    def print_values(self):
        for sect in self.all_sections:
            for s in sect.settings:
                s.print_value()
            print
        print

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
        settings = SettingsWriter(path=settings_path)

    except:
        import traceback
        parser.error("invalid xml\n%s" % traceback.format_exc())

    gentools.print_header(H, generatedfrom=settings_path)
    print '#include "std.h"\n'
    settings.print_typedefs()
    settings.print_defines()
    settings.print_values()
    gentools.print_footer(H)
