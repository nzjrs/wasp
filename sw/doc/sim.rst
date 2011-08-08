Simulator
=================

Prerequisites for Building
**************************
- Download, compile and install JSBSim

::

    cvs -z3 -d:pserver:anonymous@jsbsim.cvs.sourceforge.net:/cvsroot/jsbsim co -P JSBSim 
    cd JSBSim
    ./autogen.sh --enable-libraries --enable-shared --prefix=/opt/jsbsim
    make
    sudo make install

- Install libglib2.0-dev 

Building and Running
********************
First check out (and create) the correct branch::

    $ git checkout -b sim origin/sim
 
From the onboard directory::

    $ make ARCH=jsbsim TARGET=test/test_led_main
    $ LD_LIBRARY_PATH=/opt/jsbsim/lib/ ./bin/jsbsim/test/test_led_main.elf

The simulator is also affected by some environment variables

:WASP_NO_FLIGHTGEAR:    Disables FlightGear visualisation
