from setuptools import setup

import sgfmill

SGFMILL_URL = "https://mjw.woodcraft.me.uk/sgfmill/"
VERSION = sgfmill.__version__

LONG_DESCRIPTION = """\
Sgfmill is a Python library for reading and writing Go game records
using Smart Game Format (SGF).

It supports:

* loading SGF game records to make a Python object representation
* creating SGF game objects from scratch
* setting properties and manipulating the tree structure
* serialising game records to SGF data
* applying setup stones and moves to a Go board position

Download: %(SGFMILL_URL)sdownload/sgfmill-%(VERSION)s.tar.gz

Documentation: %(SGFMILL_URL)sdownload/sgfmill-doc-%(VERSION)s.tar.gz

Online Documentation: %(SGFMILL_URL)sdoc/%(VERSION)s/

Changelog: %(SGFMILL_URL)sdoc/%(VERSION)s/changes.html

Github: https://github.com/mattheww/sgfmill

""" % vars()

setup(name='sgfmill',
      version=VERSION,
      url=SGFMILL_URL,
      description=\
        "Library for reading and writing files using Smart Game Format (SGF).",
      long_description=LONG_DESCRIPTION,
      author="Matthew Woodcraft",
      author_email="matthew@woodcraft.me.uk",
      packages=['sgfmill'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python",
          "Topic :: Games/Entertainment :: Board Games",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords="go,baduk,weiqi,sgf",
      license="MIT",
)

