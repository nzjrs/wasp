import os.path
import time
import gtk
import unittest

import ppz.ui.treeview as treeview
import ppz.ui.senders as senders

#common constants to test against
from testcommon import *

# Stolen from Kiwi
def refresh_gui(delay=0):
	while gtk.events_pending():
		gtk.main_iteration_do(block=False)
	time.sleep(delay)

class TreeviewTest(unittest.TestCase):
    def setUp(self):
        self.mf = get_mf()

    def testConstruct(self):
        ts = treeview.MessageTreeStore()
        for m in self.mf.get_messages():
            ts.add_message(m)
        tv = treeview.MessageTreeView(ts)

        refresh_gui()

class RequestMessageSenderTest(unittest.TestCase):
    def setUp(self):
        self.mf = get_mf()

    def testConstruct(self):
        rm = senders.RequestMessageSender(self.mf)

        refresh_gui()

class SimpleMessageSenderTest(unittest.TestCase):
    def setUp(self):
        self.mf = get_mf()

    def testConstruct(self):
        sm = senders.SimpleMessageSender(self.mf)

        refresh_gui()



if __name__ == "__main__":
    unittest.main()

