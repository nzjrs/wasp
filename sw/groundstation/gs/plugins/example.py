import gtk
import logging

import wasp
import gs.plugin as plugin

# This LOG object can be used for printing messages that will be visible
# both on the console, and in the log window (Help->Show Log)
LOG = logging.getLogger('example')

# All plugins must inherit from plugin.Plugin
class ExamplePlugin(plugin.Plugin):
    def __init__(self, conf, source, messages_file, settings_file, groundstation_window):
        # You should comment out the following two lines in your plugin. This
        # statement stops the plugin from loading unless the groundstation is
        # launched in a special 'testing' mode. See the groundstation documentation
        # in the Environment Variables section for more information
        if not wasp.IS_TESTING:
            raise plugin.PluginNotSupported("Only enabled when WASP_IS_TESTING")

        # We will be sending the 'PING' message. For a complete listing of 
        # messages the UAV may understand, see messages.xml
        self.ping_msg = messages_file.get_message_by_name("PING")

        # Keep a reference to the source because we need it to send messages to
        # the UAV
        self.source = source
        # We also want to monitor messages that the UAV sends us. In this case
        # we register_interest in the message
        self.source.register_interest(self._got_time_message, 0, "TIME")

        # Here we create a menu item to be shown in the GUI. The typical plugin
        # creates such a menu item, and then shows its own window when the menu
        # item is clicked
        item = gtk.MenuItem("Example Plugin Window")
        # Now we connect to the 'activate' signal. This means when the menu item
        # is clicked, the supplied function (self._on_menu_item_clicked) is
        # called
        item.connect("activate", self._on_menu_item_clicked)
        # Now we add the menu item to the GUI 'UAV' menu
        groundstation_window.add_menu_item("File", item)

        # Now we create our user interface (UI) using pygtk. If you are creating
        # A complex UI I recommend using glade and gtkbuilder and then using
        # gs.ui.GtkBuilderWidget to load the .ui file. See the programmer plugin
        # for a more complete examle.
        #
        # In this case it is not necessary, our UI is simple and will include
        # a button that sends a message and a label that shows the UAV runtime,
        # as seen below
        #
        # +----------------+
        # |  +----------+  |
        # |  |  button  |  |
        # |  +----------+  |
        # |     label      |
        # +----------------+
        #
        # Create the main window and connect to the delete-event signal to stop
        # it being destroyed when closed (it is hidden instead)
        self.ui = gtk.Window()
        self.ui.connect("delete-event", gtk.Widget.hide_on_delete)
        vb = gtk.VBox()                             # A box to contain our UI widgets
        b = gtk.Button("Send Message")              # Create the button
        b.connect("clicked", self._send_message)    # Like above, connect to 'clicked'
        self.label = gtk.Label("0")                 # The label to show runtime
        vb.pack_start(b, False, False)              # Add the button to the box
        vb.pack_start(self.label, False, False)     # Add the label to the box
        self.ui.add(vb)                             # Add the box to the UI


    def _on_menu_item_clicked(self, menuitem):
        LOG.debug("Menu item clicked")      # Print a message to the log
        self.ui.show_all()                  # Make our UI visible

    def _send_message(self, button):
        LOG.debug("Send Message Clicked")
        # Send the message we stored earlier. Not that the PING message takes
        # no parameters - ()
        self.source.send_message(self.ping_msg, ())

    def _got_time_message(self, msg, header, payload):
        # Now we need to break the message up into all is parts. From looking
        # at messages.xml we know that the TIME message only has one field, 
        # so we only need to unpack it into one variable (runtime)
        runtime, = msg.unpack_values(payload)
        # We now update the UI to show this 
        self.label.set_text("%d seconds" % runtime)

