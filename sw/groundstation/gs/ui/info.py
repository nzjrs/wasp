import datetime
import logging
import os.path
import gobject
import gtk

import gs.ui
import gs.ui.progressbar as progressbar

LOG = logging.getLogger("infobox")

class InfoBox(gs.ui.GtkBuilderWidget):
    def __init__(self, source):
        gs.ui.GtkBuilderWidget.__init__(self, gs.ui.get_ui_file("info.ui"))

        self.widget = self.get_resource("info_vbox")

        #change the status icon
        self.get_resource("status_image").set_from_pixbuf(
                gs.ui.get_icon_pixbuf("dashboard.svg"))

        #change the comm icon
        self.get_resource("comm_image").set_from_pixbuf(
                gs.ui.get_icon_pixbuf("radio.svg"))

        self._batt_pb = progressbar.ProgressBar(range=(8,15), average=5)
        self.get_resource("batt_hbox").pack_start(self._batt_pb, False)

        self._cpu_pb = progressbar.ProgressBar(range=(0,100))
        self.get_resource("cpu_hbox").pack_start(self._cpu_pb, False)

        #make the progress bars the same size
        sg = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        self._batt_pb.set_same_size(sg)
        self._cpu_pb.set_same_size(sg)

        source.connect("source-connected", self._on_source_connected)

        source.register_interest(self._on_status, 5, "STATUS")
        source.register_interest(self._on_comm_status, 5, "COMM_STATUS")
        source.register_interest(self._on_time, 2, "TIME")
        source.register_interest(self._on_build_info, 2, "BUILD_INFO")

        gobject.timeout_add_seconds(1, self._check_messages_per_second, source)

    def _check_messages_per_second(self, source):
        self.get_resource("rate_value").set_text("%.1f msgs/s" % source.get_messages_per_second())
        return True

    def _on_source_connected(self, source, connected):
        if connected:
            self.get_resource("connected_value").set_text("YES")
        else:
            self.get_resource("connected_value").set_text("NO")
        port, speed = source.get_connection_parameters()
        self.get_resource("port_value").set_text(port)
        self.get_resource("speed_value").set_text("%s baud" % speed)

    def _on_status(self, msg, payload):
        rc, gps, bv, in_flight, motors_on, autopilot_mode, cpu_usage = msg.unpack_values(payload)
        self.get_resource("rc_value").set_text(
                msg.get_field_by_name("rc").get_printable_value(rc))
        self.get_resource("gps_value").set_text(
                msg.get_field_by_name("gps").get_printable_value(gps))
        self.get_resource("in_flight_value").set_text(
                msg.get_field_by_name("in_flight").get_printable_value(in_flight))
        self.get_resource("motors_on_value").set_text(
                msg.get_field_by_name("motors_on").get_printable_value(motors_on))
        self.get_resource("autopilot_mode_value").set_text(
                msg.get_field_by_name("autopilot_mode").get_printable_value(autopilot_mode))

        self._cpu_pb.set_value(cpu_usage)
        self._batt_pb.set_value(bv/10.0)

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

