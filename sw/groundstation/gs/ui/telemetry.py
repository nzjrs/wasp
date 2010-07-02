import logging
import gtk

import gs.ui
import gs.ui.window
import gs.config as config
import gs.ui.graph as graph
import wasp
import wasp.fms as fms
import wasp.ui.treeview as treeview
import wasp.ui.senders as senders

LOG = logging.getLogger("telemetry")

class TelemetryController(gs.ui.GtkBuilderWidget):

    def __init__(self, config, source, messagesfile, mainwindow):
        gs.ui.GtkBuilderWidget.__init__(self, "telemetry.ui")

        self.source = source
        self.mainwindow = mainwindow
        self.messagesfile = messagesfile
        self.graphmanager = graph.GraphManager(config, source, messagesfile, self.get_resource("graphs_box"), mainwindow)
        self.widget = self.get_resource("hpane")

        rxts = source.get_rx_message_treestore()
        if rxts:
            sw = self.get_resource("telemetry_sw")
            rxtv = treeview.MessageTreeView(rxts, editable=wasp.IS_TESTING, show_dt=not wasp.IS_TESTING)
            sw.add(rxtv)

            vb = self.get_resource("telemetry_left_vbox")
            if wasp.IS_TESTING:
                b = gtk.Button("Send Selected")
                b.connect("clicked", self.on_send_msg_clicked, rxtv)
                vb.pack_start(b, False, False)

            rm = senders.RequestMessageSender(messagesfile)
            rm.connect("send-message", lambda _rm, _msg, _vals: self.source.send_message(_msg, _vals))
            vb.pack_start(rm, False, False)

            gb = self.get_resource("graph_button")
            gb.connect("clicked", self.on_gb_clicked, rxtv)

    def on_gb_clicked(self, btn, tv):
        field = tv.get_selected_field()
        msg = tv.get_selected_message()
        self.graphmanager.add_graph(msg, field)

    def on_send_msg_clicked(self, btn, tv):
        msg,vals = tv.get_selected_message_and_values()
        if msg:
            LOG.info("Sending Msg: %s %s" % (msg,vals))
            self.source.send_message(msg, vals)

    def request_telemetry(self):
        dlg = gs.ui.window.DialogWindow(
                                "Requrest Telemetry",
                                parent=self.mainwindow)

        rm = senders.RequestTelemetrySender(self.messagesfile)
        rm.connect("send-message", lambda _rm, _msg, _vals: self.source.send_message(_msg, _vals))
        dlg.vbox.pack_start(rm, False, False)

        dlg.show_all()



