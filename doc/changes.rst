Changes
=======

Sgfmill 1.1.1 (2018-05-20)
--------------------------

* Sped up the :class:`.Board` implementation (thanks to Seth Troisi).


Sgfmill 1.1 (2018-02-11)
------------------------

* The parser now permits lower-case letters in *PropIdents*; see
  :doc:`parsing` for details.

* Bug fix: :meth:`.Tree_node.set` didn't check its ``identifier`` parameter
  was a well-formed *PropIdent*.

* Bug fix: :meth:`.Tree_node.set` was willing to store invalid values for
  properties of type Number, if fed invalid input.


Sgfmill 1.0 (2017-04-17)
------------------------

* Python 3 port of the SGF code from Gomill__ 0.8.

* Added the :mod:`.sgf_board_interface` module.

.. __: https://mjw.woodcraft.me.uk/gomill/

