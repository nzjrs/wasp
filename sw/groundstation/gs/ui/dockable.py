import gtk
import logging

LOG = logging.getLogger("dockable")

class DockableNotebookPageMixin:
    def __init__(self, parent_notebook, window, dock_button, label):
        self._window = window
        self._page = window.get_child()
        self._holder = gtk.VBox()
        self._parent_notebook = parent_notebook

        self._window.connect("delete-event", self._on_window_delete)        
        dock_button.connect("released", self._on_dock_button_released)

        self._window.set_title(label)
        self._parent_notebook.append_page(self._holder, gtk.Label(label))

        self._page.reparent(self._holder)

    def _on_window_delete(self, widget):
        self.dock_handler()
        return True

    def _on_dock_button_released(self, widget):
        self.dock_handler()

    def dock_handler(self, forceDock=False):
        if forceDock or self._page.get_parent() == self._window:
            self._holder.show_all()
            self._page.reparent(self._holder)
            self._window.hide_all()
            
            self._parent_notebook.show()
        elif self._page.get_parent() == self._holder:
            self._window.show_all()            
            self._page.reparent(self._window)
            self._holder.hide_all()

            container_hide = True
            for child in self._parent_notebook.get_children():
                if child.props.visible == True:
                    container_hide = False
            if container_hide:
                self._parent_notebook.hide()
	
		
