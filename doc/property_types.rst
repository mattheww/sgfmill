Property types
==============

.. currentmodule:: sgfmill.sgf

.. _basic_go_types:

Basic Go types
--------------

Sgfmill represents Go colours and moves as follows:

======== ===========================================
 Name     Possible values
======== ===========================================
*colour* single-character string: ``'b'`` or ``'w'``
*point*  pair (*int*, *int*) of coordinates
*move*   *point* or ``None`` (for a pass)
======== ===========================================

The terms *colour*, *point*, and *move* are used as above throughout this
documentation (in particular, when describing parameters and return types).

*colour* values are used to represent players, as well as stones on the board.
(When a way to represent an empty point is needed, ``None`` is used.)

*point* values are treated as (row, column). The bottom left is ``(0, 0)``
(the same orientation as |gtp|, but not |sgf|). So the coordinates for a 9x9
board are as follows::

  9 (8,0)  .  .  .  .  .  (8,8)
  8  .  .  .  .  .  .  .  .  .
  7  .  .  .  .  .  .  .  .  .
  6  .  .  .  .  .  .  .  .  .
  5  .  .  .  .  .  .  .  .  .
  4  .  .  .  .  .  .  .  .  .
  3  .  .  .  .  .  .  .  .  .
  2  .  .  .  .  .  .  .  .  .
  1 (0,0)  .  .  .  .  .  (0,8)
     A  B  C  D  E  F  G  H  J

There are functions in the :mod:`~sgfmill.common` module to convert between
these coordinates and the conventional (``T19``\ -style) notation.

Sgfmill is designed to work with square boards, up to size 26x26.


.. _sgf_property_types:

SGF property types
------------------

The following table shows how |sgf| property types are represented as Python
values (eg by the :meth:`Tree_node.get` and :meth:`Tree_node.set` methods).

=========== ========================
|sgf| type   Python representation
=========== ========================
None         ``True``
Number       int
Real         float
Double       ``1`` or ``2`` (int)
Colour       *colour*
SimpleText   string
Text         string
Stone        *point*
Point        *point*
Move         *move*
=========== ========================

Sgfmill doesn't distinguish the Point and Stone |sgf| property types. It
rejects representations of 'pass' for the Point and Stone types, but accepts
them for Move (this is not what is described in the |sgf| specification, but
it does correspond to the properties in which 'pass' makes sense).

Values of list or elist types are represented as Python lists. An empty elist
is represented as an empty Python list (in contrast, the raw value is a list
containing a single empty string).

Values of compose types are represented as Python pairs (tuples of length
two). ``FG`` values are either a pair (int, string) or ``None``.

For Text and SimpleText values, :meth:`~Tree_node.get` and
:meth:`~Tree_node.set` take care of escaping. You can store arbitrary strings
in a Text value and retrieve them unchanged, with the following exceptions:

* all linebreaks are normalised to ``\n``

* whitespace other than line breaks is converted to a single space

:meth:`~Tree_node.get` accepts compressed point lists, but
:meth:`~Tree_node.set` never produces them (some |sgf| viewers still don't
support them).

In some cases, :meth:`~Tree_node.get` will accept values which are not
strictly permitted in |sgf|, if there's a sensible way to interpret them. In
particular, empty lists are accepted for all list types (not only elists).

In some cases, :meth:`~Tree_node.set` will accept values which are not exactly
in the Python representation listed, if there's a natural way to convert them
to the |sgf| representation.

Both :meth:`~Tree_node.get` and :meth:`~Tree_node.set` check that Point values
are in range for the board size. Neither :meth:`~Tree_node.get` nor
:meth:`~Tree_node.set` pays attention to range restrictions for values of type
Number.

Examples::

   >>> node.set('KO', True)
   >>> node.get_raw('KO')
   b''
   >>> node.set('HA', 3)
   >>> node.set('KM', 5.5)
   >>> node.set('GB', 2)
   >>> node.set('PL', 'w')
   >>> node.set('RE', 'W+R')
   >>> node.set('GC', 'Example game\n[for documentation]')
   >>> node.get_raw('GC')
   b'Example game\n[for documentation\\]'
   >>> node.set('B', (2, 3))
   >>> node.get_raw('B')
   b'dg'
   >>> node.set('LB', [((6, 0), "label 1"), ((6, 1), "label 2")])
   >>> node.get_raw_list('LB')
   [b'ac:label 1', b'bc:label 2']



