import os.path

import testsetup
import ppz.transport as transport

p = transport.TransportParser(check_crc=False, debug=False)

data = open(os.path.join(testsetup.TEST_DIR,"capture.dat")).read()

for d in data:
    pl = p.parse_one(d)
    if pl:
        print "ACID=%s MSG=%s" % (ord(pl[0]),ord(pl[1]))


