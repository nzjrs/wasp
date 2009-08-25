#!/usr/bin/env python

import gentools

try:
    import wasp.xmlobject as xmlobject
except ImportError:
    import xmlobject

import os.path
import sys

#<!DOCTYPE radio SYSTEM "radio.dtd">
#<radio name="Futaba T6EXAP" data_min="900" data_max="2100" sync_min ="5000" sync_max ="15000">
# <channel ctl="1" function="ROLL"     max="1109" neutral="1520" min="1936" average="0"/>
# <channel ctl="2" function="PITCH"    min="1099" neutral="1525" max="1921" average="0"/>
# <channel ctl="3" function="THROTTLE" min="1930" neutral="1930" max="1108" average="0"/>
# <channel ctl="4" function="YAW"      min="1940" neutral="1518" max="1116" average="0"/>
# <channel ctl="5" function="GAIN1"    min="1100" neutral="1500" max="3000" average="1"/>
# <channel ctl="6" function="MODE"     min="1900" neutral="1500" max="1100" average="1"/>
#</radio>

USAGE = "Usage: %s radio_xml_file.xml" % sys.argv[0]
H = "RADIO_H"

if len(sys.argv) != 2:
    print USAGE
    sys.exit(1)
    
try:
    x = xmlobject.XMLFile(path=sys.argv[1])
    radio = x.root
    channels = radio.channel
    avgchans = [c for c in channels if c.average == "1"]
    nrmchans = [c for c in channels if c.average == "0"]
except:
    print "Invalid or missing xml\n  %s" % USAGE
    sys.exit(1)

def norm_chan(c):
    if c.neutral == c.min:
        return "tmp_radio * (MAX_PPRZ / (float)(SIGNED_SYS_TICS_OF_USEC(%s-%s)))" % (c.max, c.min), "0"
    else:
        return "tmp_radio * (tmp_radio >=0 ? (MAX_PPRZ/(float)(SIGNED_SYS_TICS_OF_USEC(%s-%s))) : (MIN_PPRZ/(float)(SIGNED_SYS_TICS_OF_USEC(%s-%s))))" % (c.max, c.neutral, c.min, c.neutral), "MIN_PPRZ"

gentools.print_header(H, generatedfrom=os.path.abspath(sys.argv[1]))

print '#define RADIO_NAME "%s"' % radio.name
print
print '#define RADIO_CTL_NB', len(channels)
print

i = 0
for c in channels:
    print "#define RADIO_CTL_%s %s" % (c.ctl, i)
    print "#define RADIO_%s RADIO_CTL_%s" % (c.function.upper(), c.ctl)
    i += 1

print
print "#define PPM_DATA_MIN_LEN (%sul)" % radio.data_min
print "#define PPM_DATA_MAX_LEN (%sul)" % radio.data_max
print "#define PPM_SYNC_MIN_LEN (%sul)" % radio.sync_min
print "#define PPM_SYNC_MAX_LEN (%sul)" % radio.sync_max
print

print "#define NormalizePpm() {\\"
print "  static uint8_t avg_cpt = 0; /* Counter for averaging */\\"
print "  int16_t tmp_radio;\\"

for c in nrmchans:
    value, min_pprz = norm_chan(c)
    print "  tmp_radio = ppm_pulses[RADIO_%s] - SYS_TICS_OF_USEC(%s);\\" % (c.function, c.neutral)
    print "  rc_values[RADIO_%s] = %s;\\" % (c.function, value)
    print "  Bound(rc_values[RADIO_%s], %s, MAX_PPRZ); \\\n\\" % (c.function, min_pprz)
for c in avgchans:
    print "  avg_rc_values[RADIO_%s] += ppm_pulses[RADIO_%s];\\" % (c.function, c.function)

print "  avg_cpt++;\\"
print "  if (avg_cpt == RC_AVG_PERIOD) {\\"
print "    avg_cpt = 0;\\"
for c in avgchans:
    value, min_pprz = norm_chan(c)
    print "    tmp_radio = avg_rc_values[RADIO_%s] / RC_AVG_PERIOD -  SYS_TICS_OF_USEC(%s);\\" % (c.function, c.neutral)
    print "    rc_values[RADIO_%s] = %s;\\" % (c.function, value)
    print "    avg_rc_values[RADIO_%s] = 0;\\" % c.function
    print "    Bound(rc_values[RADIO_%s], %s, MAX_PPRZ); \\\n\\" % (c.function, min_pprz)
print "    rc_values_contains_avg_channels = TRUE;\\"
print " }\\"
print "}"

gentools.print_footer(H)



