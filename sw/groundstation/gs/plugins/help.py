import gtk

import gs.plugin as plugin

class Help(plugin.Plugin):

    def __init__(self, conf, source, messages_file, settings_file, groundstation_window):
        self._add_link(groundstation_window, 
                "Wasp Documentation",
                "http://www.waspuav.org/doc/")

    def _add_link(self, groundstation_window, name, url):
        item = gtk.ImageMenuItem(name)
        item.set_image(gtk.image_new_from_stock(gtk.STOCK_HELP, gtk.ICON_SIZE_MENU))
        item.connect("activate", self._show_url, url)
        groundstation_window.add_menu_item("Help", item)

    def _show_url(self, menuitem, url):
        gtk.show_uri(None, url, gtk.gdk.CURRENT_TIME)
