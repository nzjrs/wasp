import gtk
import logging

import gs.plugin as plugin
import gs.config as config

LOG = logging.getLogger('testmanager')

class TestConfigurable(plugin.Plugin, config.ConfigurableIface):
    CONFIG_SECTION = "TEST"
    def __init__(self, conf, source, messages_file, groundstation_window):
        config.ConfigurableIface.__init__(self, conf)
        self.ck = "0"

#        groundstation_window.add_menu_item("Foo", gtk.MenuItem("test1"))
#        groundstation_window.add_menu_item("File", gtk.MenuItem("test2"))

    def update_state_from_config(self):
        self.ck = self.config_get("Test_Check","0")
        LOG.info("Updating state from config. Check: %s" % self.ck)

    def update_config_from_state(self):
        LOG.info("Updating config from state")
        self.config_set("test_combo",   "1")
        self.config_set("test_entry",   "foo")
        self.config_set("test_radio",   "A")
        self.config_set("Test_Check",   self.ck)
        self.config_set("e1",           "bar")
        self.config_set("e2",           "baz")
        self.config_set("123",          None)

    def get_preference_widgets(self):
        c1 = self.build_combo("test_combo", "1","2","3")
        e0 = self.build_entry("test_entry")
        g1 = self.build_radio_group("test_radio", "A","B","C")
        e1 = self.build_entry("e1")
        e2 = self.build_entry("e2")
        ck1 = self.build_checkbutton("Test_Check")

        sg = self.build_sizegroup()

        items = [c1, ck1, e0, e1, e2]
        items += g1

        frame = self.build_frame("foo", [
            c1,
            ck1,
            e0,
            g1[0],
            self.build_label("Short", e1, sg),
            self.build_label("Much Longer Label", e2, sg),
            g1[1],
            g1[2]
        ])

        return "Test Manager", frame, items
