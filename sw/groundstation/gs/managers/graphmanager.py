import gobject
import gtk
import logging

import gs.ui.graph as graph
import gs.config as config

LOG = logging.getLogger('graphmanager')

class _GraphRange(gtk.VBox):
    def __init__(self, graph):
        gtk.VBox.__init__(self)

        graph.connect("range-changed", self._on_range_changed)

        mal = gtk.Label("Max:")
        self.maxadj = gtk.Adjustment()
        self._update_adjustment(self.maxadj)
        masb = gtk.SpinButton(self.maxadj)
        masb.props.digits = 1

        mil = gtk.Label("Min:")
        self.minadj = gtk.Adjustment()
        self._update_adjustment(self.minadj)
        misb = gtk.SpinButton(self.minadj)
        misb.props.digits = 1

        self.pack_start(mal, False)
        self.pack_start(masb, False)
        self.pack_start(mil, False)
        self.pack_start(misb, False)

    def _update_adjustment(self, adj, value=0.0, lower=0.0, upper=0.0):
        adj.lower = lower
        adj.page_increment = 1.0
        adj.step_increment = 0.1
        adj.upper = upper
        adj.value = value

    def _on_range_changed(self, graph, min_, max_):
        self._update_adjustment(self.maxadj, value=max_, lower=min_, upper=(max_*1.5))
        self._update_adjustment(self.minadj, value=min_, lower=(min_*1.5), upper=max_)

    def _on_max_spinbutton_changed(self, adj, graph):
        pass

class _GraphHolder(gtk.HBox):
    """
    Composite widget holding a rtgraph and controls

    graph is a hbox:

    frame      |
     [\___  ]  | vertical buttons (pause, remove, etc)
     [    \ ]  | range widgets
    """

    def __init__(self, g, name, adjustable, on_pause, on_print, on_remove):
        gtk.HBox.__init__(self, spacing=5)

        frame = gtk.Frame(name)

        vb = gtk.VBox()
        vb.pack_start(g, True, True)

        tweak = None
        if adjustable:
            tweak = g.get_scroll_rate_widget()
            vb.pack_start(tweak.widget, False, False)

        frame.add(vb)
        self.pack_start(frame)

        vb = gtk.VBox()

        bbox = gtk.VButtonBox()
        vb.pack_start(bbox, True, True)

        pa = gtk.Button(stock=gtk.STOCK_MEDIA_PAUSE)
        pa.connect("clicked", on_pause, tweak)
        pr = gtk.Button(stock=gtk.STOCK_PRINT)
        pr.connect("clicked", on_print, g, name)
        rm = gtk.Button(stock=gtk.STOCK_REMOVE)
        rm.connect("clicked", on_remove, name)
        bbox.pack_start(pa, False, False)
        bbox.pack_start(pr, False, False)
        bbox.pack_start(rm, False, False)
        bbox.set_layout(gtk.BUTTONBOX_END)

        if adjustable:
            r = _GraphRange(g)
            vb.pack_start(r, False, False)

        self.pack_start(vb, False, False)
        self.show_all()

class GraphManager(config.ConfigurableIface):

    CONFIG_SECTION = "GRAPHMANAGER"

    def __init__(self, conf, source, messages, box, main_window):
        config.ConfigurableIface.__init__(self, conf)
        self._source = source
        self._messages = messages
        self._box = box
        self._main_window = main_window
        self._graphs = {}

    def _on_pause(self, sender, tweakScrollRate):
        if tweakScrollRate:
            tweakScrollRate.setValue(0)
            tweakScrollRate.refresh()

    def _on_remove(self, sender, name):
        gh = self._graphs[name]
        self._box.remove(gh)
        del(self._graphs[name])

    def _on_print(self, sender, graph, name):
        def on_print_page(operation, context, page_nr):
            cr = context.get_cairo_context()
            graph.drawIntoCairoContext(cr, name=name)

        print_op = gtk.PrintOperation()
        print_op.set_n_pages(1)
        print_op.connect("draw_page", on_print_page)
        res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)

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

    def add_graph(self, msg, field, adjustable=True):
        name = "%s:%s" % (msg.name, field.name)

        if name not in self._graphs:
            LOG.info("Adding graph: %s" % name)

            gh = _GraphHolder(
                    graph.Graph(self._source, msg, field),
                    name,
                    adjustable,
                    self._on_pause,
                    self._on_print,
                    self._on_remove)

            self._box.pack_start(gh)
            self._graphs[name] = gh

