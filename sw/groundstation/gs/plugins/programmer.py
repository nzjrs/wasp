import gtk
import gobject
import os.path
import logging
import subprocess

import gs.ui
import gs.plugin as plugin

LOG = logging.getLogger('programmer')

class Programmer(plugin.Plugin, gs.ui.GtkBuilderWidget):

    ANIMATION = ("|","/","-","\\")

    def __init__(self, conf, source, messages_file, groundstation_window):
        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "programmer.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        pb = gs.ui.get_icon_pixbuf("electronics.svg",size=gtk.ICON_SIZE_MENU)
        item = gtk.ImageMenuItem("Program Autopilot")
        item.set_image(gtk.image_new_from_pixbuf(pb))
        item.connect("activate", self._show_window)
        groundstation_window.add_menu_item("UAV", item)

        #calculate path to onboard dir
        self._onboard_dir = os.path.abspath(os.path.join(mydir, "..", "..", "..", "onboard"))

        #not currently running
        self._process = None
        #yucky running animation
        self._anim = 0

        self._win = self.get_resource("mainwindow")
        self._win.set_icon(pb)
        self._win.set_title("Program Autopilot")
        self._win.connect("delete-event", gtk.Widget.hide_on_delete)
        self._status = self.get_resource("status_label")
        self.get_resource("program_button").connect("clicked", self._on_program)
        self.get_resource("close_button").connect("clicked", self._on_close)
        self.get_resource("cancel_button").connect("clicked", self._on_cancel)

    def _show_window(self, *args):
        self._win.show_all()

    def _set_status_label(self, txt):
        self._status.set_markup('<span face="monospace">%s</span>' % txt)

    def _check_make(self):
        self._process.poll()
        if self._process.returncode != None:
            if self._process.returncode != 0:
                self._set_status_label("Error")
            else:
                self._set_status_label("Finished")
            self._process = None
            return False
        else:
            self._anim = (self._anim + 1) % len(self.ANIMATION)
            self._set_status_label("Running (%s)" % self.ANIMATION[self._anim])
            return True

    def _run_make(self, target="autopilot_main"):
        LOG.info("Running make, target: %s" % target)
        self._anim = 0
        self._set_status_label("Running (%s)" % self.ANIMATION[self._anim])
        self._process = subprocess.Popen(
                            "make upload TARGET=%s" % target,
                            cwd=self._onboard_dir,
                            shell=True,
                            stdout=None,
                            stderr=None)
        gobject.timeout_add_seconds(1, self._check_make)

    def _on_program(self, *args):
        if not self._process:
            self._run_make()
        else:
            LOG.info("Not programming, process allready running")

    def _on_close(self, *args):
        self._win.hide()

    def _on_cancel(self, *args):
        if self._process and self._process.returncode == None:
            self._process.terminate()


