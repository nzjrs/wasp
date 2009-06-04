"""
Implements the standard Ivy API.

You can refer to the example code ``pyhello.py`` for an example of use.

All methods in this module are frontends to a `ivy.IvyServer` instance, stored
in the module's attributes `_IvyServer`.

:group Connecting to/disconnecting from the Ivy bus:
  IvyInit, IvyStart,IvyMainLoop, IvyStop
:group Bindings: IvyBindMsg, IvyUnBindMsg, IvyBindDirectMsg
:group Inspecting the Ivy bus:
  IvyGetApplicationList, IvyGetApplication, IvyGetApplicationName,
  IvyGetApplicationHost
:group Interacting with other Ivy clients:
  IvySendMsg, IvySendDieMsg, IvySendDirectMsg
:group Timers: IvyTimerRepeatAfter, IvyTimerModify, IvyTimerRemove

Copyright (c) 2005 Sebastien Bigaret <sbigaret@users.sourceforge.net>
"""

_IvyServer=None

from ivy import IvyApplicationConnected, IvyApplicationDisconnected
from ivy import IvyRegexpAdded, IvyRegexpRemoved
from ivy import void_function

def IvyInit(agent_name, ready_msg=None,
            main_loop_type_ignored=0,
            on_cnx_fct=void_function,
            on_die_fct=void_function):
  """
  Initializes the module. This method should be called exactly once before any
  other method is called.
  """
  global _IvyServer
  assert _IvyServer is None
  from ivy import IvyServer
  _IvyServer = IvyServer(agent_name, ready_msg, on_cnx_fct, on_die_fct)


def IvyStart(ivybus=None):
    """
    Starts the Ivy server and fully activate the client.  Please refer to the
    discussion in `IvyMainLoop()` 's documentation.
    """
    assert _IvyServer != None
    _IvyServer.start(ivybus)


def IvyMainLoop():
    """
    Simulates the original main loop: simply waits for the server termination.

    Note that while the original API requires this to be called, this module
    does NOT rely in any way on this method. In particular, a client is
    fully functional and begins to receive messages as soon as the `IvyStart()`
    method is called.
    """
    assert _IvyServer != None
    _IvyServer.server_termination.wait()


def IvyStop():
    assert _IvyServer != None
    _IvyServer.stop()


def IvyBindMsg(on_msg_fct, regexp):
    """
    Registers a method that should be called each time a message matching
    regexps is sent on the Ivy bus.

    :return: an id identifying the binding, that can be used to unregister it
      (see `IvyUnBindMsg()`)
    """
    assert _IvyServer != None
    return _IvyServer.bind_msg(on_msg_fct, regexp)

def IvyBindDirectMsg(on_msg_fct):
    """
    Registers a method that should be called each time someone sends us
    a direct message

    """
    assert _IvyServer != None
    return _IvyServer.bind_direct_msg(on_msg_fct)

def IvyUnBindMsg(id):
    """
    Unregisters a binding

    :param id: the binding's id, as previously returned by `IvyBindMsg()`.
    :return: the regexp corresponding to the unsubscribed binding
    :except KeyError: if no such subscription can be found
    """
    assert _IvyServer != None
    return _IvyServer.unbind_msg(id)

def IvyBindRegexpChange(regexp_change_callback):
  """
  """
  assert _IvyServer != None
  return _IvyServer.bind_regexp_change(regexp_change_callback)

def IvySendMsg(msg):
    """
    Sends a message on the bus
    """
    assert _IvyServer != None
    return _IvyServer.send_msg(msg)

def IvySendDieMsg(client):
    """
    Sends a "die" message to `client`, instructing him to terminate.

    :param client: an `ivy.IvyClient` object,  as returned by
      `IvyGetApplication()`
    """
    assert _IvyServer != None
    client.send_die_message()


def IvySendDirectMsg(client, num_id, msg):
    """
    Sends a message directly to an other Ivy client, with the supplied
    numerical id and message.
    
    :Parameters:
      - `client`: an `ivy.IvyClient` object, as returned by
        `IvyGetApplication()`
      - `num_id`: an additional integer to use. It may, or may not, be
        meaningful, this only depends on the usage your application makes of
        it, the Ivy protocol itself does not care and simply transmits it
        along with the message.
      - `msg`: the message to send
    """
    assert _IvyServer != None
    client.send_direct_message(num_id, msg)


def IvySendError(client, num_id, error_msg):
    """
    Sends an "error" message to `client`

    :Parameters:
      - `client`: an `ivy.IvyClient` object, as returned by
        `IvyGetApplication()`
      - `num_id`: an additional integer to use. It may, or may not, be
        meaningful, this only depends on the usage your application makes of
        it, the Ivy protocol itself does not care and simply transmits it
        along with the message.
      - `error_msg`: the message to send
    """
    assert _IvyServer != None
    client.send_error(num_id, error_msg)


def IvyGetApplicationList():
    """
    Returns the names of the applications that are currently connected
    """
    assert _IvyServer != None
    return _IvyServer.get_clients()

def IvyGetApplicationMessages(client):
    """
    Returns all subscriptions for that client

    :param client: an `ivy.IvyClient` object,  as returned by
      `IvyGetApplication()`
    :return: list of tuples (idx, regexp)
    """
    return client.get_regexps()

def IvyGetApplication(name):
    """
    Returns the Ivy client registered on the bus under the given name.
    
    .. WARNING:: if multiple applications are registered w/ the same name only
      one is returned
    
    :returns: an `ivy.IvyClient` object
    """
    assert _IvyServer != None
    clients = _IvyServer.get_client_with_name(name)
    return clients and clients[0] or None

def IvyGetApplicationName(client):
    """
    Equivalent to ``client.agent_name``

    :param client: an `ivy.IvyClient` object, as returned by
      `IvyGetApplication()`
    """
    return client.agent_name

def IvyGetApplicationHost(client):
    """
    Equivalent to ``client.fqdn``. IP address is stored under ``client.ip``,
    and port number under ``client.port``

    :param client: an `ivy.IvyClient` object,  as returned by
      `IvyGetApplication()`
    """
    return client.fqdn
  

_timers={}
def IvyTimerRepeatAfter(count, delay, callback):
    """
    Creates and activates a new timer
    
    :Parameters:
      - `count`: nb of time to repeat the loop, ``0`` (zero) for an endless loop
      - `delay`: the delay between ticks, in milliseconds
      - `callback`: the function to call on every tick. That function is
        called without any parameters.

    :return: the timer's id
    """
    assert _IvyServer != None
    from ivy import IvyTimer
    # The original python API relies on a callback called without any parameter
    cb = lambda timer, callback=callback: callback()
    timer = IvyTimer(_IvyServer, count, delay, cb)
    _timers[timer.id]=timer
    timer.start()
    return timer.id


def IvyTimerModify(timer_id, delay):
    """
    Modifies a timer's delay.  Note that the modification will happen after
    the next tick.
    
    :Parameters:
      - `timer_id`: id of the timer to modify, as returned by
        `IvyTimerRepeatAfter()`
      - `delay`: the delay, in milliseconds, between ticks
    """
    _timers[timer_id].delay = delay


def IvyTimerRemove(timer_id):
    """
    Stops and removes a given timer.
    
    :param timer_id: id of the timer, as returned by `IvyTimerRepeatAfter`
    """
    from ivy import IvyTimer
    timer = _timers[timer_id]
    timer.abort = True
    del _timers[timer_id]



#TODO  IvyUnBindMsg(id)


"""
# copy/paste for quick tests w/ ivyprobe
from ivy.std_api import *
IvyInit('Test', 'test welcome', 0) 
IvyStart()
def onmsgproc(*larg):
   print larg

IvyBindMsg(onmsgproc, '(.*)')
IvyGetApplicationList()
app=IvyGetApplication('IVYPROBE')
IvyGetApplicationName(app)
IvyGetApplicationHost(app)
IvySendDirectMsg(app, 765, 'glop')
IvySendDieMsg(app)
"""
