import gtk
import logging

import wasp
import gs.plugin as plugin
import gs.config as config

LOG = logging.getLogger('testmanager')

class TestConfigurable(plugin.Plugin, config.ConfigurableIface):
    CONFIG_SECTION = "TEST"
    def __init__(self, conf, source, messages_file, settings_file, groundstation_window):
        config.ConfigurableIface.__init__(self, conf)
        if not wasp.IS_TESTING:
            raise plugin.PluginNotSupported("Only enabled when WASP_IS_TESTING")

        self.ck = "0"
        groundstation_window.add_menu_item("Foo", gtk.MenuItem("foo1"), gtk.MenuItem("foo2"))
        groundstation_window.add_submenu_item("Foo", "Bar", gtk.MenuItem("bar1"), gtk.MenuItem("bar2"))
        groundstation_window.add_menu_item("File", gtk.MenuItem("baz1"))

    def update_state_from_config(self):
        self.ck = self.config_get("Test_Check","0")
        LOG.info("Updating state from config. Check: %s" % self.ck)

    def update_config_from_state(self):
        LOG.info("Updating config from state")
        self.config_set("test_combo",       "1")
        self.config_set("test_entry",       "foo")
        self.config_set("test_radio",       "A")
        self.config_set("test_radio_num",   "0")
        self.config_set("Test_Check",       self.ck)
        self.config_set("e1",               "bar")
        self.config_set("e2",               "baz")
        self.config_set("123",              None)

    def get_preference_widgets(self):
        c1 = self.build_combo("test_combo", "1","2","3")
        e0 = self.build_entry("test_entry")
        g1 = self.build_radio_group("test_radio", "A","B","C")
        g2 = self.build_radio_group("test_radio_num", "0","1","2","3")
        e1 = self.build_entry("e1")
        e2 = self.build_entry("e2")
        ck1 = self.build_checkbutton("Test_Check")

        sg = self.build_sizegroup()

        items = [c1, ck1, e0, e1, e2]
        items += g1
        items += g2

        frame = self.build_frame("foo", [
            c1,
            ck1,
            e0,
            g1[0],
            self.build_label("Short", e1, sg=sg),
            self.build_label("Much Longer Label", e2, sg=sg),
            g1[1],
            g1[2],
            self.build_label("Horizontal Radio", self.build_hbox(*g2), sg=sg)
        ])

        return "Test Manager", frame, items
