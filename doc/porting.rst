Porting to Python 3
===================

.. currentmodule:: sgfmill.sgf

Sgfmill is a Python 3 version of the |sgf| code from the Gomill__ project.

.. __: https://mjw.woodcraft.me.uk/gomill/


The differences are as follows:

There is a new :func:`Sgf_game.from_bytes` classmethod, which behaves like the old
:func:`!Sgf_game.from_string`.

:func:`Sgf_game.from_string` now expects a Python 3 string (which contains
Unicode characters), and forces the game's encoding to UTF-8.

:meth:`Sgf_game.serialise` now returns a bytes object.

:meth:`Tree_node.get_raw` and :meth:`Tree_node.set_raw` (and related methods)
now use bytes objects.

For Text and SimpleText properties, :meth:`Tree_node.get` and
:meth:`Tree_node.set` use Python 3 strings.


The exact rules for what 'raw' data is accepted for some property types have
changed, due to changes in the Python language features used to implement the
parser. In particular:

* CESU-8 is no longer accepted when parsing data which purports to be UTF-8.

* The raw values accepted for properties of type Real are now determined by
  Python 3's `float()`__ function rather than the platform libc (exactly what
  is accepted will depend on the Python minor version).

* The interpreter for type Number is more lenient, accepting spaces anywhere
  in the string, and 'grouping underscores' from Python 3.6 on.


.. __: https://docs.python.org/3/library/functions.html#float
