#!/usr/bin/env python
import sys
import os
import logging
import optparse

import gtk

sys.path.insert(0,'/home/user/pythonlibs')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

from gs.config import Config
from gs.source import UAVSource
from gs.ui.info import InfoBox
from gs.ui.graph import Graph, GraphHolder, GraphManager
from wasp.messages import MessagesFile
from wasp.settings import SettingsFile
from wasp.ui.treeview import MessageTreeView
from wasp.ui.senders import RequestMessageSender

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

    def add_graph(self, msg, field, adjustable=True):
        name = "%s:%s" % (msg.name, field.name)

        if name not in self._graphs:
            LOG.info("Adding graph: %s" % name)

            gh = GraphHolder(
                    Graph(self._source, msg, field),
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

class UI:
    def __init__(self,prefsfile, messagesfile, settingsfile, use_test_source, show_tabs=False):

        gtk.gdk.threads_init()

        LOG.info("Groundstation loading")
        LOG.info("Restored preferences: %s" % prefsfile)
        LOG.info("Messages file: %s" % messagesfile)
        LOG.info("Settings file: %s" % settingsfile)

        self._messagesfile = MessagesFile(path=messagesfile, debug=False)
        self._messagesfile.parse()

        self._config = Config(filename=prefsfile)
        self._source = UAVSource(self._config, self._messagesfile, use_test_source)
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
                self.make_status_page())
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

        self._win.show_all()

    def make_status_page(self):
        hb = gtk.HBox()
        info = InfoBox(self._source)
        hb.pack_start(info.widget, expand=True, fill=True)

        vb = gtk.VButtonBox()
        vb.set_layout(gtk.BUTTONBOX_START)

        b = gtk.Button(stock=gtk.STOCK_CONNECT)
        b.connect("clicked", lambda btn,source: source.connect_to_uav(), self._source)
        vb.pack_start(b)
        b = gtk.Button(stock=gtk.STOCK_DISCONNECT)
        b.connect("clicked", lambda btn,source: source.disconnect_from_uav(), self._source)
        vb.pack_start(b)
        hb.pack_start(vb, expand=False, fill=True)

        return hb

    def make_telemetry_page(self):
        def on_gb_clicked(btn, _tv, _gm):
            field = _tv.get_selected_field()
            msg = _tv.get_selected_message()
            _gm.add_graph(msg, field)

        rxts = self._source.get_rx_message_treestore()
        if not rxts:
            LOG.critical("Could not get RX treestore")
            return

        vb = gtk.VBox()
        rxtv = MessageTreeView(rxts, editable=False, show_dt=True)
        vb.pack_start(rxtv, expand=True, fill=True)

        b = gtk.Button(stock=gtk.STOCK_ADD)
        b.connect("clicked", on_gb_clicked, rxtv, self._tm)
        vb.pack_start(b, expand=False, fill=True)

        #rm = RequestMessageSender(self._messagesfile)
        #rm.connect("send-message", lambda _rm, _msg, _vals: self._source.send_message(_msg, _vals))
        #vb.pack_start(rm, expand=False, fill=False)


        #sw.add(rxtv)

        #vb = self.get_resource("telemetry_left_vbox")


        #gb = self.get_resource("graph_button")
        #

        return vb

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
    thisdir = os.path.abspath(os.path.dirname(__file__))
    default_messages = os.path.join(thisdir, "..", "onboard", "config", "messages.xml")
    default_settings = os.path.join(thisdir, "..", "onboard", "config", "settings.xml")

    confdir = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.environ.get("HOME","."), ".config", "wasp"))
    if not os.path.exists(confdir):
        os.makedirs(confdir)
    prefs = os.path.join(confdir, "tablet.ini")

    parser = optparse.OptionParser()
    parser.add_option("-m", "--messages",
                    default=default_messages,
                    help="Messages xml file", metavar="FILE")
    parser.add_option("-s", "--settings",
                    default=default_settings,
                    help="Settings xml file", metavar="FILE")
    parser.add_option("-p", "--preferences",
                    default=prefs,
                    help="User preferences file", metavar="FILE")
    parser.add_option("-t", "--use-test-source",
                    action="store_true", default=False,
                    help="Dont connect to the UAV, use a test source")

    options, args = parser.parse_args()

    if not os.path.exists(options.messages):
        parser.error("could not find messages.xml")

    if not os.path.exists(options.settings):
        parser.error("could not find settings.xml")


    u = UI(
          options.preferences,
          options.messages,
          options.settings,
          options.use_test_source)
    gtk.main()
