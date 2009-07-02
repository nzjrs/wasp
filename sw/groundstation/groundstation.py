#!/usr/bin/env python2.5
import os.path
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(name)-20s][%(levelname)-7s] %(message)s (%(filename)s:%(lineno)d)"
    )

import gs.groundstation as groundstation

if __name__ == "__main__":
    confdir = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.environ['HOME'], ".config", "ppz"))
    if not os.path.exists(confdir):
        os.makedirs(confdir)
    prefs = os.path.join(confdir, "groundstation.ini")

    gs = groundstation.Groundstation(prefs)
    gs.main()
