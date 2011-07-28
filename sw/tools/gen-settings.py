#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import gentools

try:
    import wasp.settings as settings
    import wasp.xmlobject as xmlobject
except ImportError:
    import settings
    import xmlobject

import optparse
import re
import os.path
import sys

class _Writer(object):

    def __init__(self, generated_from):
        self.generated_from = generated_from

    def preamble(self, outfile):
        pass

    def body(self, outfile):
        pass

    def postamble(self, outfile):
        pass

class SettingsWriter(settings.SettingsFile, _Writer):

    H = "SETTINGS_GENERATED_H"

    def __init__(self, *args, **kwargs):
        settings.SettingsFile.__init__(self, *args, **kwargs)
        _Writer.__init__(self, kwargs["generated_from"])

    def _print_typedefs(self, outfile):
        print >> outfile, "typedef bool_t (*SettingSetterCallback_t)(uint8_t chan, void *data);"
        print >> outfile, "typedef bool_t (*SettingGetterCallback_t)(uint8_t chan, void *data);"
        print >> outfile

    def _print_dynamic_settings(self, outfile):
        min_ = -1
        max_ = 0

        for sect in self.all_sections:
            for s in sect.settings:
                if s.dynamic:
                    print >> outfile, "#define %s %d" % (s.id_str, s.id)
                    if s.type:
                        print >> outfile, "#define SETTING_TYPE_%s %s" % (s.name, s.type_enum)

                    if min_ == -1:
                        min_ = s.id
                    max_ = max(s.id, max_)

        print >> outfile
        print >> outfile, "#define SETTING_ID_MIN %s" % min_
        print >> outfile, "#define SETTING_ID_MAX %d" % max_
        print >> outfile

    def _print_static_settings(self, outfile):
        for sect in self.all_sections:
            for s in sect.settings:
                print >> outfile, "#define %s %s" % (s.name, s.value)
                if s.rational_approximation:
                    val,num,den,err,approx = s.get_rational_approximation()

                    print >> outfile, "/* Fraction %d bit approximation, %0.3f%% error " % (s.rational_approximation, err*100.0)
                    print >> outfile, " * %.10f ~= %d / %d " % (val, num, den)
                    print >> outfile, " * %.10f ~= %.10f */" % (val, approx)
                    print >> outfile, "#define %s_NUM %d" % (s.name, num)
                    print >> outfile, "#define %s_DEN %d" % (s.name, den)

            print >> outfile
        print >> outfile

    def preamble(self, outfile):
        gentools.print_header(self.H, generatedfrom=self.generated_from, outfile=outfile)
        print >> outfile, '#include "std.h"\n'

    def body(self, outfile):
        self._print_typedefs(outfile)
        self._print_dynamic_settings(outfile)
        self._print_static_settings(outfile)

    def postamble(self, outfile):
        gentools.print_footer(self.H, outfile=outfile)

class RSTWriter(settings.SettingsFile, _Writer, gentools.RSTHelper):

    def __init__(self, *args, **kwargs):
        settings.SettingsFile.__init__(self, *args, **kwargs)

    def preamble(self, outfile):
        self.rst_write_header("Settings", outfile, level=0)
        print >> outfile
        self.rst_write_comment(outfile, "begin-body")
        print >> outfile

    def body(self, outfile):
        self.rst_write_header("Run-time Adjustable Settings", outfile, level=2)
        print >> outfile
        self.rst_write_table(outfile,
                "",
                ("Name","Type"),
                [(s.name, s.type) for s in self.all_settings if s.dynamic])
        print >> outfile
        self.rst_write_header("Compile-time Adjustable Settings", outfile, level=2)
        print >> outfile
        for sect in self.all_sections:
            self.rst_write_header(sect.name, outfile, level=3)
            print >> outfile
            for s in sect.settings:
                self.rst_write_list(outfile, s.name)
                print >> outfile
                if s.doc:
                    self.rst_write_list(outfile, "*%s*" % s.doc, 2)
                if s.type != None:
                    val_s = "Value: %s (%s)" % (s.value,s.type)
                else:
                    val_s = "Value: %s" % s.value
                self.rst_write_list(outfile, val_s, 2)
                if s.set:
                    self.rst_write_list(outfile, "Min: %s" % s.min, 2)
                    self.rst_write_list(outfile, "Max: %s" % s.max, 2)
                print >> outfile

    def postamble(self, outfile):
        self.rst_write_comment(outfile, "end-body")
        print >> outfile

if __name__ == "__main__":
    OUTPUT_MODES = {
        "header"        :   SettingsWriter,
        "rst"           :   RSTWriter,
    }
    OUTPUT_MODES_DEFAULT = "header"
    OUTPUT_MODES_LIST = ", ".join(OUTPUT_MODES)

    parser = optparse.OptionParser()
    parser.add_option("-s", "--settings",
                    default="settings.xml",
                    help="settings xml file", metavar="FILE")
    parser.add_option("-f", "--format",
                    default=OUTPUT_MODES_DEFAULT,
                    help="output format: %s [default: %s]" % (OUTPUT_MODES_LIST, OUTPUT_MODES_DEFAULT))
    options, args = parser.parse_args()

    if not os.path.exists(options.settings):
        parser.error("could not find settings.xml")

    try:
        klass = OUTPUT_MODES[options.format]
    except KeyError:
        parser.error("output mode must be one of %s" % OUTPUT_MODES_LIST)

    try:
        settings_path = os.path.abspath(options.settings)
    except:
        import traceback
        parser.error("invalid xml\n%s" % traceback.format_exc())

    f = sys.stdout

    writer = klass(path=settings_path, generated_from=settings_path)
    writer.preamble(outfile=f)
    writer.body(outfile=f)
    writer.postamble(outfile=f)

