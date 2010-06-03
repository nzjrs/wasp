Setting up the Autopilot
========================

Installing the Bootloader
-------------------------
- Install lcp21isp (this can be done via synaptic)
- Connect a 3.3v compatible FTDI serial dongle to the TX0 and RX0 lines on the GPS or UART0 connector
- Ground BOOT/SDA_1 pin (ie short together pins 1 and 7 on the GPS connector) and power up the board
- From the rocket directory, execute the command

::

    make install_bootloader

Programming the Autopilot (Using the Command Line)
---------------------------------------------------
- Plug a mini USB cable into the motherboard and computer (if you’re using a virtual box, connect the “USB bootloader” to the virtual box)
- Power up the motherboard (8V seems to be fine, but can go up to 18V)
- cd into the sw/onboard directory
- Execute the command

::

    make upload

Programming the Autopilot (Using the Groundstation)
---------------------------------------------------
- Plug a mini USB cable into the motherboard and computer (if you’re using a virtual box, connect the “USB bootloader” to the virtual box)
- Power up the motherboard (8V seems to be fine, but can go up to 18V)
- Select *UAV -> Program Autopilot*

Calibrating the Radio
---------------------
- From the groundstation, select *UAV -> Calibrate Radio*
- Move all the transmitter sticks. You should see values change.
- Fill out *Name* and *Min* , *Center* , *Max* for each channel. Note that Min represents the functional min value (i.e. zero throttle, left bank) and can be numerically greater than max depending on the transmitter.
- If the channel is a switch (and will be used for switching rather than control) then check the *Filtered* box.
- Click save, which will generate a file at *~/Desktop/radio.xml*
- Replace the radio.xml in sw/onboard/config.xml with the new one and reprogram the autopilot. This should then give you proper channel mappings.

If you wish to hand edit the radio xml file, be aware of the following tags::

    <!--
    -- Attributes of root (Radio) tag :
    -- name: name of RC
    -- data_min: min width of a pulse to be considered as a data pulse
    -- data_max: max width of a pulse to be considered as a data pulse
    -- sync_min: min width of a pulse to be considered as a synchro pulse
    -- sync_max: max width of a pulse to be considered as a synchro pulse
    -- pulse_type: POSITIVE ( Futaba and others) | NEGATIVE (JR)
    --
    -- Note: min, max and sync are expressed in micro-seconds
    -->

    <!-- 
    -- Attributes of channel tag :
    -- ctl: name of the command on the transmitter - only for displaying
    -- no: order in the PPM frame
    -- function: logical command
    -- averaged: channel filtered through several frames (for discrete commands)
    -- min: minimum pulse length (micro-seconds)
    -- max: maximum pulse length (micro-seconds)
    -- neutral: neutral pulse length (micro-seconds)
    --
    -- Note: a command may be reversed by exchanging min and max values. Neutral does not need
    --       to be mid way between min and max, for example, neutral = min in the case of
    --       the throttle
    -->

Setting Up the GPS Receiver
===========================

If you are Using a GPS receiver then open u-center (tested with v5.07) and perform
the following sequence of steps.

LEA-4P
------
.. http://paparazzi.enac.fr/wiki/GPS#Manual_Configuration
.. http://diydrones.com/profiles/blogs/tutorial-programming-your
* Right Click on the NMEA Icon and choose disable child
* Choose UBX->CFG->NAV2(Navigation 2) - set it to use Airborne 4G (tells the Kalman filter to expect significant changes in direction)
* UBX->CFG->PRT - set USART1 to 38400bps (must match the value in your Airframe file)
* Change the baudrate of U-Center to 38400bps if the connection is lost at this point
* UBX->CFG->RXM(Receiver Manager) - change GPS Mode to 3 - Auto (Enabling faster bootup only if signal levels are very good)
* UBX->CFG->RATE(Rates) - change the Measurement Period to 250ms (4 Hz position updates)
* UBX->CFG->SBAS : Disable (SBAS appears to cause occasional severe altitude calcuation errors)
* UBX->NAV (not UBX->CFG->NAV): double click on POSUTM, SOL, STATUS, SVINFO, VELNED. They should change from grey to black
* UBX->CFG->CFG : save current config, click "send" in the lower left corner to permanently save these settings to the receiver 



