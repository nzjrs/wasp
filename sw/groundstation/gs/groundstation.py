import sys
import os.path
import datetime
import math
import gtk.gdk
import gobject
import logging

gobject.threads_init()
gtk.gdk.threads_init()

from gs.database import Database
from gs.config import Config, ConfigurableIface, ConfigWindow
from gs.source import UAVSource
from gs.plugin import PluginManager

from gs.ui import GtkBuilderWidget, get_icon_pixbuf, message_dialog
from gs.ui.graph import Graph, GraphManager
from gs.ui.tree import DBWidget
from gs.ui.msgarea import MsgAreaController
from gs.ui.statusbar import StatusBar
from gs.ui.info import InfoBox
from gs.ui.flightplan import FlightPlanEditor
from gs.ui.log import LogBuffer, LogWindow
from gs.ui.map import Map
from gs.ui.settings import SettingsController
from gs.ui.window import DialogWindow
from gs.ui.statusicon import StatusIcon

from wasp.messages import MessagesFile
from wasp.settings import SettingsFile
from wasp.ui.treeview import MessageTreeView
from wasp.ui.senders import RequestMessageSender, RequestTelemetrySender

LOG = logging.getLogger('groundstation')

class Groundstation(GtkBuilderWidget, ConfigurableIface):

    CONFIG_SECTION = "MAIN"

    CONFIG_CONNECT_NAME = "Connect_to_UAV_automatically"
    CONFIG_CONNECT_DEFAULT = "1"
    CONFIG_LAT_DEFAULT = -43.520451
    CONFIG_LON_DEFAULT = 172.582377
    CONFIG_ZOOM_DEFAULT = 12

    def __init__(self, prefsfile, messagesfile, settingsfile, use_test_source):
        #connect our log buffer to the python logging subsystem
        self._logbuffer = LogBuffer()
        handler = logging.StreamHandler(self._logbuffer)
        defaultFormatter = logging.Formatter(self._logbuffer.FORMAT)
        handler.setFormatter(defaultFormatter)
        logging.root.addHandler(handler)

        LOG.info("Groundstation loading")
        LOG.info("Restored preferences: %s" % prefsfile)
        LOG.info("Messages file: %s" % messagesfile)
        LOG.info("Settings file: %s" % settingsfile)

        try:
            mydir = os.path.dirname(os.path.abspath(__file__))
            ui = os.path.join(mydir, "groundstation.ui")
            GtkBuilderWidget.__init__(self, ui)
        except Exception:
            LOG.critical("Error loading ui file", exc_info=True)
            sys.exit(1)

        icon = get_icon_pixbuf("rocket.svg")
        gtk.window_set_default_icon(icon)

        self._tried_to_connect = False
        self._home_lat = self.CONFIG_LAT_DEFAULT
        self._home_lon = self.CONFIG_LON_DEFAULT
        self._home_zoom = self.CONFIG_ZOOM_DEFAULT

        self.window = self.get_resource("main_window")

        self._config = Config(filename=prefsfile)
        ConfigurableIface.__init__(self, self._config)

        self._messagesfile = MessagesFile(path=messagesfile, debug=False)
        self._messagesfile.parse()

        self._source = UAVSource(self._config, self._messagesfile, use_test_source)
        self._source.connect("source-connected", self._on_source_connected)

        #track the state of a few key variables received from the plane
        self._state = {}
        self._source.register_interest(self._on_gps, 2, "GPS_LLH")

        self._settingsfile = SettingsFile(path=settingsfile)
        self._settings = SettingsController(self._source, self._settingsfile, self._messagesfile)

        #All the menus in the UI. Get them the first time a plugin tries to add a submenu
        #to the UI to save startup time.
        self._menus = {
                "File"      :   None,
                "Window"    :   None,
                "Map"       :   None,
                "UAV"       :   None,
                "Help"      :   None,
        }

        self._plugin_manager = PluginManager()
        self._plugin_manager.initialize_plugins(self._config, self._source, self._messagesfile, self)

        self._map = Map(self._config, self._source)
        self._gm = GraphManager(self._config, self._source, self._messagesfile, self.get_resource("graphs_box"), self.window)
        self._msgarea = MsgAreaController()
        self._sb = StatusBar(self._source)
        self._info = InfoBox(self._source)
        self._fp = FlightPlanEditor(self._map)
        self._statusicon = StatusIcon(icon, self._source)

        #raise the window when the status icon clicked
        self._statusicon.connect("activate", lambda si, win: win.present(), self.window)

        self.get_resource("main_left_vbox").pack_start(self._info.widget, False, False)
        self.get_resource("main_map_vbox").pack_start(self._msgarea, False, False)
        self.get_resource("window_vbox").pack_start(self._sb, False, False)
        self.get_resource("autopilot_hbox").pack_start(self._fp.widget, True, True)
        self.get_resource("settings_hbox").pack_start(self._settings.widget, True, True)

        #Lazy initialize the following when first needed
        self._plane_view = None
        self._horizon_view = None
        self._prefs_window = None

        #create the map
        self.get_resource("map_holder").add(self._map.get_widget())
        self._map.connect("notify::auto-center", self.on_map_autocenter_property_change)
        self._map.connect("notify::show-trip-history", self.on_map_show_trip_history_property_change)
    
        #Create other notebook tabs
        self._create_telemetry_ui()

        #Setup those items which are configurable, or depend on configurable
        #information, and implement config.ConfigurableIface
        self._configurable = [
            self,
            self._source,
            self._map,
            self._gm,
        ]
        #Add those plugins that can also be configured
        self._configurable += self._plugin_manager.get_plugins_implementing_interface(ConfigurableIface)

        for c in self._configurable:
            if c:
                c.update_state_from_config()

        self.get_resource("menu_item_disconnect").set_sensitive(False)
        self.get_resource("menu_item_autopilot_disable").set_sensitive(False)
        self.builder_connect_signals()

        #FIXME: REMOVE THE AUTOPILOT PAGE
        nb = self.get_resource("main_notebook")
        nb.remove_page(
            nb.page_num(
                self.get_resource("autopilot_hbox")))

        self.window.show_all()

    def _create_telemetry_ui(self):
        def on_gb_clicked(btn, _tv, _gm):
            field = _tv.get_selected_field()
            msg = _tv.get_selected_message()
            _gm.add_graph(msg, field)

        rxts = self._source.get_rx_message_treestore()
        if rxts:
            sw = self.get_resource("telemetry_sw")
            rxtv = MessageTreeView(rxts, editable=False, show_dt=True)
            sw.add(rxtv)

            vb = self.get_resource("telemetry_left_vbox")

            rm = RequestMessageSender(self._messagesfile)
            rm.connect("send-message", lambda _rm, _msg, _vals: self._source.send_message(_msg, _vals))
            vb.pack_start(rm, False, False)

            gb = self.get_resource("graph_button")
            gb.connect("clicked", on_gb_clicked, rxtv, self._gm)

    def _on_gps(self, msg, payload):
        fix,sv,lat,lon,hsl,hacc,vacc = msg.unpack_scaled_values(payload)
        if fix:
            self._state["lat"] = lat
            self._state["lon"] = lon
            #convert from mm to m
            self._state["hsl"] = hsl/1000.0

    def _on_source_connected(self, source, connected):
        conn_menu = self.get_resource("menu_item_connect")
        disconn_menu = self.get_resource("menu_item_disconnect")

        if connected:
            conn_menu.set_sensitive(False)
            disconn_menu.set_sensitive(True)

            #request UAV info once connected
            gobject.timeout_add(500, self.on_menu_item_refresh_uav_activate)
        else:
            disconn_menu.set_sensitive(False)
            conn_menu.set_sensitive(True)

    def _connect(self):
        self._tried_to_connect = True
        self._source.connect_to_uav()

    def _disconnect(self):
        self._source.disconnect_from_uav()

    def add_menu_item(self, name, item):
        if name in self._menus:
            menu = self._menus[name]
            if not menu:
                menu = self.get_resource("%s_menu" % name.lower())
        else:
            #add a new menu
            menuitem = gtk.MenuItem(name)
            self.get_resource("main_menubar").append(menuitem)
            menu = gtk.Menu()
            menuitem.set_submenu(menu)

        self._menus[name] = menu
        menu.append(item)

    def update_state_from_config(self):
        self._c = self.config_get(self.CONFIG_CONNECT_NAME, self.CONFIG_CONNECT_DEFAULT)
        if self._c == "1" and not self._tried_to_connect:
            gobject.timeout_add_seconds(2, self._connect)

        try:
            self._home_lat = float(self.config_get("home_lat", self.CONFIG_LAT_DEFAULT))
            self._home_lon = float(self.config_get("home_lon", self.CONFIG_LON_DEFAULT))
            self._home_zoom = float(self.config_get("home_zoom", self.CONFIG_ZOOM_DEFAULT))
        except Exception:
            LOG.critical("Config error reading home position", exc_info=True)

    def update_config_from_state(self):
        self.config_set(self.CONFIG_CONNECT_NAME, self._c)
        self.config_set("home_lat", self._home_lat)
        self.config_set("home_lon", self._home_lon)
        self.config_set("home_zoom", self._home_zoom)

    def get_preference_widgets(self):
        ck = self.build_checkbutton(self.CONFIG_CONNECT_NAME)
        e1 = self.build_entry("home_lat")
        e2 = self.build_entry("home_lon")
        e3 = self.build_entry("home_zoom")

        items = [ck, e1, e2, e3]

        sg = self.make_sizegroup()
        frame = self.build_frame(None, [
            ck,
            self.build_label("Home Latitude", e1, sg),
            self.build_label("Home Longitude", e2, sg),
            self.build_label("Home Zoom", e3, sg)
        ])

        return "Main Window", frame, items

    def on_window_destroy(self, widget):
        for c in self._configurable:
            if c:
                c.update_config_from_state()
        self._config.save()
        self._source.quit()
        gtk.main_quit()

    def on_uav_mark_home(self, *args):
        #get lat, lon from state
        try:
            lat = self._state["lat"]
            lon = self._state["lon"]
            hsl = self._state["hsl"]
            self._map.mark_home(lat,lon)
            self._sb.mark_home(lat, lon)

            #tell the UAV where home is
            self._source.send_message(
                    self._messagesfile.get_message_by_name("MARK_HOME"),
                    (lat,lon,hsl)
            )
        except KeyError, e:
            msg = self._msgarea.new_from_text_and_icon(
                            gtk.STOCK_DIALOG_ERROR,
                            "Mark Home Failed",
                            "A GPS location has not been received from the UAV yet",
                            timeout=5)
            msg.show_all()

    def on_menu_item_export_kml_activate(self, *args):
        path = self._map.save_kml()
        if path:
            msg = self._msgarea.new_from_text_and_icon(
                            gtk.STOCK_INFO,
                            "KML Export Successful",
                            "The file has been saved to %s" % path,
                            timeout=5)
        else:
            msg = self._msgarea.new_from_text_and_icon(
                            gtk.STOCK_DIALOG_ERROR,
                            "KML Export Failed",
                            "You must mark the home position of the flight first.",
                            timeout=5)
        msg.show_all()

    def on_menu_item_refresh_uav_activate(self, *args):
        #request a number of messages from the UAV
        for n in ("BUILD_INFO", ):
            m = self._messagesfile.get_message_by_name(n)
            if m:
                self._source.request_message(m.id)

        #so we can be called on timeout_add
        return False

    def on_menu_item_request_telemetry_activate(self, *args):
        dlg = DialogWindow(
                "Requrest Telemetry",
                parent=self.window)

        rm = RequestTelemetrySender(self._messagesfile)
        rm.connect("send-message", lambda _rm, _msg, _vals: self._source.send_message(_msg, _vals))
        dlg.vbox.pack_start(rm, False, False)

        dlg.show_all()

    def on_menu_item_log_activate(self, widget):
        w = LogWindow(self._logbuffer)
        w.connect("delete-event", gtk.Widget.hide_on_delete)
        w.set_transient_for(self.window)
        w.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        w.show_all()

    def on_menu_item_show_plugins_activate(self, widget):
        def make_model(plugins):
            m = gtk.ListStore(str, str)
            for name,ver in plugins:
                m.append((name,ver))
            return m
        loaded, failed = self._plugin_manager.get_plugin_summary()

        ptv = self.get_resource("plugintreeview")
        ptv.set_model( make_model(loaded) )
        pftv = self.get_resource("pluginfailedtreeview")
        pftv.set_model( make_model(failed) )

        w = self.get_resource("pluginwindow")
        w.connect("delete-event", gtk.Widget.hide_on_delete)
        w.set_transient_for(self.window)
        w.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        w.show_all()

    def on_menu_item_home_activate(self, widget):
        self._map.set_mapcenter(self._home_lat, self._home_lon, self._home_zoom)

    def on_menu_item_centre_activate(self, widget):
        self._map.centre()

    def on_menu_item_zoom_in_activate(self, widget):
        self._map.set_zoom(self._map.props.zoom+1)

    def on_menu_item_zoom_out_activate(self, widget):
        self._map.set_zoom(self._map.props.zoom-1)    

    def on_menu_item_cache_map_activate(self, widget):
        self._map.show_cache_dialog(self._msgarea)

    def on_menu_item_preferences_activate(self, widget):
        if not self._prefs_window:
            self._prefs_window = ConfigWindow(self.window, self._configurable)

        resp = self._prefs_window.show(self._config)
        #If the user clicked ok to the dialog, update all 
        #objects which are configuration dependant
        if resp == gtk.RESPONSE_ACCEPT:
            for obj in self._configurable:
                obj.update_state_from_config()
            
    def on_menu_item_connect_activate(self, widget):
        self._connect()

    def on_menu_item_disconnect_activate(self, widget):
        self._disconnect()
        
    def on_autopilot_enable_activate(self, widget):
        self.get_resource("menu_item_autopilot_disable").set_sensitive(True)
        self.get_resource("menu_item_autopilot_enable").set_sensitive(False)
    
    def on_autopilot_disable_activate(self, widget):
        self.get_resource("menu_item_autopilot_disable").set_sensitive(False)
        self.get_resource("menu_item_autopilot_enable").set_sensitive(True)
        

    def on_menu_item_about_activate(self, widget):
        dlg = gtk.AboutDialog()
        dlg.set_name("UAV Groundstation")
        dlg.set_authors(("Mark Cottrell", "John Stowers"))
        dlg.set_version("0.2")
        dlg.run()
        dlg.destroy()
        
    def on_menu_item_dock_all_activate(self, widget):
        message_dialog("Not Implemented", self.window)
        
    def db_chooser_callback(self, widget):
        filename = widget.get_filename()
        if filename:
            #tell the database to load from a new file
            db = Database(filename)
            
            db_notes = self.get_resource("db_notes")
            buff = db_notes.get_buffer()
            
            notes = db.fetchall("select notes from flight where rowid=1")[0][0]
            if (notes):
                buff.set_text(notes)

            sw = self.get_resource("dbscrolledwindow")
            for c in sw.get_children():
                sw.remove(c)
            dbw = DBWidget(db)
            dbw.show()
            sw.add(dbw)
            db.close()

    def on_menu_item_show_previous_activate(self, widget):
        message_dialog("Not Implemented", self.window)

    def on_menu_item_plane_view_activate(self, widget):
        if self._plane_view == None:
            try:
                from gs.ui.plane import PlaneView
                self._plane_view = PlaneView(self._source)
            except:
                LOG.warning("Could not initialize plane view", exc_info=True)
                return

        self._plane_view.show_all()
        
    def on_menu_item_horizon_view_activate(self, widget):
        if self._horizon_view == None:
            try:
                from gs.ui.horizon import HorizonView
                self._horizon_view = HorizonView(self._source)
            except:
                LOG.warning("Could not initialize horizon view", exc_info=True)
                return

        self._horizon_view.show_all()

    def on_menu_item_clear_path_activate(self, widget):
        self._map.clear_gps()

    def on_menu_item_clear_previous_activate(self, widget):
        self._map.clear_tracks()

    def on_map_autocenter_property_change(self, osm, *args):
        self.get_resource("menu_item_auto_centre").set_active(osm.get_property("auto-center"))
        
    def on_menu_item_auto_centre_toggled(self, widget):
        self._map.props.auto_center = widget.get_active()

    def on_map_show_trip_history_property_change(self, osm, *args):
        self.get_resource("menu_item_show_path").set_active(osm.get_property("show-trip-history"))

    def on_menu_item_show_path_toggled(self, widget):
        self._map.props.show_trip_history = widget.get_active()

    def main(self):
        if os.name == "nt": gtk.gdk.threads_enter()
        gtk.main()
        if os.name == "nt": gtk.gdk.threads_leave()

