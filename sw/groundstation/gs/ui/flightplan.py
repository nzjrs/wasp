import math
import os.path
import osmgpsmap
import gtk

import gs.ui

class FlightPlanEditor(gs.ui.GtkBuilderWidget):
    def __init__(self, mainmap):
        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "flightplan.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        self._mainmap = mainmap
        self._map = None
        self.widget = self.get_resource("main_hbox")

        self._model = gtk.ListStore(float,float,float)        
        self.get_resource("coord_treeview").set_model(self._model)

        idx = 0
        for name in ("Lat","Lon","Alt"):
            col = gtk.TreeViewColumn(name)
            cell = gtk.CellRendererText()
            if (name == "Alt"):
                cell.set_property('editable', True)
                cell.connect('edited', self._cell_edited_cb, (self._model, idx))
                col.pack_start(cell, True)
                col.add_attribute(cell, "text", idx)
            else:
                col.pack_start(cell, True)
                col.add_attribute(cell, 'text', idx)
            self.get_resource("coord_treeview").append_column(col)
            idx += 1

        self.get_resource("show_map_btn").connect("clicked", self.show_map)

    def _cell_edited_cb(self, cell, path, new_text, model, col):
        model
        model[path][col] = float(new_text)
        return

    def _map_click_callback(self, osmMap, event):
        mouse_x = event.x
        mouse_y = event.y
        lat,lon = osmMap.get_co_ordinates(mouse_x, mouse_y)
        lat = math.degrees(lat)
        lon = math.degrees(lon)
        if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
            self._model.append( (lat,lon,0) )
            osmMap.draw_gps(lat,lon,0)

    def show_map(self, *args):
        if self._map == None:
            self._map = osmgpsmap.GpsMap(
                    repo_uri=self._mainmap.props.repo_uri,
                    proxy_uri=self._mainmap.props.proxy_uri,
                    tile_cache=self._mainmap.props.tile_cache
            )
            self._map.connect("button-press-event", self._map_click_callback)
            self.widget.pack_start(self._map, True, True)

        self._map.props.auto_center = False
        self._map.set_mapcenter(
                    self._mainmap.props.latitude,
                    self._mainmap.props.longitude,
                    self._mainmap.props.zoom
        )
        self._map.show()

