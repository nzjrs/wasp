#!/usr/bin/env python
import sys
import os
import logging
import optparse
import gtk
import gobject

gobject.threads_init()
gtk.gdk.threads_init()

sys.path.insert(0,'/home/user/pythonlibs')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

import gs
import gs.ui
from gs.config import Config, ConfigurableIface
from gs.source import UAVSource
from gs.ui import message_dialog
from gs.ui.info import InfoBox
from gs.ui.graph import Graph, GraphHolder, GraphManager
from wasp.messages import MessagesFile
from wasp.settings import SettingsFile
from wasp.ui.treeview import MessageTreeView
from wasp.ui.senders import RequestMessageSender, RequestMessageButton, RequestTelemetrySender

HILDON_AVAILABLE = False
try:
    import hildon
    HILDON_AVAILABLE = True
except ImportError:
    pass

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(name)-20s][%(levelname)-7s] %(message)s (%(filename)s:%(lineno)d)"
    )

LOG = logging.getLogger('groundstation')

class TabletGraphManager(GraphManager):
    def __init__(self, conf, source, messages, ui):
        GraphManager.__init__(self, conf, source, messages, None, None)
        self._ui = ui

    def add_graph(self, msg, field, adjustable=True, double_buffer=False):
        name = "%s:%s" % (msg.name, field.name)

        if name not in self._graphs:
            LOG.info("Adding graph: %s" % name)

            gh = GraphHolder(
                    Graph(self._source, msg, field, double_buffer=True),
                    name,
                    adjustable,
                    None,#self._on_pause,
                    None,#self._on_print,
                    self._on_remove,
                    None)#self._on_fullscreen)

            gh.show_all()
            self._ui.add_page(name, gh)
            self._graphs[name] = gh

    def _on_remove(self, sender, name):
        gh = self._graphs[name]
        gh.graph.delete()
        self._ui.remove_page(gh)
        del(self._graphs[name])

class UI(ConfigurableIface):

    CONFIG_SECTION = "MAIN"
    DEFAULT_COMMAND_BUTTON = "BOMB_DROP"

    def __init__(self, options, show_tabs=False):

        prefsfile = os.path.abspath(options.preferences)
        messagesfile = os.path.abspath(options.messages)
        settingsfile = os.path.abspath(options.settings)

        if not os.path.exists(messagesfile):
            message_dialog("Could not find messages.xml", None, secondary=gs.CONFIG_DIR)
            sys.exit(1)
        if not os.path.exists(settingsfile):
            message_dialog("Could not find settings.xml", None, secondary=gs.CONFIG_DIR)
            sys.exit(1)

        LOG.info("Groundstation loading")
        LOG.info("Restored preferences: %s" % prefsfile)
        LOG.info("Messages file: %s" % messagesfile)
        LOG.info("Settings file: %s" % settingsfile)

        self._messagesfile = MessagesFile(path=messagesfile, debug=False)
        self._messagesfile.parse()

        self._settingsfile = SettingsFile(path=settingsfile)

        self._config = Config(filename=prefsfile)
        ConfigurableIface.__init__(self, self._config)
        self.autobind_config("command_button")

        self._source = UAVSource(self._config, self._messagesfile, options)
        self._tm = TabletGraphManager(self._config, self._source, self._messagesfile, self)

        self._in_fullscreen = False

        if HILDON_AVAILABLE:
            self._win = hildon.Window()
            self._win.connect("key-press-event", self._on_hildon_key_press)
        else:
            self._win = gtk.Window()
            self._win.set_default_size(800, 480)

        self._win.set_title("Wasp Groundstation")
        self._win.connect("window-state-event", self._on_window_state_change)
        self._win.connect("destroy", self._on_close)

        vb = gtk.VBox(spacing=5)
        self._notebook = gtk.Notebook()
        if not show_tabs:
            self._notebook.set_show_tabs(False)

        self._bb = gtk.HBox()

        vb.pack_start(self._notebook, expand=True, fill=True)
        vb.pack_start(self._bb, expand=False, fill=True)
        self._win.add(vb)

        self.add_page(
                "Status",
                self.make_status_page(show_uav_info=True, show_build=True, show_comm_status=True))
        self.add_page(
                "Telemetry",
                self.make_telemetry_page())

        self._configurable = [
            self._source,
            self._tm,
        ]
        for c in self._configurable:
            if c:
                c.update_state_from_config()

        gobject.timeout_add(2000, lambda: self._source.connect_to_uav())
        gobject.timeout_add(3000, lambda: self._source.refresh_uav_info())

        self._win.show_all()

    def main(self):
        gtk.main()

    def make_status_page(self, show_uav_info=True, show_build=False, show_comm_status=False):
        #hbox for info pages
        ihb = gtk.HBox(homogeneous=True, spacing=5)
        if show_uav_info:
            info = InfoBox(self._source, self._settingsfile, show_images=False, show_build=False, show_comm_status=False)
            ihb.pack_start(info.widget)
        if show_build or show_comm_status:
            vb = gtk.VBox(spacing=5)
            if show_build:
                info = InfoBox(self._source, self._settingsfile, show_images=False, show_uav_status=False, show_build=True, show_comm_status=False)
                vb.pack_start(info.widget, False, False)
            if show_comm_status:
                info = InfoBox(self._source, self._settingsfile, show_images=False, show_uav_status=False, show_build=False, show_comm_status=True)
                vb.pack_start(info.widget, False, False)
            ihb.pack_start(vb, False, True)

        #buttons
        vb = gtk.VButtonBox()
        vb.set_layout(gtk.BUTTONBOX_START)

        b = gtk.Button(stock=gtk.STOCK_CONNECT)
        b.connect("clicked", lambda btn,source: source.connect_to_uav(), self._source)
        vb.pack_start(b)
        b = gtk.Button(stock=gtk.STOCK_DISCONNECT)
        b.connect("clicked", lambda btn,source: source.disconnect_from_uav(), self._source)
        vb.pack_start(b)
        mb = RequestMessageButton(self._messagesfile, "BUILD_INFO", gtk.Button(stock=gtk.STOCK_REFRESH))
        mb.connect("send-message", lambda mb, msg, vals, source: source.send_message(msg, vals), self._source)
        vb.pack_start(mb)
        #custom command buttons
        for name in self._command_button.split(","):
            LOG.info("Adding custom command button: %s" % name)
            msg = self._messagesfile.get_message_by_name(name)
            b = gtk.Button(msg.pretty_name)
            b.connect("clicked", lambda b,s,c,: s.send_command(c, ()), self._source, msg)
            vb.pack_start(b)

        #hb contains info and buttons
        hb = gtk.HBox(spacing=5)
        hb.pack_start(ihb, True, True)
        hb.pack_start(vb, False, False)

        return hb

    def _on_graph_clicked(self, btn, rxtv):
        field = rxtv.get_selected_field()
        msg = rxtv.get_selected_message()
        if field and msg:
            self._tm.add_graph(msg, field)

    def _on_request_telemetry(self, btn):
        def _request_clicked(_rm, _msg, _vals, _source, _dlg):
            _source.send_message(_msg, _vals)
            _dlg.response(gtk.RESPONSE_OK)

        dlg = gtk.Dialog(
                    title="Requrest Telemetry",
                    parent=self._win)

        rm = RequestTelemetrySender(self._messagesfile)
        rm.connect("send-message", _request_clicked, self._source, dlg)
        dlg.vbox.pack_start(rm, False, False)

        dlg.show_all()
        dlg.run()
        dlg.destroy()

    def make_telemetry_page(self):
        rxts = self._source.get_rx_message_treestore()
        if not rxts:
            LOG.critical("Could not get RX treestore")
            return

        vb = gtk.VBox()
        rxtv = MessageTreeView(rxts, editable=False, show_dt=True)
        vb.pack_start(rxtv, expand=True, fill=True)

        b = gs.ui.get_button("Graph Selected", image_stock=gtk.STOCK_ADD)
        b.connect("clicked", self._on_graph_clicked, rxtv)
        vb.pack_start(b, expand=False, fill=True)

        b = gs.ui.get_button("Request Telemetry", image_stock=gtk.STOCK_INFO)
        b.connect("clicked", self._on_request_telemetry)
        vb.pack_start(b, expand=False, fill=True)

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        sw.add_with_viewport(vb)

        return sw

    def _on_close(self, *args):
        for c in self._configurable:
            if c:
                c.update_config_from_state()
        self._config.save()
        self._source.quit()
        gtk.main_quit()


    def _on_hildon_key_press(self, widget, event, *args):
        if event.keyval == gtk.keysyms.F6:
            # The "Full screen" hardware key has been pressed
            if self._in_fullscreen:
                self._win.unfullscreen()
            else:
                self._win.fullscreen()

    def _on_window_state_change(self, widget, event, *args):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self._in_fullscreen = True
        else:
            self._in_fullscreen = False

    def _on_button_clicked(self, btn, page):
        self._notebook.set_current_page(
                self._notebook.page_num(page))

    def add_page(self, pagename, page):
        b = gtk.Button(label=pagename)
        b.connect("clicked", self._on_button_clicked, page)
        b.show()
        page.set_data("BUTTON", b)
        self._notebook.append_page(page)
        self._bb.pack_start(b)

    def remove_page(self, page):
        i = self._notebook.page_num(page)
        if i == -1:
            LOG.critical("Could not find page to remove")
            return

        self._notebook.remove_page(i)
        #remove the button too
        b = page.get_data("BUTTON")
        self._bb.remove(b)
        page.set_data("BUTTON", None)
        self._notebook.set_current_page(0)

if __name__ == "__main__":
    parser = gs.get_default_command_line_parser(True, False, True, preferences_name="tablet.ini")
    options, args = parser.parse_args()
    if gs.IS_WINDOWS:
        import gtk.gdk
        gtk.gdk.threads_enter()    
    UI(options).main()
    if gs.IS_WINDOWS:
        import gtk.gdk
        gtk.gdk.threads_leave()
    sys.exit(1)

