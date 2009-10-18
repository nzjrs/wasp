import gtk
import gobject
import os.path
import logging
import subprocess

import gs.ui
import gs.plugin as plugin

LOG = logging.getLogger('programmer')

class TestConfigurable(plugin.Plugin, gs.ui.GtkBuilderWidget):

    ANIMATION = ("|","/","-","\\")

    def __init__(self, conf, source, messages_file, groundstation_window):
        mydir = os.path.dirname(os.path.abspath(__file__))
        uifile = os.path.join(mydir, "programmer.ui")
        gs.ui.GtkBuilderWidget.__init__(self, uifile)

        item = gtk.MenuItem("Program")
        item.connect("activate", self._show_window)
        groundstation_window.add_menu_item("UAV", item)

        #calculate path to onboard dir
        self._onboard_dir = os.path.abspath(os.path.join(mydir, "..", "..", "..", "onboard"))

        #not currently running
        self._process = None
        #yucky running animation
        self._anim = 0

        self._win = self.get_resource("programmer_window")
        self._status = self.get_resource("status_label")
        self._win.connect("delete-event", self._window_closed)
        self.get_resource("clear_button").connect("clicked", self._on_clear)
        self.get_resource("program_button").connect("clicked", self._on_program)
        self.get_resource("close_button").connect("clicked", self._on_close)

    def _show_window(self, *args):
        self._win.show_all()

    def _window_closed(self, *args):
        #hide window, don't destroy it
        self._win.hide()
        return True

    def _check_make(self):
        self._process.poll()
        if self._process.returncode != None:
            if self._process.returncode != 0:
                self._status.set_markup('<span face="monospace">Error</span>')
            else:
                self._status.set_markup('<span face="monospace">Finished</span>')
            self._process = None
            return False
        else:
            self._anim = (self._anim + 1) % len(self.ANIMATION)
            self._status.set_markup('<span face="monospace">Running (%s)</span>' % self.ANIMATION[self._anim])
            return True

    def _run_make(self, target="autopilot_main"):
        if not self._process:
            self._process = subprocess.Popen(
                                "make upload TARGET=%s" % target,
                                cwd=self._onboard_dir,
                                shell=True,
                                stdout=None,
                                stderr=None)
            gobject.timeout_add_seconds(1, self._check_make)

    def _on_clear(self, *args):
        LOG.debug("clear")

    def _on_program(self, *args):
        LOG.debug("program")
        self._run_make()

    def _on_close(self, *args):
        self._win.hide()

