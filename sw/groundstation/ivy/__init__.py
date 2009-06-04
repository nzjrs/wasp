"""
Ivy is a lightweight software bus for quick-prototyping protocols. It
allows applications to broadcast information through text messages, with a
subscription mechanism based on regular expressions.

If you're used to the standard Ivy API, you probably want to look at the
`std_api` module.

.. attention:: Version 2.0 broke backward compatibility.  If you are upgrading
  from ivy-python v1.x, be sure to read the `v2.0 compatibility notes`_,
  below.

Introduction
------------

The Ivy software bus was designed at the French Centre d'Etudes de la
Navigation Aerienne (CENA).  The original work: sofware, documentation,
papers, credits can be found on the `Ivy Home Page`_; it contains all the
necessary materials needed to understand Ivy.

This package is the Python library; Ivy librairies are also available for
numerous languages, among wich: C, C#, C++, Java, Perl --see the `Ivy Download
Page <http://www.tls.cena.fr/products/ivy/download/index.html>`_ for details.

This python library is a full rewrite of the original software, and it is
written in pure python.  Note that another python implementation is available
at the `Ivy downloads page`_, which is built by `SWIG <http://www.swig.org/>`_
on top of the Ivy C library.



Understanding the package
-------------------------

This Ivy package is made of two modules: `ivy` and `std_api`.

In order to understand the way it works, we highly suggest that you read the
materials available from the `Ivy Home Page`_.  Within the documentation of
this python package we suppose that you are already familiar with the way an
ivy bus works, and with how the corresponding framework is organized.

`ivy.std_api`
~~~~~~~~~~~~~
Once familiar with the ivy framework, you'll find in the `std_api` module the
exact API you're expecting (see for example the  `The Ivy C library`_).

An example of use, directly taken from the original swig-base python release,
is included with the package, see ``examples/pyhello.py``.

.. important:: One big difference with the original implementation is that
   there is nothing like a "main loop": the server is activated as soon as the
   method `ivy.std_api.IvyStart` is called, and the `ivy.std_api.IvyMainLoop` method simply
   waits for the server to terminate (the server is in fact 

`ivy.ivy`
~~~~~~~~~

It's where the "magic" goes: the module `std_api` is built on top of it.

You'll be interested in using this package if for example, you want to manage
more than one ivy-bus in an application.  We won't give here much hint on how
to use it, since the code of the `ivy` odule itself serves as a perfect
example of use!

Logging
-------

  The module issues messages through python's standard ``logging`` module:
  
    - logger's name: ``'Ivy'``
    - default level: ``logging.INFO``
    - default handler: a ``logging.StreamHandler`` logging messages to the
      standard error stream.

  For example, if you need to see all messages issued by the package, including
  debug messages, use the following code excerpt:

  .. python::
    import logging
    logging.getLogger('Ivy').setLevel(logging.DEBUG)

  Further details can be found in the `Python standard documentation
  <http://docs.python.org/lib/module-logging.html>`_.

v2.0 compatibility notes
------------------------

Version 2.0 broke the backward compatibility with former versions 1.x: every
callback methods now receives an `ivy.IvyClient` object as its first
parameter.

This makes it possible for the receiving code to know which agent on the bus
sends the corresponding event. Unfortunately, this breaks backward
compatibility and callback methods must be adapted to the new scheme.

For example, suppose you're binding a regexp to the callback ``on_msg``:

.. python::
  IvyBindMsg(onhello, "^hello=([^ ]*) from=([^ ]*)")

In ivy-python 1.x, you used to declare the callback as follows

.. python::
      def onhello(*arg):
          print "Got hello message: %s from: %s"% (arg[0], arg[1])

or:
  
.. python::
      def onhello(message, from):
          print "Got hello message: %s from: %s"% (message, from)


In version 2.0, your callbacks also get the agent triggering the event as the
1st parameter; the previous callbacks should be rewritten this way:

.. python::
      def onhello(*arg):
          print "Got hello message: %s from: %s (coming from ivy agent: %r)"% (arg[1], arg[2], arg[0])

or:

.. python::
      def onhello(agent, message, from):
          print "Got hello message: %s from: %s (coming from ivy agent: %r)"% (message, from, agent)


Misc. notes
-----------

  - direct msg: to app_name == the last one registered w/ that name (for
    example register ivyprobe 3 times and send a direct msg to IVYPROBE from
    one of them)

  - regexps order and ids: ivyprobe e.g. subscribes regexp in reverse order of
    ids.  If two matches -> which one should we choose? Not explicitely
    documented.


License
-------

This software is distributed under the `"new" BSD license
<http://www.opensource.org/licenses/bsd-license.php>`_,

(please refer the file ``LICENSE`` for full legal details)

Copyright (c) 2005-2008 Sebastien Bigaret <sbigaret@users.sourceforge.net>

.. _Ivy Home Page: http://www.tls.cena.fr/products/ivy/
.. _The Ivy C library: http://www.tls.cena.fr/products/ivy/documentation/ivy-c.pdf
.. _Ivy downloads page: http://www.tls.cena.fr/products/ivy/download/binaries.html
"""
__version__='2.1'
