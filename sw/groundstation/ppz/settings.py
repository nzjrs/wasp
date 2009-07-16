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

    def print_id(self, i):
        print "#define SETTING_ID_%s %d" % (self.name, i)

    def print_define(self):
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

    def print_ids(self):
        i = 1
        for sect in self.sections:
            for s in sect.settings:
                s.print_id(i)
                i += 1
        print

    def print_defines(self):
        for sect in self.sections:
            for s in sect.settings:
                s.print_define()
            print
        print
                
