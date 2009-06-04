import os.path
import sys
import logging
import gtk

import gs.data as data
import gs.ui.dockable as dockable
import gs.ui.source as source

import gs.ui.rtgraph as rtgraph

LOG = logging.getLogger("graph")

class GraphChannel(rtgraph.Channel):
    def __init__(self, name):
        rtgraph.Channel.__init__(self, name=name)
        self._paused = False
        self._name = name
        self._sm = None

    def set_source_manager(self, sm):
        self._sm = sm

    def getValue(self):
        if self._sm:
            return self._sm.get_source().get_data(self._name)[0]
        else:
            return 0.5

    def pause_toggle(self):
        self._paused = not self._paused

    def get_lines(self):
        return self._lines

class GraphUI(rtgraph.GraphUI):
    pass

class Graph(dockable.DockableNotebookPageMixin, source.ManualUpdateFromSource):

    def __init__(self, main_window, parent_notebook, label, lines, **kwargs):
        source.ManualUpdateFromSource.__init__(self)

        try:
            builder = gtk.Builder()
            path = os.path.join(os.path.dirname(__file__), "plot.xml")
            builder.add_from_file(path)
        except:
            print "Could not load xml file."
            sys.exit(1)

        #get some objects for the dockable mixin magic
        window = builder.get_object("window")
        dock_button = builder.get_object("dock_button")
        dockable.DockableNotebookPageMixin.__init__(self, parent_notebook, window, dock_button, label)

        self._graphs = [GraphChannel(l) for l in lines]
        graphui = GraphUI(self._graphs)
        builder.get_object("holder").pack_start(graphui)
        graphui.show_all()

    def set_source_manager(self, sm):
        source.ManualUpdateFromSource.set_source_manager(self, sm)
        for g in self._graphs:
            g.set_source_manager(sm)

    def update_from_data(self, data):
        print "data"
        #d = [data[label] for label in self._lines]
        #self._plot.update(d)


