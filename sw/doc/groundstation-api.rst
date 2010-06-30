=================
Groundstation API
=================

.. autosummary::

    wasp.messages.PyField
    wasp.messages.PyMessage
    wasp.messages.MessagesFile
    wasp.settings.Setting
    wasp.settings.SettingsFile
    libserial.SerialChooser.SerialChooser
    libserial.SerialSender.SerialSender
    gs.plugin.Plugin
    gs.config.ConfigurableIface
    gs.source.UAVSource
    gs.source.MessageCb

-----------
libwasp API
-----------

.. automodule:: wasp
   :members:

.. automodule:: wasp.messages
   :members:
   :undoc-members:

.. automodule:: wasp.communication
   :members:
   :undoc-members:

.. automodule:: wasp.settings
   :members:
   :undoc-members:

.. automodule:: wasp.transport
   :members:
   :undoc-members:

.. automodule:: wasp.monitor
   :members:
   :undoc-members:

-------------
libserial API
-------------

.. automodule:: libserial
   :members:

.. automodule:: libserial.SerialChooser
   :members:
   :undoc-members:

.. automodule:: libserial.SerialSender
   :members:
   :undoc-members:

--------------------------------------------
Extending the Groundstation (The Plugin API)
--------------------------------------------

.. autoclass:: gs.plugin.Plugin
   :members:

.. autoexception:: gs.plugin.PluginNotSupported

.. autoclass:: gs.config.ConfigurableIface
   :members:

.. autoclass:: gs.groundstation.Groundstation
   :members:

.. autoclass:: gs.source.UAVSource
   :members:

.. autoclass:: gs.source.MessageCb
   :members:
