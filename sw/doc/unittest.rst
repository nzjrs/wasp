Unit Testing
************

Unit testing is run through the "test" architecture.  At present this is
a host-based (x86) architecture and is essentially the "null" architecture
with the additional test-related makefile targets.

It might be possible to write an "embedded" testsuite, but we aren't
there yet.

This current code uses the `GLib-2.0
<http://library.gnome.org/devel/glib/stable/glib-Testing.html>`_ unit
testing framework. [#f1]_

Running the unit tests
----------------------

::

  make test

builds the test suite binaries for the local architecture,
then run them.  The test programs are run by `gtester
<http://library.gnome.org/devel/glib/stable/gtester.html>`_ , GLib's
test runner.  

::

  make testprogs

builds the test binaries but not execute them.  The resulting binaries
appear in ``sw/onboard/bin/test/``

Developing unit tests
---------------------

The overall test system consists of a number of test suites (binaries), each of
which run a sequence of test cases (functions), each of which contain
a number of tests (assertions).  The division into binaries and suites
is somewhat arbitrary and strictly for organization.

The test binaries are given by the variable ``TEST_PROGS`` in ``arch/Makefile.test`` 

::

  TEST_PROGS = test_math test_string

For each test binary, a Makefile variables lists the source files that contain the actual tests:

::

  test_math_TESTSRCS = math/tests/*_tc.c

These source files are scanned for test functions (see :ref:`how-it-works`). This
variable goes through wildcard expansion.

Additional source files which should be linked to the test binary are
given by a second variable:

::
  
  test_math_SRCS = autopilot.c

These files **are not** scanned for test functions and are not wildcard-expanded.


Writing unit tests
~~~~~~~~~~~~~~~~~~


A simple test is defined by a function whose name ends in `_tc` (testcase)

::

   void math_test_sum_tc( void )

The GLib unit testing system organizes tests into a hierarchy (why?).
The test suite generation scripts convert the function name into a name in the
hierarchy by breaking the name up at underscores.  So `math_test_sum_tc`
is the test case `/math/test/sum` to GLib.  Similarly there might be a
`/math/test/difference` etc.

The test consists of code and unit testing assertions (listed `in the GLib documentation <http://library.gnome.org/devel/glib/stable/glib-Testing.html>`_ )

::

  void math_test_sum_tc( void )
  {
     int a = 1;
     int b = 2;
     int c = a+b;

     g_assert_cmpint( a, 1 );
     g_assert_cmpint( b, 2 );
     g_assert_cmpint( c, 3 );
  }
	

In this case the assertions test that the sum has succeeded (c = a+b)
and that neither a nor b have been changed. [#f2]_

GLib also supports test cases with setup and teardown functions.  These functions can be shared between a number of
test cases ensuring the same variables are available for each test.  These test cases are specified as follows:

::

  void math_test_mult_tc( a_math_fixture *fix, gconstpointer test_data )

Where the "fixture" is a pointer to data which has also been passed to the
setup function, then the test case, then the teardown function.  All three
of these function must be defined.  The setup function must have the name
``{fixture name}_setup`` and the teardown ``{fixture name}_teardown``.
The name of the fixture type isn't a magic value.

:: 

  typedef struct { 
     int a,b; 
  } a_math_fixture;

  void a_math_fixture_setup( a_math_fixture *fix, gconstpointer test_data )
  {
     fix->a = 1;
     fix->b = 2;
  }

  void math_test_mult_tc( a_math_fixture *fix, gconstpointer test_data )
  {
    int c = fix->a * fix->b;
    g_assert_cmpint( c, 2 );
  }

  void math_test_div_tc( a_math_fixture *fix, gconstpointer test_data )
  {
    int c = fix->b / fix->a;
    g_assert_cmpint( c, 2 );
  }


  void a_math_fixture_teardown( a_math_fixture *fix, gconstpointer test_data )
  {
    ;
  }


In this case, the two test cases 'mult' and 'div' share the same setup and teardown functions.


.. _how-it-works:

How it works
~~~~~~~~~~~~

Each test source file is run through the script `tools/gen-testsuite.py`
which generates a temporary copy of the file in `bin/test/`.  It scans
the file for test cases (functions ending in _tc) and notes whether they are
standalone or with a fixture.  
It appends a function to the temporary copy which registers all of the test cases with GLib
(calls `g_test_add` for each test case).

The test program itself is then generated using `tools/gen-testmain.py`
which scans the temporary files for the registration functions, and
generates a temporary source file `bin/test/{test_name}.c` which calls
each registration function and runs the tests.

`arch/Makefile-targets.test` takes care of the
autogeneration, and compilation of all of the resulting files.


.. rubric:: Footnotes 

.. [#f1]  I'm a bit surprised there
          isn't a "canonical" C unit testing framework ... even the
          popular options are a bit hard to find.  I chose GLib
          because it was implicitly supported by being included
          in the GLib.  The next-best alternative would be `CUnit
          <http://cunit.sourceforge.net/>`_

.. [#f2]  Obviously this isn't a very sophisticated test, nor is it complete,
	  and it will break horribly when the constants are changed....  In 
          other words, don't copy it.
