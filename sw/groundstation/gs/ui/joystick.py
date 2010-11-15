import gtk
import gobject

import gs.joystick
import gs.ui.progressbar as progressbar

class JoystickWidget(gtk.VBox):
    def __init__(self, num_axis=8, show_uncalibrated=False, show_buttons=False, **kwargs):
        gtk.VBox.__init__(self, spacing=5)

        axis_labels = kwargs.get("axis_labels", ["%d:" % i for i in range(num_axis)])
        assert len(axis_labels) == num_axis

        self.show_uncalibrated = show_uncalibrated
        self.show_buttons = show_buttons

        self.progress = [
                progressbar.ProgressBar(
                    range=(-32767,32767),
                    label=axis_labels[i],
                    **kwargs) for i in range(num_axis)]
        for p in self.progress:
            self.pack_start(p, False, False)

        self.joystick = None
        self.joystick_axis_id = None
        self.joystick_button_id = None

        self.button_vals = {}
        if show_buttons:
            hb = gtk.HBox()
            hb.pack_start(gtk.Label("Buttons: "), False, False)
            self.button_label = gtk.Label("")
            self.button_label.props.xalign = 0.0
            hb.pack_start(self.button_label, True, True)
            self.pack_start(hb, False, False)

        #update the joystick values in an idle handler, otherwise we
        #redraw the UI far too fast
        self.joystick_values = {}
        gobject.timeout_add(1000/20, self._update_progressbars)

    def set_joystick(self, joystick):
        self.joystick = joystick
        self.joystick_axis_id = self.joystick.connect("axis", self._on_joystick_event)
        self.joystick_button_id = self.joystick.connect("button", self._on_joystick_button)

    def _on_joystick_button(self, joystick, button_num, button_value, init):
        self.button_vals[button_num] = button_value

    def _on_joystick_event(self, joystick, joystick_axis, joystick_value, init):
            if self.show_uncalibrated:
                joystick_axis, joystick_value = self.joystick.get_uncalibrated_axis_and_value(joystick_axis)
            self.joystick_values[joystick_axis] = joystick_value

    def _update_progressbars(self):
        while True:
            try:
                axis, value = self.joystick_values.popitem()
                self.progress[axis].set_value(value)
            except IndexError:
                #ignored axis
                pass
            except KeyError:
                #dict empty, finished updating all axis
                break

        if self.show_buttons:
            depressed = [str(b) for b in self.button_vals if self.button_vals[b]]
            self.button_label.set_text(','.join(depressed))

        return True

if __name__ == "__main__":
    w = gtk.Window()
    jsw = JoystickWidget(show_range=False, show_buttons=True)
    jsw.set_joystick(gs.joystick.Joystick(0))
    w.add(jsw)
    w.show_all()
    w.connect("delete-event", gtk.main_quit)
    gtk.main()

