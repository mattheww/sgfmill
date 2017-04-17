:class:`!Sgf_game` objects
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: sgfmill.sgf

|sgf| data is represented using :class:`!Sgf_game` objects. Each object
represents the data for a single |sgf| file (corresponding to a ``GameTree``
in the |sgf| spec). This is typically used to represent a single game,
possibly with variations (but it could be something else, such as a problem
set).

.. contents:: Page contents
   :local:
   :backlinks: none


Creating :class:`!Sgf_game`\ s
""""""""""""""""""""""""""""""

An :class:`!Sgf_game` can either be created from scratch or loaded from a
string.

To create one from scratch, instantiate an :class:`!Sgf_game` object directly:

.. class:: Sgf_game(size[, encoding="UTF-8"])

   *size* is an integer from 1 to 26, indicating the board size.

   The optional *encoding* parameter specifies the :ref:`raw property encoding
   <raw_property_encoding>` to use for the game.

When a game is created this way, the following root properties are initially
set: :samp:`FF[4]`, :samp:`GM[1]`, :samp:`SZ[{size}]`, and
:samp:`CA[{encoding}]`.

To create a game from existing |sgf| data, use the
:func:`!Sgf_game.from_bytes` or :func:`!Sgf_game.from_string` classmethod:

.. classmethod:: Sgf_game.from_bytes(bb[, override_encoding=None])

   :rtype: :class:`!Sgf_game`

   Creates an :class:`!Sgf_game` from the |sgf| data in *bb*, which must be
   a bytes-like object.

   Raises :exc:`ValueError` if it can't parse the data, or if the ``SZ`` or
   ``CA`` properties are unacceptable. No error is reported for other
   malformed property values. See also :doc:`parsing`.

   Assumes the data is in the encoding described by the ``CA`` property in the
   root node (defaulting to ``"ISO-8859-1"``), and uses that as the :ref:`raw
   property encoding <raw_property_encoding>`.

   But if *override_encoding* is present, assumes the data is in that encoding
   (no matter what the ``CA`` property says), and sets the ``CA`` property and
   raw property encoding to match.

   The board size is taken from the ``SZ`` propery in the root node
   (defaulting to ``19``). Board sizes greater than ``26`` are rejected.


   Example::

     g = sgf.Sgf_game.from_bytes(
         b"(;FF[4]GM[1]SZ[9]CA[UTF-8];B[ee];W[ge])",
         override_encoding="iso8859-1")


.. classmethod:: Sgf_game.from_string(s)

   :rtype: :class:`!Sgf_game`

   Creates an :class:`!Sgf_game` from the |sgf| data in *s*, which must be a
   string.

   Raises :exc:`ValueError` if it can't parse the data, or if the ``SZ`` or
   ``CA`` properties are unacceptable. No error is reported for other
   malformed property values. See also :doc:`parsing`.

   The game's :ref:`raw property encoding <raw_property_encoding>` and ``CA``
   property will be ``"UTF-8"`` (replacing any ``CA`` property present in the
   string).

   The board size is taken from the ``SZ`` propery in the root node
   (defaulting to ``19``). Board sizes greater than ``26`` are rejected.

   Example::

     g = sgf.Sgf_game.from_string(
         "(;FF[4]GM[1]SZ[9]CA[UTF-8];B[ee];W[ge])")


Serialising :class:`!Sgf_game`\ s
"""""""""""""""""""""""""""""""""

To retrieve the |sgf| data as bytes, use the :meth:`!serialise` method:

.. method:: Sgf_game.serialise([wrap])

   :rtype: bytes

   Produces the |sgf| representation of the data in the :class:`!Sgf_game`.

   Returns a bytes object, in the encoding specified by the ``CA`` root
   property (defaulting to ``"ISO-8859-1"``).

   See :ref:`changing_ca` for details of the behaviour if the ``CA`` property
   is changed from its initial value.

   :meth:`!serialise` makes some effort to keep the output line length to no
   more than 79 bytes. Pass ``None`` in the *wrap* parameter to disable this
   behaviour, or pass an integer to specify a different limit.


Accessing the game's nodes
""""""""""""""""""""""""""

The complete game tree is represented using :class:`Tree_node` objects, which
are used to access the |sgf| properties. An :class:`!Sgf_game` always has at
least one node, the :dfn:`root node`.

.. method:: Sgf_game.get_root()

   :rtype: :class:`Tree_node`

   Returns the root node of the game tree.

The complete game tree can be accessed through the root node, but the
following convenience methods are also provided. They return the same
:class:`Tree_node` objects that would be reached via the root node.

Some of the convenience methods are for accessing the :dfn:`leftmost`
variation of the game tree. This is the variation which appears first in the
|sgf| ``GameTree``, often shown in graphical editors as the topmost horizontal
line of nodes. In a game tree without variations, the leftmost variation is
just the whole game.


.. method:: Sgf_game.get_last_node()

   :rtype: :class:`Tree_node`

   Returns the last (leaf) node in the leftmost variation.

.. method:: Sgf_game.get_main_sequence()

   :rtype: list of :class:`Tree_node` objects

   Returns the complete leftmost variation. The first element is the root
   node, and the last is a leaf.

.. method:: Sgf_game.get_main_sequence_below(node)

   :rtype: list of :class:`Tree_node` objects

   Returns the leftmost variation beneath the :class:`Tree_node` *node*. The
   first element is the first child of *node*, and the last is a leaf.

   Note that this isn't necessarily part of the leftmost variation of the
   game as a whole.

.. method:: Sgf_game.get_main_sequence_above(node)

   :rtype: list of :class:`Tree_node` objects

   Returns the partial variation leading to the :class:`Tree_node` *node*. The
   first element is the root node, and the last is the parent of *node*.

.. method:: Sgf_game.extend_main_sequence()

   :rtype: :class:`Tree_node`

   Creates a new :class:`Tree_node`, adds it to the leftmost variation, and
   returns it.

   This is equivalent to
   :meth:`get_last_node`\ .\ :meth:`~Tree_node.new_child`


Root node properties
""""""""""""""""""""

The root node contains global properties for the game tree, and typically also
contains *game-info* properties. It sometimes also contains *setup* properties
(for example, if the game does not begin with an empty board).

Changing the ``FF`` and ``GM`` properties is permitted, but Sgfmill will carry
on using the FF[4] and GM[1] (Go) rules.

Changing ``SZ`` is not permitted (but if the size is 19 you may remove the
property).

Changing ``CA`` is permitted (this controls the encoding used by
:meth:`~Sgf_game.serialise`).

The following methods provide convenient access to some of the root node's
|sgf| properties. The main difference between using these methods and using
:meth:`~Tree_node.get` on the root node is that these methods return the
appropriate default value if the property is not present.

.. method:: Sgf_game.get_size()

   :rtype: integer

   Returns the board size (``19`` if the ``SZ`` root property isn't present).

.. method:: Sgf_game.get_charset()

   :rtype: string

   Returns the effective value of the ``CA`` root property (``ISO-8859-1`` if
   the ``CA`` root property isn't present).

   The returned value is a codec name in normalised form, which may not be
   identical to the string returned by ``get_root().get("CA")``. Raises
   :exc:`ValueError` if the property value doesn't identify a Python codec.

   This gives the encoding that would be used by :meth:`serialise`. It is not
   necessarily the same as the :doc:`raw property encoding <encoding>` (use
   :meth:`~Tree_node.get_encoding` on the root node to retrieve that).


.. method:: Sgf_game.get_komi()

   :rtype: float

   Returns the :term:`komi` (``0.0`` if the ``KM`` root property isn't
   present).

   Raises :exc:`ValueError` if the ``KM`` root property is present but
   malformed.

.. method:: Sgf_game.get_handicap()

   :rtype: integer or ``None``

   Returns the number of handicap stones.

   Returns ``None`` if the ``HA`` root property isn't present, or if it has
   value zero (which isn't strictly permitted).

   Raises :exc:`ValueError` if the ``HA`` property is otherwise malformed.

.. method:: Sgf_game.get_player_name(colour)

   :rtype: string or ``None``

   Returns the name of the specified player, or ``None`` if the required
   ``PB`` or ``PW`` root property isn't present.

.. method:: Sgf_game.get_winner()

   :rtype: *colour*

   Returns the colour of the winning player.

   Returns ``None`` if the ``RE`` root property isn't present, or if neither
   player won.

.. method:: Sgf_game.set_date([date])

   Sets the ``DT`` root property, to a single date.

   If *date* is specified, it should be a :class:`datetime.date`. Otherwise
   the current date is used.

   (|sgf| allows ``DT`` to be rather more complicated than a single date, so
   there's no corresponding get_date() method.)


