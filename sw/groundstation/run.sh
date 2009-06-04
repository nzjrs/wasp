#!/bin/sh

#yuck yuck yuck yuck
osmpath=`python2.5 -c "\
import sys, os.path
try:
    import osmgpsmap
except ImportError:
    print os.path.expanduser('~/Programming/osm-gps-map.git/python/.libs/')
"`
mypath=`dirname $0`

PYTHONPATH=$mypath:$osmpath $1 $2 $3 $4 $5 $6 $7 $8

