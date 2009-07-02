import gobject
import gtk
#import gtkdatabox
import logging

import gs.data as data
import gs.ui.source as source
import gs.ui.graph as graph
import gs.config as config


LOG = logging.getLogger('graphmanager')

class GraphManager(config.ConfigurableIface, source.PeriodicUpdateFromSource):
    CONFIG_SECTION = "GRAPHMANAGER"
    def __init__(self, conf, box, main_window):
        config.ConfigurableIface.__init__(self, conf)
        source.PeriodicUpdateFromSource.__init__(self)
        self._am = data.AttributeManagerSingleton
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

    def on_add_graph(self, sender):
        dlg = gtk.Dialog("Select Data to Graph",
                         self._main_window,
                         gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                         (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                          gtk.STOCK_OK, gtk.RESPONSE_OK))
        dlg.vbox.set_spacing(5)
        cbs = {}

        #Add a name entry
        lbl = gtk.Label("<b>Graph Name:</b>")
        lbl.set_use_markup(True)
        lbl.set_alignment(0.0,0.5)
        dlg.vbox.pack_start(lbl, expand=False)
        name = gtk.Entry()
        dlg.vbox.pack_start(name, expand=False)

        #Add a check item for each plottable data in a scrolled window
        lbl = gtk.Label("<b>Available Data:</b>")
        lbl.set_use_markup(True)
        lbl.set_alignment(0.0,0.5)
        dlg.vbox.pack_start(lbl, expand=False)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        sw.set_size_request(-1, 300)
        box = gtk.VBox()
        sw.add_with_viewport(box)
        dlg.vbox.pack_start(sw)
        
        for d in self._am.get_attributes():
            if self._am.get_attribute_type(d) == float:
                cb = gtk.CheckButton(d)
                cbs[d] = cb
                box.pack_start(cb, expand=False)

        dlg.show_all()
        resp = dlg.run()
        if resp == gtk.RESPONSE_OK:
            checked = []
            for d,cb in cbs.items():
                if cb.get_active():
                    checked.append(d)

            if checked and name.get_text() and name.get_text() not in self._graphs:
                self.add_graph(name.get_text(), *checked)

        dlg.destroy()

    def update_state_from_config(self):
        num = self.config_get("num_graphs", 0)
        if num:
            LOG.info("Restoring %s graphs" % num)
            for i in range(0, int(num)):
                name =      self.config_get("graph_%d_name" % i,    "")
                values =    self.config_get("graph_%d_values" % i,  "")
                if name and values:
                    self.add_graph(name, *values.split(','))

    def update_config_from_state(self):
        self.config_delete_keys_in_section()

        num = 0
        for name,graph in self._graphs.items():
            self.config_set("graph_%d_name" % num,      name)
            self.config_set("graph_%d_values" % num,    ','.join(graph.get_lines()))
            num += 1

        LOG.info("Saved %s graphs" % num)
        self.config_set("num_graphs", num)

    def add_graph(self, name, *lines):
        LOG.info("Adding graph %s: %s" % (name, ','.join(lines)))
        #graph is a 
        # hbox
        #   frame | vertical buttons (pause, remove, etc)
        hbox = gtk.HBox()
        hbox.set_spacing(5)

        graph = _Graph(*lines)
        frame = gtk.Frame(name)
        frame.add(graph.plot)
        hbox.pack_start(frame)

        bbox = gtk.VButtonBox()
        pa = gtk.Button(stock=gtk.STOCK_MEDIA_PAUSE)
        pa.connect("clicked", self._on_pause, graph)
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
        self._graphs[name] = graph
        self._hboxes[name] = hbox

        hbox.show_all()

    def update_from_data(self, rx):
        pass
        #for graph in self._graphs.values():
        #    graph.update(rx)

