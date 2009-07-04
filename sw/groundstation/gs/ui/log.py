import re
import gtk

class LogWindow(gtk.Window):
    def __init__(self, buf):
        gtk.Window.__init__(self)

        tv = gtk.TextView(buf)
        tv.props.editable = False
        tv.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))

        sw = gtk.ScrolledWindow()
        sw.get_vadjustment().connect("changed", self._scroll_changed)
        sw.get_vadjustment().connect("value-changed", self._scroll_value_changed)

        sw.add(tv)

        self.add(sw)
        self.set_default_size(600, 500)
        self.set_title("Log Messages")

    # The following code is taken from pychess project;
    # it keeps the scroller at the bottom of the text
    # Thanks to Thomas Dybdahl Ahle who sent it to me
    def _scroll_changed(self, vadjust):
        if not hasattr(vadjust, "need_scroll") or vadjust.need_scroll:
            vadjust.set_value(vadjust.upper-vadjust.page_size)
            vadjust.need_scroll = True

    def _scroll_value_changed(self, vadjust):
        vadjust.need_scroll = abs(vadjust.value + vadjust.page_size - vadjust.upper) < vadjust.step_increment

class LogBuffer(gtk.TextBuffer):
    """
    Log buffer storage.

    Implement a log buffer, which automatically appends
    a log at the end, with the right color, and limit the
    buffer size to a specified value.

    To be used within a gtk.TextView.
    """

    FORMAT = "[%(levelname)-9s]%(name)s::%(message)s"
    MAX_LINE_COUNT = 100

    def __init__(self):
        gtk.TextBuffer.__init__(self)

        self.create_tag('TRACE', foreground='blue', background='black', font="courrier 8")
        self.create_tag('DEBUG', foreground='lightblue', background='black', font="courrier 8")
        self.create_tag('INFO', foreground='white', background='black', font="courrier 8")
        self.create_tag('WARNING', foreground='yellow', background='black', font="courrier 8")
        self.create_tag('ERROR', foreground='red', background='black', font="courrier 8")
        self.create_tag('EXCEPTION', foreground='violet', background='black', font="courrier 8")
        self.create_tag('CRITICAL', foreground='white', background='red', font="courrier 8")

    def write(self, msg):
        self.begin_user_action()
        try:
            try:
                level = msg[1:10].strip()
                self.insert_with_tags_by_name(self.get_end_iter(), msg, level)
            except IndexError:
                self.insert_with_tags_by_name(self.get_end_iter(), msg, 'INFO')
            overflow = self.get_line_count() - self.MAX_LINE_COUNT
            if overflow > 0:
                self.delete(self.get_iter_at_line(0), self.get_iter_at_line(overflow))
                # todo: scroll to the bottom of the buffer
        finally:
            self.end_user_action()

    def clear(self):
        self.begin_user_action()
        try:
            self.delete(*self.get_bounds())
        finally:
            self.end_user_action()

    def flush(self):
        pass
