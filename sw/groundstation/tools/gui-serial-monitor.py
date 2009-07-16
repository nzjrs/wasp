#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import gtk

import os.path
import optparse
import wasp
import wasp.transport as transport
import wasp.communication as communication
import wasp.messages as messages
import wasp.monitor as monitor

import wasp.ui.treeview as treeview
import wasp.ui.senders as senders

class UI(monitor.GObjectSerialMonitor):
    def __init__(self, messages_file, serialsender, transport, debug=False):
        monitor.GObjectSerialMonitor.__init__(self, serialsender)
        self._debug = debug
        self._messages_file = messages_file
        self._serialsender = serialsender
        self._transport = transport

        self._serialsender.connect_to_port()

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
        for header, payload in self._transport.parse_many(data):
            msg =  self._messages_file.get_message_by_id(header.msgid)
            if msg:
                self._rxts.update_message(msg, payload)

        return True

if __name__ == "__main__":
    thisdir = os.path.abspath(os.path.dirname(__file__))
    default_messages = os.path.join(thisdir, "..", "..", "onboard", "config", "messages.xml")

    parser = optparse.OptionParser()
    wasp.setup_comm_optparse_options(parser, default_messages)
    parser.add_option("-d", "--debug",
                    action="store_true",
                    help="print extra debugging information")
    parser.add_option("-D", "--debug-tx",
                    action="store_true",
                    help="print extra debugging information about TX")
    options, args = parser.parse_args()

    m = messages.MessagesFile(path=options.messages, debug=options.debug)
    s = communication.SerialCommunication(port=options.port, speed=options.speed, timeout=options.timeout)
    t = transport.Transport(check_crc=True, debug=options.debug)

    m.parse()

    ui = UI(m, s, t, debug=options.debug_tx)
    gtk.main()

