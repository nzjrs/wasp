import math
import os.path
import logging
import tempfile

import gobject
import gtk

try:
    import osmgpsmap
    MAP_AVAILABLE = osmgpsmap.__version__ >= "0.4.0"
except:
    MAP_AVAILABLE = False
    class DummyMap: pass

import gs.ui
import gs.config as config

LOG = logging.getLogger('map')

class Map(config.ConfigurableIface, gs.ui.GtkBuilderWidget):

    CONFIG_SECTION = "MAP"

    DEFAULT_PROXY = os.environ.get("http_proxy", "")
    DEFAULT_CACHE = tempfile.gettempdir()
    if os.name == "nt":
        DEFAULT_SOURCE = "0"
    else:
        DEFAULT_SOURCE = "1"

    def __init__(self, conf, source):
        config.ConfigurableIface.__init__(self, conf)

        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "map.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        self._map = None
        self._frame = gtk.Frame()
        self._lbl = None
        self._cbs = {}
        self._kwargs = {}

        if MAP_AVAILABLE:
            source.register_interest(self._on_gps, 2, "GPS_LLH")
        else:
            LOG.warning("Map disabled. You need osmgpsmap >= 0.4.0")

    def _on_gps(self, msg, payload):
        fix,sv,lat,lon,hsl = msg.unpack_values(payload)

        lat = lat/1e7
        lon = lon/1e7

        if fix:
            self._map.draw_gps(lat, lon, 0)

    def get_widget(self):
        return self._frame

    def connect(self, signal, func, *args):
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

        if not self._map:
            if MAP_AVAILABLE:
                self._map = osmgpsmap.GpsMap(
                            map_source=int(self._source),
                            proxy_uri=self._proxy,
                            tile_cache=self._cache)

                LOG.info("Map %s URI: %s" % (self._source, self._map.props.repo_uri))
                LOG.info("Proxy: %s" % self._map.props.proxy_uri)
                LOG.info("Cache: %s" % self._map.props.tile_cache)

            else:
                self._map = gtk.Label("Map Disabled")

            self._frame.add(self._map)

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
            sg = self.make_sizegroup()
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

    def show_cache_dialog(self, msgarea):

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

