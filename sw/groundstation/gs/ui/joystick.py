import gtk

import gs.joystick
import gs.ui.progressbar as progressbar

class JoystickWidget(gtk.VBox):
    def __init__(self, num_axis=8, show_uncalibrated=False, **kwargs):
        gtk.VBox.__init__(self, spacing=5)

        axis_labels = kwargs.get("axis_labels", ["%d:" % i for i in range(num_axis)])
        assert len(axis_labels) == num_axis

        self.show_uncalibrated = show_uncalibrated
        self.progress = [
                progressbar.ProgressBar(
                    range=(-32767,32767),
                    label=axis_labels[i],
                    **kwargs) for i in range(num_axis)]
        for p in self.progress:
            self.pack_start(p, False, False)

        self.joystick = None
        self.joystick_id = None

    def set_joystick(self, joystick):
        self.joystick = joystick
        self.joystick_id = self.joystick.connect("axis", self._on_joystick_event)

    def _on_joystick_event(self, joystick, joystick_axis, joystick_value, init):
        try:
            if self.show_uncalibrated:
                joystick_axis, joystick_value = self.joystick.get_uncalibrated_axis_and_value(joystick_axis)
            self.progress[joystick_axis].set_value(joystick_value)
        except IndexError:
            #ignored axis
            pass

if __name__ == "__main__":
    w = gtk.Window()
    jsw = JoystickWidget(show_range=False)
    jsw.set_joystick(gs.joystick.Joystick(0))
    w.add(jsw)
    w.show_all()
    w.connect("delete-event", gtk.main_quit)
    gtk.main()

