Architecture
============

.. image:: wasp.png

Wasp has a hardware abstraction layer which isolates the software from the 
hardware implementing the defined interfaces. For a minimal HAL implementation
please study null.c

.. image:: hal.png

.. image:: autopilot.png

The main link between the Groundstation and the Onboard software is through 
the communication layer.

.. doxygenfunction:: comm_send_message
   :project: onboard

.. doxygenstruct:: CommMessage_t
   :project: onboard

For a complete description of all communication messages please see

.. toctree::
   :maxdepth: 2

   comm-protocol
