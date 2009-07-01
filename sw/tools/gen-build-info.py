#!/usr/bin/env python

import gentools

import optparse
import time
import subprocess

class BuildInfo:

    #This value must be kept the same as that in messages.xml
    STRING_LEN = 10

    def __init__(self, target):
        self.target = target
        try:
            subprocess.call(["git", "--version"], stdout=subprocess.PIPE)
            self.rev = subprocess.Popen(["git", "rev-parse", "--verify", "HEAD"], stdout=subprocess.PIPE).communicate()[0]
            self.dirty = subprocess.call(["git", "diff", "--quiet"]) != 0
            self.branch = subprocess.Popen(["git", "symbolic-ref", "HEAD"], stdout=subprocess.PIPE).communicate()[0]
            self.ok = True
        except:
            self.ok = False

    def write(self):
        gentools.print_header("BUILD_H")
        if self.ok:
            gentools.define_string("BUILD_REV", self.rev, maxwidth=self.STRING_LEN)
            gentools.define_string("BUILD_BRANCH", self.branch.split("/")[-1], maxwidth=self.STRING_LEN)
            gentools.define_int("BUILD_DIRTY", self.dirty)
        else:
            gentools.define_string("BUILD_REV", "UNKNOWN")
            gentools.define_string("BUILD_BRANCH", "UNKNOWN")
            gentools.define_int("BUILD_DIRTY", 0)
        gentools.define_int("BUILD_TIME", int(time.mktime(time.localtime())))
        gentools.define_string("BUILD_TARGET", self.target, maxwidth=self.STRING_LEN)

        print
        gentools.define_int("BUILD_STRING_LEN", self.STRING_LEN)

        gentools.print_footer("BUILD_H")

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option("-t", "--target",
                    default="autopilot_main",
                    help="the name of the target built")
    options, args = parser.parse_args()

    b = BuildInfo(options.target)
    b.write()

