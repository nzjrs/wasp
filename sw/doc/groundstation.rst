Groundstation
=============

The Wasp groundstation is the main point from which to configure, control
and test any UAV built using the Wasp framework. Once you have 
completed :ref:`groundstation-setup` the easiest way to start the groundstation
to explore its functionality is to execute the following command from the
groundstation directory (note: you do not need to have a UAV at this point)::

./groundstation -t

This launches the groundstation mode with a test (**-t**) data source.

.. image:: groundstation.png

Configuration
-------------

Configuration occurs via the ``File->Preferences`` menu item. Configuration values
are written to ``$HOME/.config/wasp/groundstation.ini``

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

The following environment variables also influence the groundstation
display

:WASP_HOME_LAT:     The default latitude for the test data source
:WASP_HOME_LON:     The default longitude for the test data source
:WASP_IS_TESTING:   Sets additional debug/testing conditions in the groundstation

Extending the Groundstation
---------------------------

The groundstation has a powerful and easy to use API for writing 
plugins to extend its functionality. For a complete reference of the API
please see the following;

.. toctree::
   :maxdepth: 1

   groundstation-api

Example Groundstation Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example plugin which has its own user interface. It
contains a label which shows data received from the UAV, and a single button,
which when clicked sends a message to the UAV.

The plugin file (e.g. foo.py) should reside in the
**sw/groundstation/gs/plugins** directory

.. literalinclude:: /sw/groundstation/gs/plugins/example.py

Tablet UI
---------

There is a capable yet simple tablet focused UI for :xref:`wasp`. This uses
the same software as the desktop UI and has been tested on the following devices

* Nokia n800

.. image:: tablet.png

Installing
^^^^^^^^^^

First install the dependencies

* python-gtk2
* python-serial

You may need to install python-serial manually; e.g by manually copying into /usr/lib/pythonX.X/site-packages. You
also need to install the appropriate kernel modules. Copy the files located
`here <https://github.com/nzjrs/wasp/tree/master/sw/groundstation/data/n800/>`_ into ``/home/user/``

Running
^^^^^^^

Running is a bit complicated because there is no serial port on the n800. You can connect a
XBEE modem into the USB port, but you must

1. Power the XBEE externally (i.e. not from the USB port)
2. Connect the XBEE into the n800 via a USB-OTG adapter

Once the hardware preparation has been made, the following steps must be performed in this order

1. Plug in OTG adapter (but do not plug XBEE into it yet)
2. Power on XBEE
3. Power on n800
4. Wait for the n800 to start
5. Open a terminal and type

.. code-block:: bash

   sudo gainroot
   cd /home/user/
   ./setup-serial.sh

5. Now plug the XBEE USB into the OTG adapter. There should be some activity on the screen (a USB logo may
   appear).
6. Check the serial port was created in a terminal

.. code-block:: bash

   ls /dev/ttyUSB*

7. If ``/dev/ttyUSB0`` is not listed in the output of #6 then type ``dmesg`` to see what went wrong.
8. Start the tablet groundstation


