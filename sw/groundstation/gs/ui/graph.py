import random
import os.path
import sys
import logging
import gtk

import gs.ui.rtgraph as rtgraph

LOG = logging.getLogger("graph")

class FieldChannel(rtgraph.Channel):
    def __init__(self, msg, field):
        rtgraph.Channel.__init__(self)

        i = 0
        for f in msg.fields:
            if f.name == field.name:
                self._fidx = i
            i += 1

        self._val = 0

    def getValue(self):
        return self._val

    def update_msg_value(self, vals):
        self._val = vals[self._fidx]

class RandomChannel(FieldChannel):
    def getValue(self):
        return random.random()
       
class Graph(rtgraph.HScrollLineGraph):
    def __init__(self, source, msg, field, ymin=0.0, ymax=1.0, width=150, height=50, rate=30):
        rtgraph.HScrollLineGraph.__init__(self, 
                    scrollRate=rate,
                    size=(width,height),
                    range=(ymin,ymax),
                    autoScale=True,
                    axisLabel=True,
                    channels=[FieldChannel(msg, field)]
        )
        self._source = source
        self._source.register_interest(self._on_msg, 0, msg.name)

    def _on_msg(self, msg, payload):
        vals = msg.unpack_values(payload)
        for f in self.channels:
            f.update_msg_value(vals)

    def get_scroll_rate_widget(self):
        return self.getTweakControls()[0]

    def delete(self):
        self._source.unregister_interest(self._on_msg)

