def setup_comm_optparse_options(parser, default_messages="/dev/null"):
    """
    Adds a number of communication related command line options to an
    optparse parser instance. These options are
    "-m", "--messages" : messages xml file
    "-p", "--port"     : serial port
    "-s", "--speed"    : serial port baud rate
    "-t", "--timeout"  : serial timeout
    """
    parser.add_option("-m", "--messages",
                    default=default_messages,
                    help="messages xml file", metavar="FILE")
    parser.add_option("-p", "--port",
                    default="/dev/ttyUSB0",
                    help="serial port")
    parser.add_option("-s", "--speed",
                    type="int", default=57600,
                    help="serial port baud rate")
    parser.add_option("-t", "--timeout",
                    type="int", default=1,
                    help="serial timeout")
