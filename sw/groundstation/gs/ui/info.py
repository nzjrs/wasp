import datetime
import logging
import os.path
import gobject
import gtk

import gs.ui
import gs.ui.progressbar as progressbar

LOG = logging.getLogger("infobox")

def set_image_from_file(image, filename):
    pb = gtk.gdk.pixbuf_new_from_file_at_size(
                    filename,
                    *gtk.icon_size_lookup(gtk.ICON_SIZE_DIALOG)
    )
    image.set_from_pixbuf(pb)

class InfoBox(gs.ui.GtkBuilderWidget):
    def __init__(self, source):
        mydir = os.path.dirname(os.path.abspath(__file__))
        ui = os.path.join(mydir, "info.ui")
        gs.ui.GtkBuilderWidget.__init__(self, ui)

        self.widget = self.get_resource("info_vbox")

        #change the status icon
        set_image_from_file(
            self.get_resource("status_image"),
            os.path.join(mydir,"icons","dashboard.svg")
        )
        #change the comm icon
        set_image_from_file(
            self.get_resource("comm_image"),
            os.path.join(mydir,"icons","radio.svg")
        )

        self.pb = progressbar.ProgressBar(range=(8,15), average=5)
        self.get_resource("batt_hbox").pack_start(self.pb, True)

        source.serial.connect("serial-connected", self._on_serial_connected, source)

        source.register_interest(self._on_status, 5, "STATUS")
        source.register_interest(self._on_comm_status, 5, "COMM_STATUS")
        source.register_interest(self._on_time, 2, "TIME")
        source.register_interest(self._on_build_info, 2, "BUILD_INFO")

        gobject.timeout_add_seconds(1, self._check_messages_per_second, source)

    def _check_messages_per_second(self, source):
        self.get_resource("rate_value").set_text("%.1f msgs/s" % source.get_messages_per_second())
        return True

    def _on_serial_connected(self, serial, connected, source):
        if connected:
            self.get_resource("connected_value").set_text("YES")

            port, speed = source.get_connection_parameters()
            self.get_resource("port_value").set_text(port)
            self.get_resource("speed_value").set_text("%s baud" % speed)
        else:
            self.get_resource("connected_value").set_text("NO")

    def _on_status(self, msg, payload):
        rc, gps, bv = msg.unpack_values(payload)
        self.get_resource("rc_value").set_text(
                msg.get_field_by_name("rc").get_printable_value(rc))
        self.get_resource("gps_value").set_text(
                msg.get_field_by_name("gps").get_printable_value(gps))

        self.pb.set_value(bv/10.0)

    def _on_comm_status(self, msg, payload):
        overruns, errors = msg.unpack_printable_values(payload, joiner=None)
        self.get_resource("overruns_value").set_text(overruns)
        self.get_resource("errors_value").set_text(errors)

    def _on_time(self, msg, payload):
        runtime, = msg.unpack_printable_values(payload, joiner=None)
        self.get_resource("runtime_value").set_text(runtime)

    def _on_build_info(self, msg, payload):
        rev, branch, target, dirty, time = msg.unpack_printable_values(payload, joiner=None)

        #gtk.Label does not like strings with embedded null
        def denull(s):
            return s.replace("\x00","")

        self.get_resource("rev_value").set_text(denull(rev))
        self.get_resource("branch_value").set_text(denull(branch))
        self.get_resource("target_value").set_text(denull(target))
        self.get_resource("dirty_value").set_text(dirty)

        t = datetime.datetime.fromtimestamp(int(time))
        self.get_resource("time_value").set_text(t.strftime("%d/%m/%Y %H:%M:%S"))

if __name__ == "__main__":
    i = InfoBox()

    w = gtk.Window()
    w.add(i.widget)
    w.show_all()
    w.connect("delete-event", lambda *a: gtk.main_quit())

    i.set_build_info("123", 0, 0, 0, 0)

    gtk.main()
