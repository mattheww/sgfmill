Installation
============

.. contents:: Page contents
   :local:
   :backlinks: none


Requirements
------------

Sgfmill requires Python 3.2 or later. There are no other requirements.

This is a Python 3 version of the |sgf| code from the Python 2 Gomill__ project.
If you need Python 2 support, please use Gomill instead.

.. __: https://mjw.woodcraft.me.uk/gomill/


Installing
----------

Sgfmill can be installed from the Python Package Index::

    pip3 install sgfmill

To remove an installed version of Sgfmill, run ::

    pip3 uninstall sgfmill


Downloading sources and documentation
-------------------------------------

The source distribution can be downloaded from the `Python Package index`__,
or from http://mjw.woodcraft.me.uk/sgfmill/, as a file named
:file:`sgfmill-{version}.tar.gz`.

.. __: https://pypi.python.org/pypi/sgfmill

This documentation is distributed separately in html form at
http://mjw.woodcraft.me.uk/sgfmill/ as :file:`sgfmill-doc-{version}.tar.gz`.

The version-control history is available at
https://github.com/mattheww/sgfmill.

To install from the source distribution::

  python3 setup.py bdist_wheel
  pip3 install --user dist/sgfmill-*.whl


Running the test suite
----------------------

The testsuite is available from the source distribution or a version-control
checkout.

To run the testsuite against the distributed :mod:`!sgfmill` package, change to
the distribution directory and run ::

  ./run_sgfmill_testsuite


To run the testsuite against an installed :mod:`!sgfmill` package, change to
the distribution directory and run ::

  python test_installed_sgfmill.py


.. _running the example scripts:

Running the example scripts
---------------------------

The example scripts are included in the source distribution. To run them, it
is simplest to install the :mod:`!sgfmill` package first.

If you do not wish to do so, you can run ::

  export PYTHONPATH=<path to the distribution directory>

so that the example scripts will be able to find the :mod:`!sgfmill` package.



Building the documentation
--------------------------

The sources for this HTML documentation are included in the Sgfmill source
distribution. To build the documentation, change to the distribution directory
and run ::

   ./build_docs

The documentation will be generated in :file:`doc/_build/html`.

Requirements:

- Sphinx__ version 1.0 or later (tested with 1.2)

.. __: http://sphinx.pocoo.org/

