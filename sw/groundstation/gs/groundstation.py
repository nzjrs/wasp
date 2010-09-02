import sys
import os.path
import datetime
import math
import gtk.gdk
import gobject
import logging

gobject.threads_init()
gtk.gdk.threads_init()

import gs
from gs.config import Config, ConfigurableIface, ConfigWindow
from gs.source import UAVSource
from gs.plugin import PluginManager

from gs.ui import GtkBuilderWidget, get_icon_pixbuf, message_dialog
from gs.ui.tree import DBWidget
from gs.ui.msgarea import MsgAreaController
from gs.ui.statusbar import StatusBar
from gs.ui.info import InfoBox
from gs.ui.log import LogBuffer, LogWindow
from gs.ui.map import Map
from gs.ui.telemetry import TelemetryController
from gs.ui.settings import SettingsController
from gs.ui.command import CommandController
from gs.ui.control import ControlController
from gs.ui.statusicon import StatusIcon

import wasp
from wasp.messages import MessagesFile
from wasp.settings import SettingsFile
from wasp.ui.treeview import MessageTreeView

LOG = logging.getLogger('groundstation')

class Groundstation(GtkBuilderWidget, ConfigurableIface):
    """ The main groundstation window """

    CONFIG_SECTION = "MAIN"

    CONFIG_CONNECT_NAME = "Connect_to_UAV_automatically"
    CONFIG_CONNECT_DEFAULT = "1"
    CONFIG_LAT_DEFAULT = wasp.HOME_LAT
    CONFIG_LON_DEFAULT = wasp.HOME_LON
    CONFIG_ZOOM_DEFAULT = 12

    def __init__(self, options):
        
        prefsfile = os.path.abspath(options.preferences)
        messagesfile = os.path.abspath(options.messages)
        settingsfile = os.path.abspath(options.settings)
        plugindir = os.path.abspath(options.plugin_dir)
        disable_plugins = options.disable_plugins

        if not os.path.exists(messagesfile):
            message_dialog("Could not find messages.xml", None, secondary="%s does not exist." % messagesfile)
            sys.exit(1)
        if not os.path.exists(settingsfile):
            message_dialog("Could not find settings.xml", None, secondary="%s does not exist." % settingsfile)
            sys.exit(1)
    
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
            GtkBuilderWidget.__init__(self, "groundstation.ui")
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
        self.window.set_title(gs.NAME)

        self._config = Config(filename=prefsfile)
        ConfigurableIface.__init__(self, self._config)

        self._messagesfile = MessagesFile(path=messagesfile, debug=False)
        self._messagesfile.parse()

        self._source = UAVSource(self._config, self._messagesfile, options)
        self._source.connect("source-connected", self._on_source_connected)
        self._source.connect("uav-selected", self._on_uav_selected)

        #track the UAVs we have got data from
        self._source.connect("uav-detected", self._on_uav_detected)
        self._uav_detected_model = gtk.ListStore(str,int)
        self._uav_detected_model.append( ("All UAVs", wasp.ACID_ALL) )

        #track the state of a few key variables received from the plane
        self._state = {}
        self._source.register_interest(self._on_gps, 2, "GPS_LLH")

        #All the menus in the UI. Get them the first time a plugin tries to add a submenu
        #to the UI to save startup time.
        self._menus = {
                "File"      :   None,
                "Window"    :   None,
                "Map"       :   None,
                "UAV"       :   None,
                "Help"      :   None,
        }

        self._map = Map(self._config, self._source)
        self._msgarea = MsgAreaController()
        self._sb = StatusBar(self._source)
        self._info = InfoBox(self._source)
        self._statusicon = StatusIcon(icon, self._source)

        #raise the window when the status icon clicked
        self._statusicon.connect("activate", lambda si, win: win.present(), self.window)

        self.get_resource("main_left_vbox").pack_start(self._info.widget, False, False)
        self.get_resource("main_map_vbox").pack_start(self._msgarea, False, False)
        self.get_resource("window_vbox").pack_start(self._sb, False, False)

        #The telemetry tab page
        self.telemetrycontroller = TelemetryController(self._config, self._source, self._messagesfile, self.window)
        self.get_resource("telemetry_hbox").pack_start(self.telemetrycontroller.widget, True, True)

        #The settings tab page
        settingsfile = SettingsFile(path=settingsfile)
        self.settingscontroller = SettingsController(self._source, settingsfile, self._messagesfile)
        self.get_resource("settings_hbox").pack_start(self.settingscontroller.widget, True, True)

        #The command and control tab page
        self.commandcontroller = CommandController(self._source, self._messagesfile)
        self.get_resource("command_hbox").pack_start(self.commandcontroller.widget, False, True)
        self.controlcontroller = ControlController(self._source, self._messagesfile)
        self.get_resource("control_hbox").pack_start(self.controlcontroller.widget, True, True)

        #Lazy initialize the following when first needed
        self._plane_view = None
        self._horizon_view = None
        self._prefs_window = None

        #create the map
        self.get_resource("map_holder").add(self._map.get_widget())
        self._map.connect("notify::auto-center", self.on_map_autocenter_property_change)
        self._map.connect("notify::show-trip-history", self.on_map_show_trip_history_property_change)

        #initialize the plugins
        self._plugin_manager = PluginManager(plugindir)
        if not disable_plugins:
            self._plugin_manager.initialize_plugins(self._config, self._source, self._messagesfile, self)
    
        #Setup those items which are configurable, or depend on configurable
        #information, and implement config.ConfigurableIface
        self._configurable = [
            self,
            self._source,
            self._map,
            self.telemetrycontroller.graphmanager,
        ]
        #Add those plugins that can also be configured
        self._configurable += self._plugin_manager.get_plugins_implementing_interface(ConfigurableIface)

        for c in self._configurable:
            if c:
                c.update_state_from_config()

        self.get_resource("menu_item_disconnect").set_sensitive(False)
        self.get_resource("menu_item_autopilot_disable").set_sensitive(False)
        self.builder_connect_signals()

        self.window.show_all()

    def _on_uav_detected(self, source, acid):
        self._uav_detected_model.append( ("0x%X" % acid, acid) )

    def _on_uav_selected(self, source, acid):
        self.window.set_title("%s - UAV: 0x%X" % (gs.NAME, acid))

    def _on_gps(self, msg, header, payload):
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
            gobject.timeout_add(500, lambda: self._source.refresh_uav_info())
        else:
            disconn_menu.set_sensitive(False)
            conn_menu.set_sensitive(True)

    def _connect(self):
        self._tried_to_connect = True
        self._source.connect_to_uav()

    def _disconnect(self):
        self._source.disconnect_from_uav()

    def _add_submenu(self, name, parent_menu):
        """ adds a submenu of name to parent_menu """
        if name not in self._menus:
            #add a new menu
            menuitem = gtk.MenuItem(name)
            parent_menu.append(menuitem)
            menu = gtk.Menu()
            menuitem.set_submenu(menu)
            self._menus[name] = menu
        return self._menus[name]

    def _get_toplevel_menu(self, name):
        """ gets, or creates a toplevel menu of name """
        if name in self._menus:
            menu = self._menus[name]
            if not menu:
                menu = self.get_resource("%s_menu" % name.lower())
        else:
            menu = self._add_submenu(name, self.get_resource("main_menubar"))

        return menu

    def add_menu_item(self, name, *item):
        """
        Adds an item to the main window menubar. 

        :param name: the name of the top-level menu to add to, e.g. "File". 
                     If a menu of that name does not exist, one is created
        :param item: One or more gtk.MenuItem to add
        """
        menu = self._get_toplevel_menu(name)
        for i in item:
            menu.append(i)

    def add_submenu_item(self, name, submenu_name, *item):
        """
        Adds a submenu and item to the main window menubar.

        :param name: the name of the top-level menu to add to, e.g. "File". 
                     If a menu of that name does not exist, one is created
        :param submenu_name: the name of the submenu to hold the item
        :param item: One or more gtk.MenuItem to add
        """
        menu = self._add_submenu(submenu_name, self._get_toplevel_menu(name))
        for i in item:
            menu.append(i)

    def add_control_widget(self, name, control_widget):
        """
        Adds a control widget to the Command and Control page

        :param name: the name, a string describing the control method, 
                     i.e. 'Joystick'
        :param control_widget: a `gs.ui.control.ControlWidgetIface` that gets placed
                     in the Command and control page of the GUI
        """
        self.controlcontroller.add_control_widget(name, control_widget)

    def update_state_from_config(self):
        self._c = self.config_get(self.CONFIG_CONNECT_NAME, self.CONFIG_CONNECT_DEFAULT)
        if self._c == "1" and not self._tried_to_connect:
            gobject.timeout_add(2000, self._connect)

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

        sg = self.build_sizegroup()
        frame = self.build_frame(None, [
            ck,
            self.build_label("Home Latitude", e1, sg=sg),
            self.build_label("Home Longitude", e2, sg=sg),
            self.build_label("Home Zoom", e3, sg=sg)
        ])

        return "Main Window", frame, items

    def on_window_destroy(self, widget):
        for c in self._configurable:
            if c:
                c.update_config_from_state()
        self._config.save()
        self._source.quit()
        gtk.main_quit()

    def on_menu_item_edit_flightplan_activate(self, *args):
        self._map.edit_flightplan()

    def on_menu_item_uav_mark_home_activate(self, *args):
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
        except KeyError:
            msg = self._msgarea.new_from_text_and_icon(
                            "Mark Home Failed",
                            "A GPS location has not been received from the UAV yet",
                            message_type=gtk.MESSAGE_ERROR,
                            timeout=5)
            msg.show_all()

    def on_menu_item_log_uav_data_activate(self, *args):
        sw = self.get_resource("log_message_scrolledwindow")
        tv = MessageTreeView(
                self._source.get_rx_message_treestore(),
                editable=False, show_dt=False, show_value=False)
        tv.show()
        sw.add(tv)

        w = self.get_resource("logdatadialog")
        w.set_transient_for(self.window)
        w.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        resp = w.run()
        w.hide()

        if resp == gtk.RESPONSE_OK:
            csv = self.get_resource("log_csv_radiobutton")

            messages = ("STATUS", "GPS_LLH")
            if csv.get_active():
                self._source.register_csv_logger(None, *messages)
            else:
                self._source.register_sqlite_logger(None, *messages)

        sw.remove(tv)

    def on_menu_item_export_kml_activate(self, *args):
        path = self._map.save_kml()
        if path:
            msg = self._msgarea.new_from_text_and_icon(
                            "KML Export Successful",
                            'The file has been saved to <a href="file://%s">%s</a>' % (path, path),
                            timeout=5)
        else:
            msg = self._msgarea.new_from_text_and_icon(
                            "KML Export Failed",
                            "You must mark the home position of the flight first.",
                            message_type=gtk.MESSAGE_ERROR,
                            timeout=5)
        msg.show_all()

    def on_menu_item_select_uav_activate(self, *args):
        tv = self.get_resource("treeview_select_uav")
        tv.set_model(self._uav_detected_model)
        dlg = self.get_resource("dialog_select_uav")
        dlg.set_transient_for(self.window)
        dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        resp = dlg.run()
        dlg.hide()

        if resp == gtk.RESPONSE_OK:
            model, iter_ = tv.get_selection().get_selected()
            if iter_:
                acid = model.get_value(iter_, 1)
                self._source.select_uav(acid)

    def on_menu_item_refresh_uav_activate(self, *args):
        self._source.refresh_uav_info()

    def on_menu_item_request_telemetry_activate(self, *args):
        self.telemetrycontroller.request_telemetry()

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
        gtk.main()

