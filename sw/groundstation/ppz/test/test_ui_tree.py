import gtk

import testsetup
import ppz.messages as messages
import ppz.transport as transport
import ppz.ui.treeview as treeview

def _send(btn, tv):
    tv.send_selected()

path = testsetup.get_messages()
mf = messages.MessagesFile(xmlfile=path, debug=True)
mf.parse()

ts = treeview.MessageTreeStore(mf)

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
