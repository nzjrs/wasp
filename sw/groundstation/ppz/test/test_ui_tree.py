import gtk

import testsetup
import ppz.messages as messages
import ppz.transport as transport
import ppz.ui.treeview as treeview

def _send(btn, tv):
    message, values = tv.get_selected_message_and_values()
    if message:
        t = transport.Transport(check_crc=True, debug=True)
        data = t.pack_message_with_values(
                    transport.TransportHeaderFooter(acid=0x78), 
                    message,
                    *values)
        print data, "LEN: ", len(data)
        for d in data:
            print "    %#X" % ord(d)

path = testsetup.get_messages()
mf = messages.MessagesFile(xmlfile=path, debug=True)
mf.parse()

ts = treeview.MessageTreeStore()

for m in mf.get_messages():
    ts.add_message(m)

tv = treeview.MessageTreeView(ts)
btn = gtk.Button("Send")
btn.connect("clicked", _send, tv)

hb = gtk.VBox()
hb.pack_start(tv, True, True)
hb.pack_start(btn, False, True)

w = gtk.Window()
w.add(hb)
w.show_all()

gtk.main()
