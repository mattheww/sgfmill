"""Sgfmill-specific test support code."""

import re
import textwrap
import unittest

from . import test_framework

from sgfmill.common import format_vertex
from sgfmill import ascii_boards
from sgfmill import boards

# This makes TestResult ignore lines from this module in tracebacks
__unittest = True


def dedent(v):
    """Variant of textwrap.dedent which also accepts bytes."""
    if isinstance(v, bytes):
        return textwrap.dedent(v.decode("iso-8859-1")).encode("iso-8859-1")
    else:
        return textwrap.dedent(v)


def compare_boards(b1, b2):
    """Check whether two boards have the same position.

    returns a pair (position_is_the_same, message)

    """
    if b1.side != b2.side:
        raise ValueError("size is different: %s, %s" % (b1.side, b2.side))
    differences = []
    for row, col in b1.board_points:
        if b1.get(row, col) != b2.get(row, col):
            differences.append((row, col))
    if not differences:
        return True, None
    msg = "boards differ at %s" % " ".join(map(format_vertex, differences))
    try:
        msg += "\n%s\n%s" % (
            ascii_boards.render_board(b1), ascii_boards.render_board(b2))
    except Exception:
        pass
    return False, msg

def compare_boards_or_diagrams(b1, b2):
    """Variant of compare_boards which allows diagrams too.

    returns a pair (position_is_the_same, message)

    Compares as boards if the diagram can be interpreted; otherwise renders the
    board and compares as strings.

    If given two diagrams, compares them as strings.

    Note that board comparision is more lenient than string comparison, to
    whatever extent interpret_diagram() is lenient (in particular it accepts
    leading and trailing whitespace).

    """
    def coerce(board, diagram):
        try:
            return board, ascii_boards.interpret_diagram(diagram, board.side)
        except ValueError:
            return ascii_boards.render_board(board), diagram
    if isinstance(b1, boards.Board) and isinstance(b2, str):
        b1, b2 = coerce(b1, b2)
    elif isinstance(b2, boards.Board) and isinstance(b1, str):
        b2, b1 = coerce(b2, b1)
    if isinstance(b1, boards.Board):
        return compare_boards(b1, b2)
    else:
        return compare_diagrams(b1, b2)

def compare_diagrams(d1, d2):
    """Compare two ascii board diagrams.

    returns a pair (strings_are_equal, message)

    (assertMultiLineEqual tends to look nasty for these, so we just show them
    both in full)

    """
    if d1 == d2:
        return True, None
    return False, "diagrams differ:\n%s\n\n%s" % (d1, d2)

class Sgfmill_testcase_mixin:
    """TestCase mixin adding support for sgfmill-specific types.

    Board/diagram features:
     assertBoardEqual
     assertDiagramEqual
     assertEqual and assertNotEqual for Boards

    """
    def init_sgfmill_testcase_mixin(self):
        self.addTypeEqualityFunc(boards.Board, self.assertBoardEqual)

    def _format_message(self, msg, standardMsg):
        # This is the same as _formatMessage from python 3.4 unittest; copying
        # it because it's not part of the public API.
        if not self.longMessage:
            return msg or standardMsg
        if msg is None:
            return standardMsg
        try:
            return '%s : %s' % (standardMsg, msg)
        except UnicodeDecodeError:
            return '%s : %s' % (unittest.util.safe_repr(standardMsg),
                                unittest.util.safe_repr(msg))

    def assertBoardEqual(self, b1, b2, msg=None):
        """assertEqual for two boards.

        Accepts diagrams too; see compare_boards_or_diagrams.

        """
        are_equal, desc = compare_boards_or_diagrams(b1, b2)
        if not are_equal:
            self.fail(self._format_message(msg, desc+"\n"))

    def assertDiagramEqual(self, d1, d2, msg=None):
        """Variant of assertMultiLineEqual for board diagrams.

        Checks that two strings are equal, with difference reporting
        appropriate for board diagrams.

        """
        are_equal, desc = compare_diagrams(d1, d2)
        if not are_equal:
            self.fail(self._format_message(msg, desc+"\n"))

    def assertNotEqual(self, first, second, msg=None):
        if isinstance(first, boards.Board) and isinstance(second, boards.Board):
            are_equal, _ = compare_boards(first, second)
            if not are_equal:
                return
            msg = self._format_message(msg, 'boards have the same position')
            raise self.failureException(msg)
        super().assertNotEqual(first, second, msg)


class Sgfmill_SimpleTestCase(Sgfmill_testcase_mixin,
                             test_framework.SimpleTestCase):
    """SimpleTestCase with the Sgfmill mixin."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_sgfmill_testcase_mixin()

class Sgfmill_ParameterisedTestCase(Sgfmill_testcase_mixin,
                                    test_framework.ParameterisedTestCase):
    """ParameterisedTestCase with the Sgfmill mixin."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_sgfmill_testcase_mixin()


def make_simple_tests(source, prefix="test_"):
    """Make test cases from a module's test_xxx functions.

    See test_framework for details.

    The test functions can use the Sgfmill_testcase_mixin enhancements.

    """
    return test_framework.make_simple_tests(
        source, prefix, testcase_class=Sgfmill_SimpleTestCase)
