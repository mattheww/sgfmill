Parser behaviour
================

The parser permits non-|sgf| content to appear before the beginning and after
the end of the game. It identifies the start of |sgf| content by looking for
``(;`` (with possible whitespace between the two characters).

The parser accepts at most 64 letters in *PropIdents* (there is no formal limit
in the specification, but no standard property has more than 2; strings as
long as 9 letters have been found in the wild).

The parser doesn't perform any checks on property values. In particular, it
allows multiple values to be present for any property.

The parser doesn't, in general, attempt to 'fix' ill-formed |sgf| content. As
an exception, if a *PropIdent* appears more than once in a node it is
converted to a single property with multiple values.

The parser permits lower-case letters in *PropIdents* (these are allowed in
some ancient |sgf| variants, and are apparently seen in the wild). It ignores
those letters, so for example ``CoPyright`` is treated as a synonym for ``CP``
and should be retrieved using ``node.get("CP")``.

