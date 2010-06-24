import datetime
import logging
import os.path
import gobject
import gtk

import gs.ui
import gs.ui.progressbar as progressbar

LOG = logging.getLogger("infobox")

class InfoBox:

    def __init__(self, source, show_build=True, show_uav_status=True, show_comm_status=True):
        self.widget = gtk.VBox(spacing=10)

        #build information
        if show_build:
            vb, (
            self.rev_value,
            self.branch_value,
            self.target_value,
            self.dirty_value,
            self.time_value) = self._build_aligned_labels("Revision","Branch","Target","Dirty","Time")
            self.widget.pack_start(
                self._build_section(
                    "Build Information",
                    gs.ui.get_icon_image(stock=gtk.STOCK_HOME),
                    vb),
                True,True)

            source.register_interest(self._on_build_info, 2, "BUILD_INFO")

        #UAV status
        if show_uav_status:
            vb, (
            self.id_value,
            self.runtime_value,
            self.rc_value,
            self.gps_value,
            self.in_flight_value,
            self.motors_on_value,
            self.autopilot_mode_value) = self._build_aligned_labels("ID","Runtime","RC","GPS","In Flight","Autopilot","Motors")
            self.widget.pack_start(
                self._build_section(
                    "UAV Status",
                    gs.ui.get_icon_image("dashboard.svg"),
                    vb),
                True,True)
            self._batt_pb = progressbar.ProgressBar(range=(8,15), average=5)
            self._build_progress_bar_holder(vb, "Battery:", self._batt_pb)
            self._cpu_pb = progressbar.ProgressBar(range=(0,100))
            self._build_progress_bar_holder(vb, "CPU Usage:", self._cpu_pb)

            #make the progress bars the same size
            sg = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
            self._batt_pb.set_same_size(sg)
            self._cpu_pb.set_same_size(sg)

            source.register_interest(self._on_status, 5, "STATUS")
            source.register_interest(self._on_time, 2, "TIME")

        #Communication status
        if show_comm_status:
            vb, (
            self.type_value,
            self.config_value,
            self.connected_value,
            self.rate_value,
            self.overruns_value,
            self.errors_value) = self._build_aligned_labels("Type", "Configuration", "Open", "Rate", "Overruns", "Errors")
            self.widget.pack_start(
                self._build_section(
                    "Communication Status",
                    gs.ui.get_icon_image("radio.svg"),
                    vb),
                True,True)

            source.connect("source-connected", self._on_source_connected)
            source.register_interest(self._on_comm_status, 5, "COMM_STATUS")
            gobject.timeout_add(1000, self._check_messages_per_second, source)

    def _build_progress_bar_holder(self, vb, name, pb):
        vb.pack_start(self._build_label(text=name), False, False)
        h = gtk.HBox()
        h.pack_start(pb,False,True)
        vb.pack_start(h, False, False)

    def _build_label(self, text=None, markup=None):
        l = gtk.Label()
        l.set_alignment(0.0,0.5)
        if text:
            l.set_text(text)
        if markup:
            l.set_markup(markup)
        return l

    def _build_aligned_labels(self, *names):
        sg = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        vb = gtk.VBox()
        lbls = []
        for name in names:
            hb = gtk.HBox()
            n = self._build_label(text="%s: " % name)
            sg.add_widget(n)
            hb.pack_start(n, False, False)
            lbl = self._build_label()
            lbls.append(lbl)
            hb.pack_start(lbl, False, False)
            vb.pack_start(hb, False, True)
        return vb, lbls

    def _build_section(self, name, image, widget):
        hb = gtk.HBox(spacing=5)
        image.set_alignment(0.5,0.0)
        image.set_padding(5,10)
        hb.pack_start(image, False, False)
        vb = gtk.VBox()
        l = self._build_label(markup="<b>%s</b>" % name)
        vb.pack_start(l, False, False)
        a = gtk.Alignment(0.0,0.5,1.0,1.0)
        a.set_padding(0,0,10,0)
        a.add(widget)
        vb.pack_start(a, False, True)
        hb.pack_start(vb, True, True)
        return hb

    def _check_messages_per_second(self, source):
        self.rate_value.set_text("%.1f msgs/s" % source.get_messages_per_second())
        return True

    def _on_source_connected(self, source, connected):
        if connected:
            self.connected_value.set_text("YES")
        else:
            self.connected_value.set_text("NO")

        comm_type, comm_config = source.get_connection_parameters() 
        self.type_value.set_text(comm_type)
        self.config_value.set_text(comm_config)

    def _on_status(self, msg, header, payload):
        rc, gps, bv, in_flight, motors_on, autopilot_mode, cpu_usage = msg.unpack_values(payload)
        self.id_value.set_text(
                str(header.acid))
        self.rc_value.set_text(
                msg.get_field_by_name("rc").get_printable_value(rc))
        self.gps_value.set_text(
                msg.get_field_by_name("gps").get_printable_value(gps))
        self.in_flight_value.set_text(
                msg.get_field_by_name("in_flight").get_printable_value(in_flight))
        self.motors_on_value.set_text(
                msg.get_field_by_name("motors_on").get_printable_value(motors_on))
        self.autopilot_mode_value.set_text(
                msg.get_field_by_name("autopilot_mode").get_printable_value(autopilot_mode))

        self._cpu_pb.set_value(cpu_usage)
        self._batt_pb.set_value(bv/10.0)

    def _on_comm_status(self, msg, header, payload):
        overruns, errors = msg.unpack_printable_values(payload, joiner=None)
        self.overruns_value.set_text(overruns)
        self.errors_value.set_text(errors)

    def _on_time(self, msg, header, payload):
        runtime, = msg.unpack_printable_values(payload, joiner=None)
        self.runtime_value.set_text(runtime)

    def _on_build_info(self, msg, header, payload):
        rev, branch, target, dirty, time = msg.unpack_printable_values(payload, joiner=None)

        #gtk.Label does not like strings with embedded null
        def denull(s):
            return s.replace("\x00","")

        self.rev_value.set_text(denull(rev))
        self.branch_value.set_text(denull(branch))
        self.target_value.set_text(denull(target))
        self.dirty_value.set_text(dirty)

        t = datetime.datetime.fromtimestamp(int(time))
        self.time_value.set_text(t.strftime("%d/%m/%Y %H:%M:%S"))



