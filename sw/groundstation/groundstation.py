#!/usr/bin/env python2.5
import os.path
import logging
import optparse

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(name)-20s][%(levelname)-7s] %(message)s (%(filename)s:%(lineno)d)"
    )

import gs.groundstation as groundstation

if __name__ == "__main__":
    thisdir = os.path.abspath(os.path.dirname(__file__))
    default_messages = os.path.join(thisdir, "..", "messages.xml")

    confdir = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.environ['HOME'], ".config", "ppz"))
    if not os.path.exists(confdir):
        os.makedirs(confdir)
    prefs = os.path.join(confdir, "groundstation.ini")

    parser = optparse.OptionParser()
    parser.add_option("-m", "--messages",
                    default=default_messages,
                    help="messages xml file", metavar="FILE")
    parser.add_option("-p", "--preferences",
                    default=prefs,
                    help="user preferences file", metavar="FILE")

    options, args = parser.parse_args()

    if not os.path.exists(options.messages):
        parser.error("could not find messages.xml")

    gs = groundstation.Groundstation(
            options.preferences,
            options.messages
    )
    gs.main()
