import math
import os.path
import logging
import tempfile
import datetime
import pango
import gtk
import gobject

try:
    import osmgpsmap
    MAP_AVAILABLE   = osmgpsmap.__version__ >= "0.5.0"
    MAP_NEW_API     = osmgpsmap.__version__ >= "0.7.1"
except:
    MAP_AVAILABLE = False
    class DummyMap: pass

import gs.ui
import gs.ui.custom as custom
import gs.config as config
import gs.geo as geo
import gs.geo.kml as kml

LOG = logging.getLogger('map')

class AltWidget(custom.GdkWidget):

    DEFAULT_HEIGHT = 60
    VISIBLE_STEPS = 5
    ALT_STEPS = 20
    ALT_RANGE = 100

    def __init__(self):
        custom.GdkWidget.__init__(self)
        self.set_size_request(-1, self.DEFAULT_HEIGHT)

        #altitude in M
        self.min_alt = -10.
        self.max_alt = 90.
        self.alt = 0.
        self.alt_pixel_x = None

    def setup_gcs(self, drawable):
        self.linegc = drawable.new_gc()
        self.linegc.set_line_attributes(1, gtk.gdk.LINE_SOLID,
                                    gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)

        self.redgc = drawable.new_gc(
                        foreground=self.get_color(drawable, r=1.0, g=0.0, b=0.0),
                        fill=gtk.gdk.SOLID,
                        line_width=1)

        self.pc = self.get_pango_context()

    def do_draw(self, drawable):
        steps = gs.linspace(0, self.height, self.VISIBLE_STEPS)
        stepvals = gs.linspace(self.min_alt, self.max_alt, self.VISIBLE_STEPS)

        stepvals.reverse()
        for i in range(len(steps)):
            y = int(steps[i])
            val = stepvals[i]

            #do not draw top or bottom lines
            if y != 0 and y != self.height:
                drawable.draw_line(self.linegc,0, y, self.width, y)

            #draw the label, skipping the top one
            if y != 0:
                layout = pango.Layout(self.pc)
                layout.set_text("%.0f m" % val)
                w,h = layout.get_pixel_size()
                drawable.draw_layout(self.linegc, 1,y-h, layout)

        #draw the altitude marker
        if self.alt_pixel_x != None:
            alt = (self.alt - self.min_alt) / (self.max_alt - self.min_alt)
            alt_pixel_y = self.height - int(alt * self.height)

            w = 10
            drawable.draw_arc(self.redgc, True, self.alt_pixel_x-w/2, alt_pixel_y-w/2, w, w, 0, 360*64)
            drawable.draw_line(self.redgc, self.alt_pixel_x, alt_pixel_y, self.alt_pixel_x, self.height)

            #debug
            if False:
                print "ALT: %.1f <= %.1f <= %.1f" % (self.min_alt, self.alt, self.max_alt)
                print "DRAW: alt %f = %dpx (h=%d, top@0)" % (self.alt, alt_pixel_y, self.height)

                drawable.draw_line(self.redgc, 0, alt_pixel_y, self.width, alt_pixel_y)

                layout = pango.Layout(self.pc)
                layout.set_text("%2.1f" % self.alt)
                w,h = layout.get_pixel_size()
                drawable.draw_layout(self.redgc, 32, 10, layout)

    def update_altitude(self, alt):

        alt = float(alt)

        #adjust range in steps while snapping to 10
        step = self.ALT_STEPS
        total_range = self.ALT_RANGE
        if alt < self.min_alt:
            self.min_alt = alt - step - (alt % 10)
            self.max_alt = self.min_alt + total_range
        if alt > self.max_alt:
            self.max_alt = alt + step - (alt % 10)
            self.min_alt = self.max_alt - total_range

        self.alt = alt
        self.queue_draw()

    def update_pixel_x(self, x):
        self.alt_pixel_x = x
        self.queue_draw()

    def update_pixel_x_and_altitude(self, x, alt):
        self.alt_pixel_x = x
        self.update_altitude(alt)

class _FlightPlanModel(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, float, float, float)
        self.editing = False

    def set_map(self, _map):
        self.map = _map
        if MAP_NEW_API:
            self.maptrack = osmgpsmap.GpsMapTrack()
            self.map.track_add(self.maptrack)

    def clear(self):
        gtk.ListStore.clear(self)
        if MAP_NEW_API:
            self.map.track_remove(self.maptrack)
            self.maptrack = osmgpsmap.GpsMapTrack()
            self.map.track_add(self.maptrack)

    def set_editing(self, e):
        self.editing = e
        if MAP_NEW_API:
            self.maptrack.props.visible = e

    def add(self, lat, lon, alt):
        self.append( (lat,lon,alt) )
        if MAP_NEW_API:
            p = osmgpsmap.point_new_degrees(lat,lon)
            self.maptrack.add_point(p)

class Map(config.ConfigurableIface, gs.ui.GtkBuilderWidget):

    CONFIG_SECTION = "MAP"

    DEFAULT_PROXY = os.environ.get("http_proxy", "")
    DEFAULT_CACHE = os.environ.get("XDG_CACHE_HOME",
                        os.path.join(os.environ.get('HOME',
                            os.path.expanduser("~")), ".cache", "wasp"))
    if os.name == "nt":
        DEFAULT_SOURCE = "0"
    else:
        DEFAULT_SOURCE = "1"

    def __init__(self, conf, source):
        config.ConfigurableIface.__init__(self, conf)
        gs.ui.GtkBuilderWidget.__init__(self, "map.ui")

        self._map = None
        self._pane = gtk.VPaned()
        self._lbl = None
        self._alt = AltWidget()
        self._cbs = {}
        self._kwargs = {}

        #tracks the flight from Mark Home -> export kml
        self._flight_track = []
        self._flight_started = None

        self.lat = None
        self.lon = None

        #the flightplan editor
        self._flightplan = _FlightPlanModel()
        self.get_resource("flight_plan_treeview").set_model(self._flightplan)
        self.get_resource("alt_cellrenderertext").connect("edited", self._cell_edited_cb)
        self.get_resource("flight_plan_window").connect("delete-event", self._flight_plan_window_closed)

        source.register_interest(self._on_gps, 2, "GPS_LLH")
        if MAP_AVAILABLE:
            LOG.info("Map enabled (version: %s)" % osmgpsmap.__version__)
        else:
            LOG.warning("Map disabled. You need osmgpsmap >= 0.5.0")

    def _on_map_button_press(self, _map, event):
        #get the click location
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            if MAP_NEW_API:
                lat,lon = self._map.get_event_location(event).get_degrees()
            else:
                lat, lon = [math.degrees(i) for i in _map.get_co_ordinates(int(event.x), int(event.y))]

            if self._flightplan.editing:
                self._flightplan.add(lat,lon,0.0)

    def _on_map_changed(self, _map):
        if self.lat and self.lon:
            if MAP_NEW_API:
                p = osmgpsmap.point_new_degrees(self.lat, self.lon)
                pixel_x, pixel_y = _map.convert_geographic_to_screen(p)
            else:
                pixel_x, pixel_y = _map.geographic_to_screen(self.lat, self.lon)
            self._alt.update_pixel_x(pixel_x)

    def _on_map_size_allocate(self, widget, allocation):
        self._alt.update_pixel_x(allocation.width/2)

    def _on_gps(self, msg, header, payload):
        fix,sv,self.lat,self.lon,hsl,hacc,vacc = msg.unpack_scaled_values(payload)

        #convert from mm to m
        hsl = hsl/1000.0

        if fix:
            if MAP_AVAILABLE:
                self._map.draw_gps(self.lat, self.lon, 0)

                px, py = self._map.geographic_to_screen(self.lat, self.lon)
                self._alt.update_pixel_x_and_altitude(px, hsl)
            else:
                self._alt.update_altitude(hsl)

            self._flight_track.append( geo.GeoPoint(lat=self.lat, lon=self.lon, alt=hsl) )

    def save_kml(self, path=None):
        if self._flight_track and self._flight_started:
            if not path:
                path = gs.user_file_path(
                            self._flight_started.strftime("%d-%b-%y %H-%M-%S.kml"))

            f = open(path,"w")
            k = kml.KmlDoc("test")
            k.add_trackpoints(self._flight_track)
            k.write(f)
            f.close()
        else:
            path = None

        return path

    def get_widget(self):
        return self._pane

    def connect(self, signal, func, *args):
        """
        Defer connecting to signals on the map object until it is created
        """
        self._cbs[signal] = (func, args)

    def update_state_from_config(self):
        self._cache = self.config_get("cache", self.DEFAULT_CACHE)
        self._proxy = self.config_get("proxy", self.DEFAULT_PROXY)
        self._source = self.config_get("source", self.DEFAULT_SOURCE)

        #convert "" -> None
        if self._proxy == "":
            self._proxy = None
        if self._cache == "":
            self._cache = None
        else:
            if not os.path.isdir(self._cache):
                os.makedirs(self._cache)

        if not self._map:
            if MAP_AVAILABLE:
                self._map = osmgpsmap.GpsMap(
                            map_source=int(self._source),
                            proxy_uri=self._proxy,
                            tile_cache=self._cache)
                #add OSD
                if MAP_NEW_API:
                    self._map.layer_add(
                                osmgpsmap.GpsMapOsd(
                                    show_zoom=True))

                #minimum size of one tile
                self._map.set_size_request(-1, 256)

                LOG.info("Map %s URI: %s" % (self._source, self._map.props.repo_uri))
                LOG.info("Proxy: %s" % self._map.props.proxy_uri)
                LOG.info("Cache: %s" % self._map.props.tile_cache)

                while True:
                    try:
                        signal, (func, args) = self._cbs.popitem()
                        self._map.connect(signal, func, *args)
                    except KeyError:
                        break

                self._flightplan.set_map(self._map)

                #generate notify events to keep the groundstation ui in sync
                self._map.props.auto_center = self._map.props.auto_center
                self._map.props.show_trip_history = self._map.props.show_trip_history

                self._map.connect('changed', self._on_map_changed)
                self._map.connect('size-allocate', self._on_map_size_allocate)
                self._map.connect_after('button-press-event', self._on_map_button_press)

            else:
                self._map = gtk.Label("Map Disabled")

            self._pane.pack1(self._map, resize=True, shrink=False)
            self._pane.pack2(self._alt, resize=False, shrink=False)
            self._pane.set_position(1000)

    def update_config_from_state(self):
        self.config_set("cache", self._cache)
        self.config_set("proxy", self._proxy)
        self.config_set("source", self._source)

    def get_preference_widgets(self):
        proxy = self.build_entry("proxy")
        cache = self.build_entry("cache")

        if MAP_AVAILABLE:
            sources = [(osmgpsmap.source_get_friendly_name(i),str(i)) for i in range(10)]
            source = self.build_combo_with_model("source", *sources)

            items = [proxy, cache, source]
            sg = self.build_sizegroup()
            frame = self.build_frame(None, [
                    self.build_label("Source", source, sg),
                    self.build_label("Proxy", proxy, sg),
                    self.build_label("Cache", cache, sg)
                ])
        else:
            frame = None
            items = ()

        return "Map", frame, items

    def centre(self):
        self._map.set_zoom(self._map.props.max_zoom)

    def mark_home(self, lat, lon):
        self._map.add_image(
                    lat,lon,
                    gs.ui.get_icon_pixbuf(stock=gtk.STOCK_HOME, size=gtk.ICON_SIZE_MENU))

        #reset the track
        self._flight_track = []
        self._flight_started = datetime.datetime.now()

    def _cell_edited_cb(self, cell, path, new_text):
        self._flightplan[path][2] = float(new_text)

    def _flight_plan_window_closed(self, window, event):
        window.hide()
        self._flightplan.set_editing(False)
        return True

    def edit_flightplan(self):
        if not MAP_AVAILABLE:
            return

        self._flightplan.set_editing(True)
        self.get_resource("flight_plan_window").show_all()

    def show_cache_dialog(self, msgarea):
        if not MAP_AVAILABLE:
            return

        def update_download_count(msg, msgarea, gpsmap):
            remaining = gpsmap.get_property("tiles-queued")
            msg.update_text(
                    primary_text=None,
                    secondary_text="%s tiles remaining" % remaining)
            if remaining > 0:
                return True
            else:
                msgarea.clear()
                return False

        dlg = self.get_resource("cache_maps_dialog")

        #widgets
        pt1la = self.get_resource("pt1_lat_entry")
        pt1lo = self.get_resource("pt1_lon_entry")
        pt2la = self.get_resource("pt2_lat_entry")
        pt2lo = self.get_resource("pt2_lon_entry")
        z = self._map.props.zoom
        mz = self._map.props.max_zoom

        LOG.debug("Showing cache dialog for zoom %d -> %d" % (z, mz))

        #preload with the current bounding box
        pt1_lat, pt1_lon,pt2_lat,pt2_lon = self._map.get_bbox()
        pt1la.set_text(str(math.degrees(pt1_lat)))
        pt1lo.set_text(str(math.degrees(pt1_lon)))
        pt2la.set_text(str(math.degrees(pt2_lat)))
        pt2lo.set_text(str(math.degrees(pt2_lon)))

        #get the zoom ranges
        zoom_start = self.get_resource("zoom_start_spinbutton")
        zoom_stop = self.get_resource("zoom_stop_spinbutton")
        
        #default to caching from current -> current + 2
        zoom_start.set_range(1, mz)
        zoom_start.set_value(z)
        zoom_stop.set_range(1, mz)
        zoom_stop.set_value(min(z+2,mz))

        resp = dlg.run()
        if resp == gtk.RESPONSE_OK:
            self._map.download_maps(
                        math.radians(float(pt1la.get_text())),
                        math.radians(float(pt1lo.get_text())),
                        math.radians(float(pt2la.get_text())),
                        math.radians(float(pt2lo.get_text())),
                        int(zoom_start.get_value()),
                        int(zoom_stop.get_value()))
            
            msg = msgarea.new_from_text_and_icon(
                                gtk.STOCK_CONNECT,
                                "Caching Map Tiles",
                                "Calculating...")
            msg.show_all()
            gobject.timeout_add(500, update_download_count, msg, msgarea, self._map)

        dlg.hide()

    def __getattr__(self, name):
        #delegate all calls to the actual map widget
        return getattr(self._map, name)

