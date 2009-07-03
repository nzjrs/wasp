import osmgpsmap
import gtk

    def record_flight_map_click_callback(self, osmMap, event, coordModel):
        mouse_x = event.x
        mouse_y = event.y
        lat,lon = osmMap.get_co_ordinates(mouse_x, mouse_y)
        lat = math.degrees(lat)
        lon = math.degrees(lon)
        if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
            coordModel.prepend( (lat,lon,0) )
            osmMap.draw_gps(lat,lon,0)

    def on_stop_record_flight(self, widget):
        pass

    def on_record_flight_activate(self, widget):
        win  = self._builder.get_object("record_flight_window")
        record_hbox  = self._builder.get_object("record_vbox")
        coordview = self._builder.get_object("coordview")
        lm = gtk.ListStore(float,float,float)

        idx = 0
        for name in ("Lat","Lon","Alt"):
            col = gtk.TreeViewColumn(name)
            cell = gtk.CellRendererText()
            if (name == "Alt"):
                cell.set_property('editable', True)
                cell.connect('edited', self.cell_edited_cb, (lm, idx))
                col.pack_start(cell, True)
                col.add_attribute(cell, "text", idx)
            else:
                col.pack_start(cell, True)
                col.add_attribute(cell, 'text', idx)
            coordview.append_column(col)
            idx += 1

        m = osmgpsmap.GpsMap(
                repo_uri=self._map.props.repo_uri,
                proxy_uri=self._map.props.proxy_uri,
                tile_cache=self._map.props.tile_cache)

        m.props.auto_center = False
        record_hbox.pack_start(m)
        m.connect("button-press-event", self.record_flight_map_click_callback, lm)
        coordview.set_model(lm)
        win.show_all()
        m.set_mapcenter(self._map.props.latitude, self._map.props.longitude, self._map.props.zoom)
        
    def on_record_flight_window_delete(self, widget, event):
        widget.hide_all()
        return True
