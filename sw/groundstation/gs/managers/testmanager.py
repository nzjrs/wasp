import logging

import gs.config as config

LOG = logging.getLogger('testmanager')

class TestManager(config.ConfigurableIface):
    CONFIG_SECTION = "TEST"
    def __init__(self, conf):
        config.ConfigurableIface.__init__(self, conf)

    def update_state_from_config(self):
        LOG.info("Updating state from config")

    def update_config_from_state(self):
        LOG.info("Updating config from state")
        self.config_set("test_combo",   "1")
        self.config_set("test_entry",   "foo")
        self.config_set("test_radio",   "A")
        self.config_set("e1",           "bar")
        self.config_set("e2",           "baz")
        self.config_set("123",          None)

    def get_preference_widgets(self):
        c1 = self.build_combo("test_combo", "1","2","3")
        e0 = self.build_entry("test_entry")
        g1 = self.build_radio_group("test_radio", "A","B","C")
        e1 = self.build_entry("e1")
        e2 = self.build_entry("e2")

        sg = self.make_sizegroup()

        items = [c1, e0, e1, e2]
        items += g1

        frame = self.build_frame("foo", [
            c1,
            e0,
            g1[0],
            self.build_label("Short", e1, sg),
            self.build_label("Much Longer Label", e2, sg),
            g1[1],
            g1[2]
        ])

        return "Test Manager", frame, items
