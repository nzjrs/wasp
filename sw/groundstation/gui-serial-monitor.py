#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import gobject
import gtk

import os.path
import optparse
import ppz
import ppz.transport as transport
import ppz.messages as messages

import ppz.ui.treeview as treeview
import ppz.ui.senders as senders

class GObjectSerialMonitor(gobject.GObject):

    __gsignals__ = {
        "got-message" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_PYOBJECT]),
        }

    def __init__(self, serialsender):
        gobject.GObject.__init__(self)
        self._watch = None   

        serialsender.connect("serial-connected", self._on_serial_connected)
        serialsender.connect_to_port()

    def _on_serial_connected(self, serial, connected):
        #remove the old watch
        if self._watch:
            gobject.source_remove(self._watch)

        if connected:
            #add new watch
            self._watch = gobject.io_add_watch(
                            serial.get_serial().fileno(), 
                            gobject.IO_IN | gobject.IO_PRI,
                            self.on_serial_data_available,
                            serial,
                            priority=gobject.PRIORITY_HIGH
            )

    def on_serial_data_available(self, fd, condition, serial):
        raise NotImplementedError

class UI(GObjectSerialMonitor):
    def __init__(self, messages_file, serialsender, transport, debug=False):
        GObjectSerialMonitor.__init__(self, serialsender)
        self._debug = debug
        self._transport = transport

        self._rxts = treeview.MessageTreeStore()
        rxtv = treeview.MessageTreeView(self._rxts, editable=False, show_dt=True)

        txts = treeview.MessageTreeStore()
        for m in ("PING", "TEST_MESSAGE"):
            msg = messages_file.get_message_by_name(m)
            if msg:
                txts.add_message(msg)
        self._txtv = treeview.MessageTreeView(txts, editable=True)

        w = gtk.Window()
        w.connect('delete-event', self._on_quit, serialsender)

        btn = gtk.Button("Send")
        btn.connect("clicked", self._on_tv_send_clicked, serialsender)

        rm = senders.RequestMessageSender(messages_file)
        rm.connect("send-message", self._on_rm_send_clicked, serialsender)

        vb = gtk.VBox()
        vb.pack_start(gtk.Label("RX"), False, False)
        vb.pack_start(rxtv, True, True)
        vb.pack_start(gtk.Label("TX"), False, False)
        vb.pack_start(self._txtv, False, False)
        vb.pack_start(btn, False, False)
        vb.pack_start(rm, False, False)

        w.add(vb)
        w.set_default_size(350, 500)
        w.show_all()

    def _send_message(self, message, values, serial):
        if message:
            data = self._transport.pack_message_with_values(
                        transport.TransportHeaderFooter(acid=0x78), 
                        message,
                        *values)
            serial.write(data.tostring())

            if self._debug:
                print data, "LEN: ", len(data)
                for d in data:
                    print "    %#X" % ord(d)

    def _on_tv_send_clicked(self, btn, serial):
        message, values = self._txtv.get_selected_message_and_values()
        self._send_message(message, values, serial)

    def _on_rm_send_clicked(self, rm, message, values, serial):
        self._send_message(message, values, serial)

    def _on_quit(self, win, event, serial):
        serial.disconnect_from_port()
        gtk.main_quit()

    def on_serial_data_available(self, fd, condition, serial):

        data = serial.read(1)
        for header, payload in t.parse_many(data):
            msg = m.get_message_by_id(header.msgid)
            if msg:
                self._rxts.update_message(msg, payload)

        return True

if __name__ == "__main__":
    thisdir = os.path.abspath(os.path.dirname(__file__))
    default_messages = os.path.join(thisdir, "..", "messages.xml")

    parser = optparse.OptionParser()
    ppz.setup_comm_optparse_options(parser, default_messages)
    parser.add_option("-d", "--debug",
                    action="store_true",
                    help="print extra debugging information")
    parser.add_option("-D", "--debug-tx",
                    action="store_true",
                    help="print extra debugging information about TX")
    options, args = parser.parse_args()

    m = messages.MessagesFile(path=options.messages, debug=options.debug)
    s = transport.SerialTransport(port=options.port, speed=options.speed, timeout=options.timeout)
    t = transport.Transport(check_crc=True, debug=options.debug)

    m.parse()

    ui = UI(m, s, t, debug=options.debug_tx)
    gtk.main()

