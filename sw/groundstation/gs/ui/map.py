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

import gs.ui
import gs.ui.altwidget as altwidget
import gs.config as config
import gs.geo as geo
import gs.geo.kml as kml

LOG = logging.getLogger('map')

class _FlightPlanModel(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, float, float, float)
        self.editing = False

    def _add_maptrack(self):
        self.maptrack = osmgpsmap.GpsMapTrack()
        self.maptrack.props.color = gtk.gdk.Color(0.0,0.0,1.0)
        self.map.track_add(self.maptrack)

    def set_map(self, _map):
        self.map = _map
        if MAP_NEW_API:
            self._add_maptrack()

    def clear(self):
        gtk.ListStore.clear(self)
        if MAP_NEW_API:
            self.map.track_remove(self.maptrack)
            self._add_maptrack()

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
    if MAP_AVAILABLE:
        DEFAULT_SOURCE = osmgpsmap.SOURCE_OPENSTREETMAP
        DEFAULT_CACHE = osmgpsmap.get_default_cache_directory()
    else:
        DEFAULT_SOURCE = 0
        DEFAULT_CACHE = "/tmp/"

    def __init__(self, conf, source):
        config.ConfigurableIface.__init__(self, conf)
        gs.ui.GtkBuilderWidget.__init__(self, "map.ui")

        self._map = None
        self._pane = gtk.VPaned()
        self._lbl = None
        self._alt = altwidget.AltWidget()
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
                heading = osmgpsmap.INVALID
                if MAP_NEW_API:
                    self._map.gps_add(self.lat, self.lon, heading)
                    px, py = self._map.convert_geographic_to_screen(osmgpsmap.point_new_degrees(self.lat, self.lon))
                else:
                    self._map.draw_gps(self.lat, self.lon, heading)
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
        self._cachebase = self.config_get("cache", self.DEFAULT_CACHE)
        self._proxy = self.config_get("proxy", self.DEFAULT_PROXY)
        self._source = self.config_get("source", self.DEFAULT_SOURCE)

        #convert "" -> None
        if self._proxy == "":
            self._proxy = None
        if self._cachebase == "":
            self._cachebase = None
        else:
            if not os.path.isdir(self._cachebase):
                os.makedirs(self._cachebase)

        if not self._map:
            if MAP_AVAILABLE:
                self._map = osmgpsmap.GpsMap(
                            map_source=int(self._source),
                            proxy_uri=self._proxy,
                            tile_cache_base=self._cachebase)
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
        self.config_set("cache", self._cachebase)
        self.config_set("proxy", self._proxy)
        self.config_set("source", self._source)

    def get_preference_widgets(self):
        proxy = self.build_entry("proxy")
        cache = self.build_entry("cache")

        if MAP_AVAILABLE:
            sources = [(osmgpsmap.source_get_friendly_name(i),str(i)) for i in range(255) if osmgpsmap.source_get_repo_uri(i)]
            source = self.build_combo_with_model("source", *sources)

            items = [proxy, cache, source]
            sg = self.build_sizegroup()
            frame = self.build_frame(None, [
                    self.build_label("Source", source, sg=sg),
                    self.build_label("Proxy", proxy, sg=sg),
                    self.build_label("Cache", cache, sg=sg)
                ])
        else:
            frame = None
            items = ()

        return "Map", frame, items

    def centre(self):
        if not MAP_AVAILABLE:
            return

        self._map.set_zoom(self._map.props.max_zoom)

    def mark_home(self, lat, lon):
        if not MAP_AVAILABLE:
            return

        pb = gs.ui.get_icon_pixbuf(stock=gtk.STOCK_HOME, size=gtk.ICON_SIZE_MENU)
        if MAP_NEW_API:
            self._map.image_add(lat,lon,pb)
        else:
            self._map.add_image(lat,lon,pb)

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
                msgarea.remove(msg)
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
                                "Caching Map Tiles",
                                secondary="Calculating...",
                                message_type=gtk.MESSAGE_INFO)
            msg.show_all()
            gobject.timeout_add(500, update_download_count, msg, msgarea, self._map)

        dlg.hide()

    def __getattr__(self, name):
        #delegate all calls to the actual map widget
        return getattr(self._map, name)

