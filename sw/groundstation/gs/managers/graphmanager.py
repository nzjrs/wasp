import gobject
import gtk
import logging

import gs.ui.graph as graph
import gs.config as config

LOG = logging.getLogger('graphmanager')

class GraphManager(config.ConfigurableIface):

    CONFIG_SECTION = "GRAPHMANAGER"

    def __init__(self, conf, source, messages, box, main_window):
        config.ConfigurableIface.__init__(self, conf)
        self._source = source
        self._messages = messages
        self._box = box
        self._main_window = main_window
        self._graphs = {}
        self._hboxes = {}

    def _on_pause(self, sender, graph):
        graph.pause_toggle()

    def _on_remove(self, sender, name):
        del(self._graphs[name])
        hb = self._hboxes[name]
        self._box.remove(hb)
        del(self._hboxes[name])

    def update_state_from_config(self):
        num = self.config_get("num_graphs", 0)
        if num:
            LOG.info("Restoring %s graphs" % num)
            for i in range(0, int(num)):
                name = self.config_get("graph_%d" % i, ":")
                try:
                    msg_name, field_name = name.split(":")
                    if msg_name and field_name:
                        msg = self._messages.get_message_by_name(msg_name)
                        field = msg.get_field_by_name(field_name)

                        if msg and field:
                            self.add_graph(msg, field)
                except Exception:
                    LOG.warn("Error adding graph", exc_info=True)

    def update_config_from_state(self):
        self.config_delete_keys_in_section()

        num = 0
        for name in self._graphs:
            self.config_set("graph_%d" % num, name)
            num += 1

        LOG.info("Saved %s graphs" % num)
        self.config_set("num_graphs", num)

    def add_graph(self, msg, field):
        name = "%s:%s" % (msg.name, field.name)

        LOG.info("Adding graph: %s" % name)
        #graph is a 
        # hbox
        #   frame | vertical buttons (pause, remove, etc)
        hbox = gtk.HBox()
        hbox.set_spacing(5)

        g = graph.Graph(self._source, msg, field)
        frame = gtk.Frame(name)
        frame.add(g)
        hbox.pack_start(frame)

        bbox = gtk.VButtonBox()
        pa = gtk.Button(stock=gtk.STOCK_MEDIA_PAUSE)
        pa.connect("clicked", self._on_pause, g)
        pr = gtk.Button(stock=gtk.STOCK_PRINT)
        rm = gtk.Button(stock=gtk.STOCK_REMOVE)
        #CRASHY
        rm.connect("clicked", self._on_remove, name)
        bbox.pack_start(pa, False, False)
        bbox.pack_start(pr, False, False)
        bbox.pack_start(rm, False, False)

        bbox.set_layout(gtk.BUTTONBOX_END)
        hbox.pack_start(bbox, False, False)

        self._box.pack_start(hbox)
        self._graphs[name] = g
        self._hboxes[name] = hbox

        hbox.show_all()


