The :mod:`~sgfmill.common` module
---------------------------------

.. module:: sgfmill.common
   :synopsis: Go-related utility functions.

The :mod:`!sgfmill.common` module provides a few Go-related utility functions,
mostly used only by :mod:`sgfmill.ascii_boards`.

It is designed to be safe to use as ``from common import *``.

The vertex functions suppose square boards up to size 25x25, which is the
upper limit of the notation they use (and also the upper limit for |gtp|).

.. function:: opponent_of(colour)

   :rtype: *colour*

   Returns the other colour::

     >>> opponent_of('b')
     'w'

.. function:: colour_name(colour)

   :rtype: string

   Returns the (lower-case) full name of a *colour*::

     >>> colour_name('b')
     'black'

.. function:: format_vertex(move)

   :rtype: string

   Returns a string describing a *move* in conventional notation::

     >>> format_vertex((3, 0))
     'A4'
     >>> format_vertex(None)
     'pass'

   The result is suitable for use directly in |GTP| responses. Note that ``I``
   is omitted from the letters used to indicate columns, so the maximum
   supported column value is ``25``.

.. function:: format_vertex_list(moves)

   :rtype: string

   Returns a string describing a sequence of *moves*::

     >>> format_vertex_list([(0, 1), (2, 3), None])
     'B1,D3,pass'
     >>> format_vertex_list([])
     ''

.. function:: move_from_vertex(vertex, board_size)

   :rtype: *move*

   Interprets the string *vertex* as conventional notation, assuming a square
   board whose side is *board_size*::

     >>> move_from_vertex("A4", 9)
     (3, 0)
     >>> move_from_vertex("a4", 9)
     (3, 0)
     >>> move_from_vertex("pass", 9)
     None

   Raises :exc:`ValueError` if it can't parse the string, or if the resulting
   point would be off the board.

   Treats *vertex* case-insensitively.

