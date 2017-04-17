Introduction
============

Sgfmill is a Python library for reading and writing Go game records using
Smart Game Format (:term:`SGF`).

It supports:

* loading |sgf| game records to make a Python object representation
* creating |sgf| game objects from scratch
* setting properties and manipulating the tree structure
* serialising game records to |sgf| data
* applying setup stones and moves to a Go board position

It is intended for use with |SGF| version FF[4], which is specified at
http://www.red-bean.com/sgf/index.html.

It has support for the game-specific properties for Go, but not those of other
games.

Point, Move and Stone values are interpreted as Go points.


Python language support
-----------------------

Sgfmill supports Python 3 only.

It is a Python 3 version of the |sgf| code from the Python 2 Gomill__ project.
If you need Python 2 support, please use Gomill instead.

.. __: https://mjw.woodcraft.me.uk/gomill/

