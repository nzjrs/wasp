import gtk
import logging
import tempfile
import os.path

import osmgpsmap

import gs.config as config

LOG = logging.getLogger('map')

class Map(config.ConfigurableIface):

    CONFIG_SECTION = "MAP"

    SOURCE_OSM = "OSM"
    SOURCE_OAM = "OAM"
    SOURCE_OTHER = "Predefined"
    URI = osmgpsmap.MAP_SOURCE_OPENSTREETMAP
    PROXY = os.environ.get("http_proxy", "")
    CACHE = tempfile.gettempdir()
    ALL_MAP_SOURCES = (
        osmgpsmap.MAP_SOURCE_GOOGLE_HYBRID, 
        osmgpsmap.MAP_SOURCE_MAPS_FOR_FREE,
        osmgpsmap.MAP_SOURCE_OPENSTREETMAP_RENDERER, 
        osmgpsmap.MAP_SOURCE_GOOGLE_SATTELITE,
        osmgpsmap.MAP_SOURCE_OPENAERIALMAP,
        osmgpsmap.MAP_SOURCE_VIRTUAL_EARTH_SATTELITE,
        osmgpsmap.MAP_SOURCE_GOOGLE_SATTELITE_QUAD,
        osmgpsmap.MAP_SOURCE_OPENSTREETMAP
    )

    def __init__(self, conf, source):
        config.ConfigurableIface.__init__(self, conf)
        self._map = None
        self._frame = gtk.Frame()
        self._cbs = {}
        self._kwargs = {}

        source.register_interest(self._on_gps, 2, "GPS_LLH")

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
        LOG.debug(self.config_get("source", self.SOURCE_OSM))

        kwargs = {
            "source"    :   self.config_get("source",   self.SOURCE_OSM),
            "cache"     :   self.config_get("cache",    self.CACHE),
            "uri"       :   self.config_get("uri",      self.URI),
            "proxy"     :   self.config_get("proxy",    self.PROXY)
        }

        if kwargs["source"] == self.SOURCE_OSM:
            kwargs["uri"] =  osmgpsmap.MAP_SOURCE_OPENSTREETMAP
        elif kwargs["source"] == self.SOURCE_OAM:
            kwargs["uri"] =  osmgpsmap.MAP_SOURCE_OPENAERIALMAP
        elif kwargs["source"] == self.SOURCE_OTHER:
            #extra check that the user selected a predefine uri
            if not kwargs["uri"]:
                LOG.warning("Did not select predefined map source")
                kwargs["uri"] =  osmgpsmap.MAP_SOURCE_OPENSTREETMAP
        else:
            LOG.warning("Unknown map source: %s" % kwargs["source"])
            kwargs["uri"] =  osmgpsmap.MAP_SOURCE_OPENSTREETMAP

        #convert "" -> None
        if kwargs["proxy"] == "":
            kwargs["proxy"] = None
        if kwargs["cache"] == "":
            kwargs["cache"] = None

        #re-instantiate the map if anything has changed
        if kwargs != self._kwargs:
            LOG.info("Map source: %s" % kwargs["source"])

            #rm the old one
            old = self._frame.get_child()
            if old:
                self._frame.remove(old)

            #make new one
            self._map = osmgpsmap.GpsMap(
                            repo_uri=kwargs["uri"],
                            proxy_uri=kwargs["proxy"],
                            tile_cache=kwargs["cache"])
            for signal, (func, args) in self._cbs.items():
                self._map.connect(signal, func, *args)
            self._map.show()

            LOG.info("Map URI: %s" % self._map.props.repo_uri)
            LOG.info("Proxy: %s" % self._map.props.proxy_uri)
            LOG.info("Cache: %s" % self._map.props.tile_cache)

            self._frame.add(self._map)
            self._kwargs = kwargs

    def update_config_from_state(self):
        self.config_set("source",   self._kwargs.get("source", self.SOURCE_OSM))
        self.config_set("cache",    self._kwargs.get("cache", self.CACHE))
        self.config_set("uri",      self._kwargs.get("uri", self.URI))
        self.config_set("proxy",    self._kwargs.get("proxy", self.PROXY))

    def get_preference_widgets(self):
        sources =       self.build_radio_group("source", self.SOURCE_OSM, self.SOURCE_OAM, self.SOURCE_OTHER)
        predefined =    self.build_combo("uri", *self.ALL_MAP_SOURCES)
        proxy =         self.build_entry("proxy")
        cache =         self.build_entry("cache")

        items = sources + [predefined, proxy, cache]
        sg = self.make_sizegroup()
        frame = self.build_frame(None, [
            self.build_frame("Map Source", [
                sources[0],
                sources[1],
                sources[2],
                predefined
            ]),
            self.build_frame("Settings", [
                self.build_label("Proxy", proxy, sg),
                self.build_label("Cache", cache, sg)
            ])
        ])

        return "Map", frame, items

    def __getattr__(self, name):
        #delegate all calls to the actual map widget
        return getattr(self._map, name)

