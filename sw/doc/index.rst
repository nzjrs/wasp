Software
========

Wasp software consists of 2 main pieces; :doc:`onboard` software written in C/C++ which
runs on the UAV, and :doc:`groundstation` software, primarily written in python, which runs
on a desktop PC.

.. image:: wasp.png

Additionally, there are a number of tools and similar utilities, primarily written in python
which bridge the pieces together.

An important common element in all pieces is the :doc:`comm-protocol`, which defines the
binary interface between the pieces. To setup or customize the :xref:`wasp` system for
a new UAV see :doc:`configuration`

.. toctree::
   :maxdepth: 2

   setup
   onboard
   groundstation
   sim
   configuration
   comm-protocol
   
