import os.path

import testsetup
import ppz.transport as transport
import ppz.messages as messages

data = open(os.path.join(testsetup.TEST_DIR,"capture.dat")).read()
path = testsetup.get_messages()

p = transport.Transport(check_crc=False, debug=False)
i = messages.MessagesFile(path)
i.parse(debug=True)

alive = i.get_message_by_name("ALIVE")

for d in data:
    pl = p.parse_one(d)
    if pl:
        if ord(pl[1]) == alive.get_id():
            print "ACID=%s MSG=%s" % (ord(pl[0]),ord(pl[1]))
            print alive.unpack_values(pl[2:])
            


