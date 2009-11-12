#!/usr/bin/env python
import sys
import os.path
import logging
import optparse

sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(name)-20s][%(levelname)-7s] %(message)s (%(filename)s:%(lineno)d)"
    )

import gs.groundstation as groundstation
import wasp.communication as communication

if __name__ == "__main__":
    thisdir = os.path.abspath(os.path.dirname(__file__))
    default_messages = os.path.join(thisdir, "..", "onboard", "config", "messages.xml")
    default_settings = os.path.join(thisdir, "..", "onboard", "config", "settings.xml")

    confdir = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.environ.get("HOME","."), ".config", "wasp"))
    if not os.path.exists(confdir):
        os.makedirs(confdir)
    prefs = os.path.join(confdir, "groundstation.ini")

    parser = optparse.OptionParser()
    communication.setup_optparse_options(parser, default_messages)
    parser.add_option("-e", "--settings",
                    default=default_settings,
                    help="Settings xml file", metavar="FILE")
    parser.add_option("-P", "--preferences",
                    default=prefs,
                    help="User preferences file", metavar="FILE")
    parser.add_option("-t", "--use-test-source",
                    action="store_true", default=False,
                    help="Use a test source, same as --source-name=test")

    options, args = parser.parse_args()

    if not os.path.exists(options.messages):
        parser.error("could not find messages.xml")

    source_opts = {}
    if options.use_test_source:
        source_name = "test"
    else:
        source_name = options.source_name

    gs = groundstation.Groundstation(
            os.path.abspath(options.preferences),
            os.path.abspath(options.messages),
            os.path.abspath(options.settings),
            source_name,
            **source_opts
    )
    gs.main()
