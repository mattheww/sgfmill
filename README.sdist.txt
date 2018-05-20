Sgfmill
=======

Sgfmill is a Python library for reading and writing Go game records using
Smart Game Format (SGF).

Sgfmill's home page is http://mjw.woodcraft.me.uk/sgfmill/

There is also a Github repository at https://github.com/mattheww/sgfmill


Requirements
------------

Sgfmill requires Python 3.2 or later. There are no other requirements.

This is a Python 3 version of the SGF code from the Python 2 Gomill project
<http://mjw.woodcraft.me.uk/sgfmill/>. If you need Python 2 support, please
use Gomill instead.


Installation
------------

Installing Sgfmill puts the sgfmill package onto the Python module search path.

To install from the source distribution:

  python3 setup.py bdist_wheel
  pip3 install --user dist/sgfmill-*.whl

To uninstall:

  pip3 uninstall sgfmill


Running the test suite
----------------------

To run the testsuite against the distributed sgfmill package, change to
the distribution directory and run

  ./run_sgfmill_testsuite


To run the testsuite against an installed sgfmill package, change to the
distribution directory and run

  python3 test_installed_sgfmill.py


Running the example scripts
---------------------------

To run the example scripts, it is simplest to install the sgfmill package
first.

If you do not wish to do so, you can run

  export PYTHONPATH=<path to the distribution directory>

so that the example scripts will be able to find the sgfmill package.


Building the documentation
--------------------------

To build the documentation, change to the distribution directory and run

   ./build_docs

The documentation will be generated in doc/_build/html.

Requirements:

   Sphinx [1] version 1.0 or later (tested with 1.4)

[1] http://sphinx.pocoo.org/


Licence
-------

Sgfmill is copyright 2009-2018 Matthew Woodcraft and the sgfmill contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Contributors
------------

See the 'Licence' page in the HTML documentation (doc/licence.rst).


Contact
-------

Please send any bug reports, suggestions, patches, questions &c to

Matthew Woodcraft
matthew@woodcraft.me.uk


Changelog
---------

See the 'Changes' page in the HTML documentation (doc/changes.rst).

                                                                mjw 2018-05-20
