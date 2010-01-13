# vim: ai ts=4 sts=4 et sw=4

import sys
import re
import os.path

import xmlobject

def contfrac(p, q):
    while q:
        n = p // q
        yield n
        q, p = p - q*n, q

def convergents(cf):
    p, q, r, s = 1, 0, 0, 1
    for c in cf:
        p, q, r, s = c*p+r, c*q+s, p, q
        yield p, q

def convert_float_to_rational_fraction_approximation(xi, maxsize=10000):
    """
    Convert a float to its best rational fraction
    approximation, where the size of the fraction numerator or
    denominator cannot exceed maxsize.

    Python 2.6 has this functionality built in, kind of
    from fractions import Fraction
    Fraction('3.1415926535897932').limit_denominator(1000)
    """
    xp,xq = float.as_integer_ratio(xi)

    p, q = 0, 0
    for r, s in convergents(contfrac(xp, xq)):
#        if s > maxsize and q:                              #limit size of denominator
        if q and (abs(s) > maxsize or abs(r) > maxsize):    #limit size of num and den
            break
        p, q = r, s

    return p,q

class _Setting:

    #Converted to an enum to fake dynamic typing, python -> c with consistent
    #type identifiers
    #WARNING WARNING: THIS MUST BE KEPT CONSISTANT WITH THE VALLUES OF TYPE_T
    #in std.h
    TYPES = {
        "uint8" :   ("TYPE_UINT8", 0),
        "int32" :   ("TYPE_INT32", 5),
        "float" :   ("TYPE_FLOAT", 6),
    }

    TYPE_PYTHON = {
        "uint8" :   int,
        "int32" :   int,
        "float" :   float,
    }

    TYPE_RANGES = {
        "uint8" :   (0,255),
        "int32" :   (-0x7fffffff-1,0x7fffffff),
        "float" :   (-100.0, 100.0),
    }

    def __init__(self, section_name, x):
        self.name = "%s_%s" % (section_name, x.name.upper())
        try:
            self.value = x.value
            self.default_value_string = self.value
        except AttributeError:
            self.value = 0
            self.default_value_string = "Unknown"

        try:
            self.rational_approximation = int(x.integer)
        except AttributeError:
            self.rational_approximation = 0

        try:
            self.get = int(x.get)
        except AttributeError:
            self.get = 0

        try:
            self.set = int(x.set)
        except AttributeError:
            self.set = 0

        try:
            self.doc = x.doc
        except AttributeError:
            self.doc = ""

        self.type = None
        if self.set or self.get:
            #if this setting is to be set or retrieved over comms, then it needs
            #to specify a type
            try:
                type_ = x.type;
            except AttributeError:
                raise
            if type_ not in self.TYPES:
                raise Exception("Get/Set of setting with type = %s not supported" % self.type)
            self.type = type_
            self.python_type = self.TYPE_PYTHON[self.type]
            self.type_enum, self.type_enum_value = self.TYPES[self.type]

        if self.set:
            self.min, self.max = self.TYPE_RANGES[self.type]
            try:
                self.min = self.python_type(x.min)
            except AttributeError:
                pass
            try:
                self.max = self.python_type(x.max)
            except AttributeError:
                pass
        else:
            self.min = -1.0 * float(sys.maxint)
            self.max = float(sys.maxint)

        #A dynamic type can be set or get, so gets assingned an ID and has more
        #code generated
        self.dynamic = (self.type and self.set) or (self.type and self.get)
        self.id = -1
        self.id_str = "SETTING_ID_%s" % self.name

        if self.dynamic:
            try:
                self.step = self.python_type(x.step)
            except AttributeError:
                if self.type == "uint8":
                    self.step = 1
                elif self.type == "int32":
                    self.step = 100
                elif self.type == "float":
                    self.step = 0.1
                else:
                    raise Exception("Type not supported")

    def format_value(self, val=None):
        if val:
            return self.python_type(val)
        else:
            return self.python_type()

    def get_value_adjustment(self):
        """
        Returns min, default, max, adjustment
        """
        default = self.python_type(self.value)
        return self.min, default, self.max, self.step

    def get_default_value(self):
        return self.format_value(self.value)

    def set_id(self, id_):
        self.id = id_

    def print_id(self):
        print "#define %s %d" % (self.id_str, self.id)

    def print_type(self):
        if self.type:
            print "#define SETTING_TYPE_%s %s" % (self.name, self.type_enum)

    def print_value(self):
        print "#define %s %s" % (self.name, self.value)
        if self.rational_approximation:
            val = float(self.value)
            if val == 0.0:
                num = 0
                den = 1
                err = 0.0
                approx = 0.0
            else:
                #maximum integer to fit in approximation of length
                maxval = (2 ** self.rational_approximation) - 1
                num,den = convert_float_to_rational_fraction_approximation(val, maxval)
                approx = float(num)/float(den)
                err = (val-approx)/val
            if err > 0.001:
                raise Exception("Approximation Error: %f != %f" % (val, approx))

            print "/* Fraction %d bit approximation, %0.3f%% error " % (self.rational_approximation, err*100.0)
            print " * %.10f ~= %d / %d " % (val, num, den)
            print " * %.10f ~= %.10f */" % (val, approx)
            print "#define %s_NUM %d" % (self.name, num)
            print "#define %s_DEN %d" % (self.name, den)

    def __str__(self):
        return "<Setting: %s>" % self.name

    def __hash__(self):
        return hash(self.name)

class _Section:
    def __init__(self, x):
        self.name = x.name.upper()

        try:
            self.settings = [_Setting(self.name, s) for s in xmlobject.ensure_list(x.setting)]
        except AttributeError:
            self.settings = []

    def __str__(self):
        return "<Section: %s>" % self.name

class Settings:
    def __init__(self, x):
        self.sections = [_Section(s) for s in xmlobject.ensure_list(x.section)]

        self.settible = []
        self.gettible = []
        i = 1;
        for sect in self.sections:
            for s in sect.settings:
                if s.set:
                    self.settible.append(s)
                if s.get:
                    self.gettible.append(s)
                if s.dynamic:
                    s.set_id(i)
                    i += 1

    def print_typedefs(self):
        print "typedef bool_t (*SettingSetterCallback_t)(uint8_t chan, void *data);"
        print "typedef bool_t (*SettingGetterCallback_t)(uint8_t chan, void *data);"
        print

    def print_defines(self):
        min_ = -1
        max_ = 0

        for sect in self.sections:
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
        for sect in self.sections:
            for s in sect.settings:
                s.print_value()
            print
        print

class SettingsFile:
    def __init__(self, **kwargs):
        path = kwargs.get("path")
        if path and not os.path.exists(path):
            raise Exception("Could not find message file")

        try:
            x = xmlobject.XMLFile(**kwargs)
            self.settings = Settings(x.root)

            settings = []
            for sect in self.settings.sections:
                for s in sect.settings:
                    settings.append(s)
            self.all_settings = settings
            self.all_sections = self.settings.sections
        except:
            self.settings = None
            self.all_settings = []
            self.all_sections = []


