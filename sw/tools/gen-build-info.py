#!/usr/bin/env python

import gentools

import time
import subprocess

try:
    subprocess.call(["git", "--version"], stdout=subprocess.PIPE)
    rev = subprocess.Popen(["git", "rev-parse", "--verify", "HEAD"], stdout=subprocess.PIPE).communicate()[0]
    dirty = subprocess.call(["git", "diff", "--quiet"]) != 0
    branch = subprocess.Popen(["git", "symbolic-ref", "HEAD"], stdout=subprocess.PIPE).communicate()[0]
    ok = True
except:
    ok = False

gentools.print_header("BUILD_H")
if ok:
    print '#define BUILD_REV "%s"' % rev.strip()
    print '#define BUILD_BRANCH "%s"' % branch.split("/")[-1].strip()
    print '#define BUILD_DIRTY', int(dirty)
else:
    print '#define BUILD_REV "UNKNOWN"'
    print '#define BUILD_BRANCH "UNKNOWN"'
    print '#define BUILD_DIRTY 0'
print "#define BUILD_TIME", int(time.mktime(time.localtime()))
gentools.print_footer("BUILD_H")
