The :mod:`sgfmill` package
==========================

All Sgfmill code is contained in modules under the :mod:`!sgfmill` package.

The package module itself defines only a single constant:

.. module:: sgfmill
   :synopsis: Tools for testing and tuning Go-playing programs.

.. data:: __version__

   The library version, as a string (like ``"1.0"``).


.. toctree::
   :hidden:
   :maxdepth: 3
   :titlesonly:

   sgf
   sgf_moves
   sgf_board_interface
   boards
   ascii_boards
   common


Modules
-------

The package includes the following modules:

.. the descriptions here should normally match the module :synopsis:, and
   therefore the module index.

========================================= ========================================================================
 |sgf|-specific
========================================= ========================================================================
:mod:`~sgfmill.sgf`                        High level |sgf| interface.
:mod:`~sgfmill.sgf_moves`                  Higher-level processing of moves and positions from |sgf| games.
:mod:`~sgfmill.sgf_board_interface`        Go-board interface required by :mod:`!sgf_moves`.
:mod:`~!sgfmill.sgf_grammar`               The |sgf| parser.
:mod:`~!sgfmill.sgf_properties`            Interpreting |sgf| property values.
========================================= ========================================================================

========================================= ========================================================================
 Go-related support code
========================================= ========================================================================
:mod:`~sgfmill.boards`                     Go board representation.
:mod:`~sgfmill.ascii_boards`               ASCII Go board diagrams.
:mod:`~sgfmill.common`                     Go-related utility functions.
========================================= ========================================================================

The main public interface is in the :mod:`~sgfmill.sgf` module.

The :mod:`~sgfmill.sgf_moves` module contains some higher-level functions for
processing moves and positions.

The :mod:`~sgfmill.sgf_board_interface` module defines an abstract board
interface required by functions in :mod:`!sgf_moves` (and implemented by
:class:`boards.Board`).

The :mod:`!sgf_grammar` and :mod:`!sgf_properties` modules are
used to implement the :mod:`!sgf` module, and are not currently documented.

The :mod:`~sgfmill.boards` module provides a Go board representation, used by
:mod:`!sgf_moves`.

The :mod:`~sgfmill.ascii_boards` module supports ASCII board diagrams, used by some
example scripts and the testsuite.

The :mod:`~sgfmill.common` module provides a few Go-related utility functions,
mostly used only by :mod:`~sgfmill.ascii_boards`.

