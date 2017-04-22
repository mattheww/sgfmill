Character encoding
==================

.. currentmodule:: sgfmill.sgf

The |sgf| format is defined as containing ASCII-encoded data, possibly with
non-ASCII characters in Text and SimpleText property values. The low-level
Sgfmill functions for loading and serialising |sgf| data work with Python
bytes or bytes-like objects.

The encoding used for Text and SimpleText property values is given by the
``CA`` root property (if that isn't present, the encoding is ``ISO-8859-1``).

In order for an encoding to be used in Sgfmill, it must exist as a Python
built-in codec, and it must be compatible with ASCII (at least whitespace,
``\``, ``]``, and ``:`` must be in the usual places). Behaviour is unspecified
if a non-ASCII-compatible encoding is requested.

When encodings are passed as parameters (or returned from functions), they are
represented using the names or aliases of Python built-in codecs (eg
``"UTF-8"`` or ``"ISO-8859-1"``). See `standard encodings`__ for a list.
Values of the ``CA`` property are interpreted in the same way.

  .. __: https://docs.python.org/3/library/codecs.html#standard-encodings


.. _raw_property_encoding:

The raw property encoding
-------------------------

Each :class:`.Sgf_game` and :class:`.Tree_node` has a fixed :dfn:`raw property
encoding`, which is the encoding used internally to store the property values.
The :meth:`Tree_node.get_raw` and :meth:`Tree_node.set_raw` methods use the
raw property encoding.

When an |sgf| game is loaded from a bytes-like object, the raw property
encoding is taken from the ``CA`` root property (unless overridden).
Improperly encoded property values will not be detected until they are
accessed (:meth:`~Tree_node.get` will raise :exc:`ValueError`; use
:meth:`~Tree_node.get_raw` to retrieve the actual bytes).

When an |sgf| game is created from a Python string (which contains Unicode
characters), the raw property encoding is always ``UTF-8``.


.. _changing_ca:

Changing the CA property
------------------------

When an |sgf| game is serialised to a string, the encoding represented by the
``CA`` root property is used. This :dfn:`target encoding` will be the same as
the raw property encoding unless ``CA`` has been changed since the
:class:`.Sgf_game` was created.

When the raw property encoding and the target encoding match, the raw property
values are included unchanged in the output (even if they are improperly
encoded.)

Otherwise, if any raw property value is improperly encoded,
:exc:`UnicodeDecodeError` is raised, and if any property value can't be
represented in the target encoding, :exc:`UnicodeEncodeError` is raised.

If the target encoding doesn't identify a Python codec, :exc:`ValueError` is
raised. The behaviour of :meth:`~Sgf_game.serialise` is unspecified if the
target encoding isn't ASCII-compatible (eg, UTF-16).


.. _transcoding:

Transcoding
-----------

Because changing the ``CA`` property has no effect until you serialise the
game, it doesn't broaden the set of characters you can use when you
:meth:`~Tree_node.set` a property.

If you plan to save a file as ``UTF-8`` and want to be able to set arbitrary
strings, you can ensure the raw property encoding is ``UTF-8`` by changing
``CA`` and reloading the game::

    game = sgf.Sgf_game.from_bytes(...)
    game.get_root().set("CA", "utf-8")
    game = sgf.Sgf_game.from_bytes(game.serialise())
    game.get_root().set("PB", "本因坊秀策")

