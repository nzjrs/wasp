import os.path

import testsetup
import ppz.messages as messages

path = testsetup.get_messages()

i = messages.MessagesFile(path)
i.parse(debug=True)

testm = ("ALIVE","DOWNLINK_STATUS", "BOOT")

for t in testm:
    m = i.get_message_by_name(t)
    print "%s" % m
    for f in m.get_fields():
        print "    %s = %s" % (f, f.get_printable_value(1))

s = i.get_message_by_id(231)
print "%s" % s
f = s.get_field_by_name("rc_status")
print "    %s = %s" % (f, f.get_printable_value(1))
