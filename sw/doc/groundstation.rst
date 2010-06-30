Groundstation
=============

The Wasp groundstation is the main point from which to configure, control
and test any UAV built using the Wasp framework. Once you have 
completed :ref:`groundstation-setup` the easiest way to start the groundstation
to explore its functionality is to execute the following command from the
groundstation directory (note: you do not need to have a UAV at this point)::

./groundstation -t

This launches the groundstation mode with a test (**-t**) data source.

Configuration
-------------

TODO

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
plugins to extend its functionality. Please see the following;

.. toctree::
   :maxdepth: 1

   groundstation-api
