# vim: ai ts=4 sts=4 et sw=4

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

    SUPPORTED_TYPES = ("uint8","float")

    def __init__(self, section_name, x):
        self.name = "%s_%s" % (section_name, x.name.upper())
        try:
            self.value = x.value
        except AttributeError:
            self.value = 0

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

        self.type = None
        if self.set or self.get:
            try:
                type_ = x.type;
            except AttributeError:
                pass
            if type_ not in _Setting.SUPPORTED_TYPES:
                raise Exception("Get/Set of setting with type = %s not supported" % self.type)
            self.type = type_

        self.id_str = "SETTING_ID_%s" % self.name

    def print_id(self, i):
        print "#define %s %d" % (self.id_str, i)

    def print_type(self):
        if self.type:
            print "#define SETTING_TYPE_%s %s" % (self.name, self.type)

    def print_value(self):
        print "#define %s %s" % (self.name, self.value)
        if self.rational_approximation:
            val = float(self.value)
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
        for sect in self.sections:
            for s in sect.settings:
                if s.set:
                    self.settible.append(s)
                if s.get:
                    self.gettible.append(s)

    def _print_set_or_get(self, name="set", settings=()):
        i = 0
        print "typedef enum {"
        for s in settings:
            print "\t%s_%s = %s," % (name.upper(), s.name, s.id_str)
            i+= 1
        print "} Setting%stable_t;" % name.title()
        print "#define NUM_SETTING_%sTABLE = %d" % (name.upper(), i)


    def print_typedefs(self):
        #self._print_set_or_get("set", self.settible)
        #print
        #self._print_set_or_get("get", self.gettible)
        #print
        print "typedef enum {"
        for t in _Setting.SUPPORTED_TYPES:
            print "\tSETTING_TYPE_%s," % t.upper()
        print "} SettingType_t;"
        print
        print "typedef bool_t (*SettingSetterCallback_t)(uint8_t chan, void *data);"
        print "typedef bool_t (*SettingGetterCallback_t)(uint8_t chan, void *data);"

    def print_defines(self):
        i = 1
        for sect in self.sections:
            for s in sect.settings:
                s.print_id(i)
                s.print_type()
                i += 1
        print

    def print_values(self):
        for sect in self.sections:
            for s in sect.settings:
                s.print_value()
            print
        print
                
