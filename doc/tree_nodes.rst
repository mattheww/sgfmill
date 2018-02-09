:class:`!Tree_node` objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: sgfmill.sgf

.. class:: Tree_node

   A Tree_node object represents a single node from an |sgf| file.

   Don't instantiate :class:`!Tree_node` objects directly; retrieve them from
   :class:`Sgf_game` objects.

.. contents:: Page contents
   :local:
   :backlinks: none


Attributes
""""""""""

   Tree_node objects have the following attributes (which should be treated as
   read-only):

   .. attribute:: owner

      The :class:`Sgf_game` that the node belongs to.

   .. attribute:: parent

      The node's parent :class:`!Tree_node` (``None`` for the root node).


Tree navigation
"""""""""""""""

A :class:`!Tree_node` acts as a list-like container of its children: it can be
indexed, sliced, and iterated over like a list, and it supports the `index`__
method.

A :class:`!Tree_node` with no children is treated as having truth value false.

For example, to find all leaf nodes::

  def print_leaf_comments(node):
      if node:
          for child in node:
              print_leaf_comments(child)
      else:
          if node.has_property("C"):
              print(node.get("C"))
          else:
              print("--")

.. __: https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types


Property access
"""""""""""""""

Each node holds a number of :dfn:`properties`. Each property is identified by
a short string called the :dfn:`PropIdent`, eg ``"SZ"`` or ``"B"``. See
:doc:`properties` for a list of the standard properties. See the
:term:`SGF` specification for full details. See :doc:`parsing` for
restrictions on well-formed *PropIdents*.

Sgfmill doesn't enforce |sgf|'s restrictions on where properties can appear
(eg, the distinction between *setup* and *move* properties).

The principal methods for accessing the node's properties are:

.. method:: Tree_node.get(identifier)

   Returns a native Python representation of the value of the property whose
   *PropIdent* is *identifier*.

   Raises :exc:`KeyError` if the property isn't present.

   Raises :exc:`ValueError` if it detects that the property value is
   malformed.

   See :ref:`sgf_property_types` for details of how property values are
   represented in Python.

   See :doc:`properties` for a list of the known properties. Any other
   property is treated as having type Text.

.. method:: Tree_node.set(identifier, value)

   Sets the value of the property whose *PropIdent* is *identifier*.

   *value* should be a native Python representation of the required property
   value (as returned by :meth:`get`).

   Raises :exc:`ValueError` if the identifier isn't a well-formed *PropIdent*,
   or if the property value isn't acceptable.

   See :ref:`sgf_property_types` for details of how property values should be
   represented in Python.

   See :doc:`properties` for a list of the known properties. Setting
   nonstandard properties is permitted; they are treated as having type Text.

.. method:: Tree_node.unset(identifier)

   Removes the property whose *PropIdent* is *identifier* from the node.

   Raises :exc:`KeyError` if the property isn't currently present.

.. method:: Tree_node.has_property(identifier)

   :rtype: bool

   Checks whether the property whose *PropIdent* is *identifier* is present.

.. method:: Tree_node.properties()

   :rtype: list of strings

   Lists the properties which are present in the node.

   Returns a list of *PropIdents*, in unspecified order.

.. method:: Tree_node.find_property(identifier)

   Returns the value of the property whose *PropIdent* is *identifier*,
   looking in the node's ancestors if necessary.

   This is intended for use with properties of type *game-info*, and with
   properties which have the *inherit* attribute.

   It looks first in the node itself, then in its parent, and so on up to the
   root, returning the first value it finds. Otherwise the behaviour is the
   same as :meth:`get`.

   Raises :exc:`KeyError` if no node defining the property is found.


.. method:: Tree_node.find(identifier)

   :rtype: :class:`!Tree_node` or ``None``

   Returns the nearest node defining the property whose *PropIdent* is
   *identifier*.

   Searches in the same way as :meth:`find_property`, but returns the node
   rather than the property value. Returns ``None`` if no node defining the
   property is found.


Convenience methods for properties
""""""""""""""""""""""""""""""""""

The following convenience methods are also provided, for more flexible access
to a few of the most important properties:

.. method:: Tree_node.get_move()

   :rtype: tuple (*colour*, *move*)

   Indicates which of the the ``B`` or ``W`` properties is present, and
   returns its value.

   Returns (``None``, ``None``) if neither property is present.

.. method:: Tree_node.set_move(colour, move)

   Sets the ``B`` or ``W`` property. If the other property is currently
   present, it is removed.

   Sgfmill doesn't attempt to ensure that moves are legal.

.. method:: Tree_node.get_setup_stones()

   :rtype: tuple (set of *points*, set of *points*, set of *points*)

   Returns the settings of the ``AB``, ``AW``, and ``AE`` properties.

   The tuple elements represent black, white, and empty points respectively.
   If a property is missing, the corresponding set is empty.

.. method:: Tree_node.set_setup_stones(black, white[, empty])

   Sets the ``AB``, ``AW``, and ``AE`` properties.

   Each parameter should be a sequence or set of *points*. If a parameter
   value is empty (or, in the case of *empty*, if the parameter is
   omitted) the corresponding property will be unset.

.. method:: Tree_node.has_setup_stones()

   :rtype: bool

   Returns ``True`` if the ``AB``, ``AW``, or ``AE`` property is present.

.. method:: Tree_node.add_comment_text(text)

   If the ``C`` property isn't already present, adds it with the value given
   by the string *text*.

   Otherwise, appends *text* to the existing ``C`` property value, preceded by
   two newlines.


Board size and raw property encoding
""""""""""""""""""""""""""""""""""""

Each :class:`!Tree_node` knows its game's board size, and its :ref:`raw
property encoding <raw_property_encoding>` (because these are needed to
interpret property values). They can be retrieved using the following methods:

.. method:: Tree_node.get_size()

   :rtype: int

.. method:: Tree_node.get_encoding()

   :rtype: string

   This returns the name of the raw property encoding (in a normalised form,
   which may not be the same as the string originally used to specify the
   encoding).

An attempt to change the value of the ``SZ`` property so that it doesn't match
the board size will raise :exc:`ValueError` (even if the node isn't the root).


Access to raw property values
"""""""""""""""""""""""""""""

Raw property values are bytes objects, containing the exact bytes that go
between the ``[`` and ``]`` in the |sgf| file. They should be treated as being
encoded in the node's :ref:`raw property encoding <raw_property_encoding>`
(but there is no guarantee that they hold properly encoded data).

The following methods are provided for access to raw property values. They can
be used to access malformed values, or to avoid the standard escape processing
and whitespace conversion for Text and SimpleText values.

When setting raw property values, any data that is a well formed |sgf|
*PropValue* is accepted: that is, any byte-string that that doesn't contain an
unescaped ``]`` or end with an unescaped ``\``. There is no check that the
string is properly encoded in the raw property encoding.

.. method:: Tree_node.get_raw_list(identifier)

   :rtype: nonempty list of bytes objects

   Returns the raw values of the property whose *PropIdent* is *identifier*.

   Raises :exc:`KeyError` if the property isn't currently present.

   If the property value is an empty elist, returns a list containing a single
   empty bytes object.

.. method:: Tree_node.get_raw(identifier)

   :rtype: bytes object

   Returns the raw value of the property whose *PropIdent* is *identifier*.

   Raises :exc:`KeyError` if the property isn't currently present.

   If the property has multiple `PropValue`\ s, returns the first. If the
   property value is an empty elist, returns an empty bytes object.

.. method:: Tree_node.get_raw_property_map(identifier)

   :rtype: dict: string → list of bytes objects

   Returns a dict mapping *PropIdents* to lists of raw values.

   Returns the same dict object each time it's called.

   Treat the returned dict object as read-only.

.. method:: Tree_node.set_raw_list(identifier, values)

   Sets the raw values of the property whose *PropIdent* is *identifier*.

   *values* must be a nonempty list of bytes objects. To specify an empty
   elist, pass a list containing a single empty bytes object.

   Raises :exc:`ValueError` if the identifier isn't a well-formed *PropIdent*,
   or if any value isn't a well-formed *PropValue*.

.. method:: Tree_node.set_raw(identifier, value)

   Sets the raw value of the property whose *PropIdent* is *identifier*.

   *value* must be a bytes object.

   Raises :exc:`ValueError` if the identifier isn't a well-formed *PropIdent*,
   or if the value isn't a well-formed *PropValue*.


Tree manipulation
"""""""""""""""""

The following methods are provided for manipulating the tree:

.. method:: Tree_node.new_child([index])

   :rtype: :class:`!Tree_node`

   Creates a new :class:`!Tree_node` and adds it to the tree as this node's
   last child.

   If the optional integer *index* parameter is present, the new node is
   inserted in the list of children at the specified index instead (with the
   same behaviour as :meth:`!list.insert`).

   Returns the new node.

.. method:: Tree_node.delete()

   Removes the node from the tree (along with all its descendents).

   Raises :exc:`ValueError` if called on the root node.

   You should not continue to use a node which has been removed from its tree.

.. method:: Tree_node.reparent(new_parent[, index])

   Moves the node from one part of the tree to another (along with all its
   descendents).

   *new_parent* must be a node belonging to the same game.

   Raises :exc:`ValueError` if the operation would create a loop in the tree
   (ie, if *new_parent* is the node being moved or one of its descendents).

   If the optional integer *index* parameter is present, the new node is
   inserted in the new parent's list of children at the specified index;
   otherwise it is placed at the end.

   This method can be used to reorder variations. For example, to make a node
   the leftmost variation of its parent::

     node.reparent(node.parent, 0)

