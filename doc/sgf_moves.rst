The :mod:`!sgf_moves` module
----------------------------

.. module:: sgfmill.sgf_moves
   :synopsis: Higher-level processing of moves and positions from SGF games.

The :mod:`!sgfmill.sgf_moves` module contains some higher-level functions for
processing moves and game positions.

(They are the sort of thing you might need to implement 'load SGF' and 'save
as SGF' features in a Go-playing program.)


.. function:: get_setup_and_moves(sgf_game[, board])

   :rtype: tuple (:class:`.Board`, list of tuples (*colour*, *move*))

   Returns the initial setup and the following moves from an
   :class:`.Sgf_game`.

   The board represents the position described by ``AB`` and/or ``AW``
   properties in the |sgf| game's root node. :exc:`ValueError` is raised if
   this position isn't legal.

   The moves are from the game's leftmost variation. Doesn't check that the
   moves are legal.

   Raises :exc:`ValueError` if the game has structure it doesn't support.

   Currently doesn't support ``AB``/``AW``/``AE`` properties after the root
   node.

   If the optional *board* parameter is provided, it must be an empty
   :class:`.Board` of the right size; the same object will be returned. This
   option is provided so you can use a different Board class (see
   :class:`.Interface_for_get_setup_and_moves` for what it needs to implement).

   See also the :script:`show_sgf.py` example script.


.. function:: set_initial_position(sgf_game, board)

   Adds ``AB``/``AW``/``AE`` properties to an :class:`.Sgf_game`'s root node,
   to reflect the position from a :class:`.Board`.

   Replaces any existing ``AB``/``AW``/``AE`` properties in the root node.

   If you wish to use your own board class, see
   :class:`.Interface_for_set_initial_position` for what it needs to
   implement.


.. function:: indicate_first_player(sgf_game)

   Adds a ``PL`` property to an :class:`.Sgf_game`'s root node if appropriate,
   to indicate which colour is first to play.

   Looks at the first child of the root to see who the first player is, and
   sets ``PL`` it isn't the expected player (Black normally, but White if
   there is a handicap), or if there are non-handicap setup stones.

