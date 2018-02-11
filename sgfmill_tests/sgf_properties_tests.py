"""Tests for sgf_properties.py."""

from textwrap import dedent

from . import sgfmill_test_support

from sgfmill import sgf_properties

def make_tests(suite):
    suite.addTests(sgfmill_test_support.make_simple_tests(globals()))

def test_interpret_simpletext(tc):
    def interpret(bb, encoding):
        context = sgf_properties._Context(19, encoding)
        return sgf_properties.interpret_simpletext(bb, context)
    tc.assertEqual(interpret(b"a\nb\\\\c", "utf-8"), "a b\\c")
    s = "test \N{POUND SIGN}"
    tc.assertEqual(interpret(s.encode("utf-8"), "UTF-8"), s)
    tc.assertEqual(interpret(s.encode("iso-8859-1"), "ISO-8859-1"), s)
    tc.assertRaises(UnicodeDecodeError, interpret,
                    s.encode("iso-8859-1"), "UTF-8")
    tc.assertRaises(UnicodeDecodeError, interpret, s.encode("utf-8"), "ASCII")

def test_serialise_simpletext(tc):
    def serialise(s, encoding):
        context = sgf_properties._Context(19, encoding)
        return sgf_properties.serialise_simpletext(s, context)
    tc.assertEqual(serialise("ab\\c", "utf-8"), b"ab\\\\c")
    s = "test \N{POUND SIGN}"
    tc.assertEqual(serialise(s, "UTF-8"), s.encode("utf-8"))
    tc.assertEqual(serialise(s, "ISO-8859-1"), s.encode("iso-8859-1"))
    tc.assertRaises(UnicodeEncodeError, serialise, "\N{EN DASH}", "ISO-8859-1")
    tc.assertRaisesRegex(TypeError, "^expected string, given bytes$",
                         serialise, b'test', "utf-8")

def test_interpret_text(tc):
    def interpret(bb, encoding):
        context = sgf_properties._Context(19, encoding)
        return sgf_properties.interpret_text(bb, context)
    tc.assertEqual(interpret(b"a\nb\\\\c", "utf-8"), "a\nb\\c")
    s = "test \N{POUND SIGN}"
    tc.assertEqual(interpret(s.encode("utf-8"), "UTF-8"), s)
    tc.assertEqual(interpret(s.encode("iso-8859-1"), "ISO-8859-1"), s)
    tc.assertRaises(UnicodeDecodeError, interpret,
                    s.encode("iso-8859-1"), "UTF-8")
    tc.assertRaises(UnicodeDecodeError, interpret, s.encode("utf-8"), "ASCII")

def test_serialise_text(tc):
    def serialise(s, encoding):
        context = sgf_properties._Context(19, encoding)
        return sgf_properties.serialise_text(s, context)
    tc.assertEqual(serialise("ab\\c", "utf-8"), b"ab\\\\c")
    s = "test \N{POUND SIGN}"
    tc.assertEqual(serialise(s, "UTF-8"), s.encode("utf-8"))
    tc.assertEqual(serialise(s, "ISO-8859-1"), s.encode("iso-8859-1"))
    tc.assertRaises(UnicodeEncodeError, serialise, "\N{EN DASH}", "ISO-8859-1")
    tc.assertRaisesRegex(TypeError, "^expected string, given bytes$",
                         serialise, b'test', "utf-8")

def test_interpret_none(tc):
    interpret_none = sgf_properties.interpret_none
    tc.assertIs(interpret_none(b""), True)
    tc.assertIs(interpret_none(b"xxx"), True)

def test_serialise_none(tc):
    serialise_none = sgf_properties.serialise_none
    tc.assertEqual(serialise_none(None), b"")
    tc.assertEqual(serialise_none(1), b"")
    tc.assertEqual(serialise_none("x"), b"")

def test_interpret_number(tc):
    interpret_number = sgf_properties.interpret_number
    tc.assertEqual(interpret_number(b"1"), 1)
    tc.assertIs(type(interpret_number(b"1")), int)
    tc.assertEqual(interpret_number(b"0"), 0)
    tc.assertEqual(interpret_number(b"-1"), -1)
    tc.assertEqual(interpret_number(b"+1"), 1)
    tc.assertEqual(interpret_number(b" 3"), 3)
    tc.assertEqual(interpret_number(b"4\n"), 4)
    tc.assertEqual(interpret_number(b"+ 1"), 1)
    tc.assertEqual(interpret_number(b"- 1"), -1)
    tc.assertEqual(interpret_number(b"1 2"), 12)
    # Python 3.6 or later will accept this
    #tc.assertEqual(interpret_number(b"1_2"), 12)
    tc.assertRaises(ValueError, interpret_number, b"1.5")
    tc.assertRaises(ValueError, interpret_number, b"0xaf")
    tc.assertRaises(Exception, interpret_number, 1)
    #tc.assertRaises(TypeError, interpret_number, "1")

def test_serialise_number(tc):
    serialise_number = sgf_properties.serialise_number
    tc.assertEqual(serialise_number(0), b"0")
    tc.assertEqual(serialise_number(1), b"1")
    tc.assertEqual(serialise_number(2), b"2")
    tc.assertEqual(serialise_number(2.0), b"2")
    tc.assertEqual(serialise_number(2.5), b"2")
    tc.assertRaises(TypeError, serialise_number, "1")

def test_interpret_real(tc):
    interpret_real = sgf_properties.interpret_real
    tc.assertEqual(interpret_real(b"1"), 1.0)
    tc.assertIs(type(interpret_real(b"1")), float)
    tc.assertEqual(interpret_real(b"0"), 0.0)
    tc.assertEqual(interpret_real(b"1.0"), 1.0)
    tc.assertEqual(interpret_real(b"1.5"), 1.5)
    tc.assertEqual(interpret_real(b"-1.5"), -1.5)
    tc.assertEqual(interpret_real(b"+0.5"), 0.5)
    tc.assertRaises(ValueError, interpret_real, b"+")
    tc.assertRaises(ValueError, interpret_real, b"0xaf")
    tc.assertRaises(ValueError, interpret_real, b"inf")
    tc.assertRaises(ValueError, interpret_real, b"-inf")
    tc.assertRaises(ValueError, interpret_real, b"NaN")
    tc.assertRaises(ValueError, interpret_real, b"1e400")
    tc.assertRaises(TypeError, interpret_real, None)
    #tc.assertRaises(TypeError, interpret_real, "1.0")
    #tc.assertRaises(TypeError, interpret_real, 1.0)

def test_serialise_real(tc):
    serialise_real = sgf_properties.serialise_real
    tc.assertEqual(serialise_real(1), b"1")
    tc.assertEqual(serialise_real(-1), b"-1")
    tc.assertEqual(serialise_real(1.0), b"1")
    tc.assertEqual(serialise_real(-1.0), b"-1")
    tc.assertEqual(serialise_real(1.5), b"1.5")
    tc.assertEqual(serialise_real(-1.5), b"-1.5")
    tc.assertEqual(serialise_real(0.001), b"0.001")
    tc.assertEqual(serialise_real(0.0001), b"0.0001")
    tc.assertEqual(serialise_real(0.00001), b"0")
    tc.assertEqual(serialise_real(1e15), b"1000000000000000")
    tc.assertEqual(serialise_real(1e16), b"10000000000000000")
    tc.assertEqual(serialise_real(1e17), b"100000000000000000")
    tc.assertEqual(serialise_real(1e18), b"1000000000000000000")
    tc.assertEqual(serialise_real(-1e18), b"-1000000000000000000")
    # 1e400 is inf
    tc.assertRaises(ValueError, serialise_real, 1e400)
    tc.assertRaises(ValueError, serialise_real, float("NaN"))

def test_interpret_double(tc):
    interpret_double = sgf_properties.interpret_double
    tc.assertEqual(interpret_double(b"1"), 1)
    tc.assertEqual(interpret_double(b"2"), 2)
    tc.assertEqual(interpret_double(b"x"), 1)
    tc.assertEqual(interpret_double(b""), 1)

def test_serialise_double(tc):
    serialise_double = sgf_properties.serialise_double
    tc.assertEqual(serialise_double(1), b"1")
    tc.assertEqual(serialise_double(2), b"2")
    tc.assertEqual(serialise_double(0), b"1")
    tc.assertEqual(serialise_double(3), b"1")

def test_interpret_colour(tc):
    interpret_colour = sgf_properties.interpret_colour
    tc.assertEqual(interpret_colour(b"b"), "b")
    tc.assertEqual(interpret_colour(b"w"), "w")
    tc.assertEqual(interpret_colour(b"B"), "b")
    tc.assertEqual(interpret_colour(b"W"), "w")
    tc.assertRaises(ValueError, interpret_colour, b"")
    tc.assertRaises(ValueError, interpret_colour, b"x")

def test_serialise_colour(tc):
    serialise_colour = sgf_properties.serialise_colour
    tc.assertEqual(serialise_colour('b'), b"B")
    tc.assertEqual(serialise_colour('w'), b"W")
    tc.assertRaises(ValueError, serialise_colour, "")
    tc.assertRaises(ValueError, serialise_colour, "x")
    tc.assertRaises(ValueError, serialise_colour, "B")
    tc.assertRaises(ValueError, serialise_colour, "W")

def test_interpret_move(tc):
    def interpret_move(s, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.interpret_move(s, context)
    tc.assertEqual(interpret_move(b"aa", 19), (18, 0))
    tc.assertEqual(interpret_move(b"ai", 19), (10, 0))
    tc.assertEqual(interpret_move(b"ba",  9), (8, 1))
    tc.assertEqual(interpret_move(b"tt", 21), (1, 19))
    tc.assertIs(interpret_move(b"tt", 19), None)
    tc.assertIs(interpret_move(b"", 19), None)
    tc.assertIs(interpret_move(b"", 21), None)
    tc.assertRaises(ValueError, interpret_move, b"Aa", 19)
    tc.assertRaises(ValueError, interpret_move, b"aA", 19)
    tc.assertRaises(ValueError, interpret_move, b"aaa", 19)
    tc.assertRaises(ValueError, interpret_move, b"a", 19)
    tc.assertRaises(ValueError, interpret_move, b"au", 19)
    tc.assertRaises(ValueError, interpret_move, b"ua", 19)
    tc.assertRaises(ValueError, interpret_move, b"a`", 19)
    tc.assertRaises(ValueError, interpret_move, b"`a", 19)
    tc.assertRaises(ValueError, interpret_move, b"11", 19)
    tc.assertRaises(ValueError, interpret_move, b" aa", 19)
    tc.assertRaises(ValueError, interpret_move, b"aa\x00", 19)
    tc.assertRaises(TypeError, interpret_move, None, 19)
    tc.assertRaises(TypeError, interpret_move, "aa", 19)
    tc.assertRaises(TypeError, interpret_move, (b'a', b'a'), 19)
    # tc.assertRaises(TypeError, interpret_move, (97, 97), 19)

def test_serialise_move(tc):
    def serialise_move(s, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.serialise_move(s, context)
    tc.assertEqual(serialise_move((18, 0), 19), b"aa")
    tc.assertEqual(serialise_move((10, 0), 19), b"ai")
    tc.assertEqual(serialise_move((8, 1), 19), b"bk")
    tc.assertEqual(serialise_move((8, 1), 9), b"ba")
    tc.assertEqual(serialise_move((1, 19), 21), b"tt")
    tc.assertEqual(serialise_move(None, 19), b"tt")
    tc.assertEqual(serialise_move(None, 20), b"")
    tc.assertRaises(ValueError, serialise_move, (3, 3), 0)
    tc.assertRaises(ValueError, serialise_move, (3, 3), 27)
    tc.assertRaises(ValueError, serialise_move, (9, 0), 9)
    tc.assertRaises(ValueError, serialise_move, (-1, 0), 9)
    tc.assertRaises(ValueError, serialise_move, (0, 9), 9)
    tc.assertRaises(ValueError, serialise_move, (0, -1), 9)
    tc.assertRaises(TypeError, serialise_move, (1, 1.5), 9)

def test_interpret_point(tc):
    def interpret_point(s, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.interpret_point(s, context)
    tc.assertEqual(interpret_point(b"aa", 19), (18, 0))
    tc.assertEqual(interpret_point(b"ai", 19), (10, 0))
    tc.assertEqual(interpret_point(b"ba",  9), (8, 1))
    tc.assertEqual(interpret_point(b"tt", 21), (1, 19))
    tc.assertRaises(ValueError, interpret_point, b"tt", 19)
    tc.assertRaises(ValueError, interpret_point, b"", 19)
    tc.assertRaises(ValueError, interpret_point, b"", 21)
    tc.assertRaises(ValueError, interpret_point, b"Aa", 19)
    tc.assertRaises(ValueError, interpret_point, b"aA", 19)
    tc.assertRaises(ValueError, interpret_point, b"aaa", 19)
    tc.assertRaises(ValueError, interpret_point, b"a", 19)
    tc.assertRaises(ValueError, interpret_point, b"au", 19)
    tc.assertRaises(ValueError, interpret_point, b"ua", 19)
    tc.assertRaises(ValueError, interpret_point, b"a`", 19)
    tc.assertRaises(ValueError, interpret_point, b"`a", 19)
    tc.assertRaises(ValueError, interpret_point, b"11", 19)
    tc.assertRaises(ValueError, interpret_point, b" aa", 19)
    tc.assertRaises(ValueError, interpret_point, b"aa\x00", 19)
    tc.assertRaises(TypeError, interpret_point, None, 19)
    tc.assertRaises(TypeError, interpret_point, (b'a', b'a'), 19)
    # tc.assertRaises(TypeError, interpret_point, (97, 97), 19)

def test_serialise_point(tc):
    def serialise_point(s, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.serialise_point(s, context)
    tc.assertEqual(serialise_point((18, 0), 19), b"aa")
    tc.assertEqual(serialise_point((10, 0), 19), b"ai")
    tc.assertEqual(serialise_point((8, 1), 19), b"bk")
    tc.assertEqual(serialise_point((8, 1), 9), b"ba")
    tc.assertEqual(serialise_point((1, 19), 21), b"tt")
    tc.assertRaises(ValueError, serialise_point, None, 19)
    tc.assertRaises(ValueError, serialise_point, None, 20)
    tc.assertRaises(ValueError, serialise_point, (3, 3), 0)
    tc.assertRaises(ValueError, serialise_point, (3, 3), 27)
    tc.assertRaises(ValueError, serialise_point, (9, 0), 9)
    tc.assertRaises(ValueError, serialise_point, (-1, 0), 9)
    tc.assertRaises(ValueError, serialise_point, (0, 9), 9)
    tc.assertRaises(ValueError, serialise_point, (0, -1), 9)
    tc.assertRaises(TypeError, serialise_point, (1, 1.5), 9)


def test_interpret_point_list(tc):
    def ipl(l, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.interpret_point_list(l, context)
    tc.assertEqual(ipl([], 19),
                   set())
    tc.assertEqual(ipl([b"aa"], 19),
                   {(18, 0)})
    tc.assertEqual(ipl([b"aa", b"ai"], 19),
                   {(18, 0), (10, 0)})
    tc.assertEqual(ipl([b"ab:bc"], 19),
                   {(16, 0), (16, 1), (17, 0), (17, 1)})
    tc.assertEqual(ipl([b"ab:bc", b"aa"], 19),
                   {(18, 0), (16, 0), (16, 1), (17, 0), (17, 1)})
    # overlap is forbidden by the spec, but we accept it
    tc.assertEqual(ipl([b"aa", b"aa"], 19),
                   {(18, 0)})
    tc.assertEqual(ipl([b"ab:bc", b"bb:bc"], 19),
                   {(16, 0), (16, 1), (17, 0), (17, 1)})
    # 1x1 rectangles are forbidden by the spec, but we accept them
    tc.assertEqual(ipl([b"aa", b"bb:bb"], 19),
                   {(18, 0), (17, 1)})
    # 'backwards' rectangles are forbidden by the spec, and we reject them
    tc.assertRaises(ValueError, ipl, [b"ab:aa"], 19)
    tc.assertRaises(ValueError, ipl, [b"ba:aa"], 19)
    tc.assertRaises(ValueError, ipl, [b"bb:aa"], 19)

    tc.assertRaises(ValueError, ipl, [b"aa", b"tt"], 19)
    tc.assertRaises(ValueError, ipl, [b"aa", b""], 19)
    tc.assertRaises(ValueError, ipl, [b"aa:", b"aa"], 19)
    tc.assertRaises(ValueError, ipl, [b"aa:tt", b"aa"], 19)
    tc.assertRaises(ValueError, ipl, [b"tt:aa", b"aa"], 19)

def test_compressed_point_list_spec_example(tc):
    # Checks the examples at http://www.red-bean.com/sgf/DD_VW.html
    def sgf_point(move, size):
        row, col = move
        row = size - row - 1
        col_s = b"abcdefghijklmnopqrstuvwxy"[col]
        row_s = b"abcdefghijklmnopqrstuvwxy"[row]
        return bytes((col_s, row_s))

    def ipl(l, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.interpret_point_list(l, context)
    tc.assertEqual(
        set(sgf_point(move, 9) for move in ipl([b"ac:ic"], 9)),
        {b"ac", b"bc", b"cc", b"dc", b"ec", b"fc", b"gc", b"hc", b"ic"})
    tc.assertEqual(
        set(sgf_point(move, 9) for move in ipl([b"ae:ie"], 9)),
        {b"ae", b"be", b"ce", b"de", b"ee", b"fe", b"ge", b"he", b"ie"})
    tc.assertEqual(
        set(sgf_point(move, 9) for move in ipl([b"aa:bi", b"ca:ce"], 9)),
        {b"aa", b"ab", b"ac", b"ad", b"ae", b"af", b"ag", b"ah", b"ai",
         b"bi", b"bh", b"bg", b"bf", b"be", b"bd", b"bc", b"bb", b"ba",
         b"ca", b"cb", b"cc", b"cd", b"ce"})

def test_serialise_point_list(tc):
    def ipl(l, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.interpret_point_list(l, context)
    def spl(l, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.serialise_point_list(l, context)

    tc.assertEqual(spl([(18, 0), (17, 1)], 19), [b'aa', b'bb'])
    tc.assertEqual(spl([(17, 1), (18, 0)], 19), [b'aa', b'bb'])
    tc.assertEqual(spl([], 9), [])
    tc.assertEqual(ipl(spl([(1,2), (3,4), (4,5)], 19), 19),
                   {(1,2), (3,4), (4,5)})
    tc.assertRaises(ValueError, spl, [(18, 0), None], 19)


def test_AP(tc):
    def serialise(arg):
        context = sgf_properties._Context(19, "UTF-8")
        return sgf_properties.serialise_AP(arg, context)
    def interpret(arg):
        context = sgf_properties._Context(19, "UTF-8")
        return sgf_properties.interpret_AP(arg, context)

    tc.assertEqual(serialise(("foo:bar", "2\n3")), b"foo\\:bar:2\n3")
    tc.assertEqual(interpret(b"foo\\:bar:2 3"), ("foo:bar", "2 3"))
    tc.assertEqual(interpret(b"foo bar"), ("foo bar", ""))

def test_ARLN(tc):
    def serialise(arg, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.serialise_ARLN_list(arg, context)
    def interpret(arg, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.interpret_ARLN_list(arg, context)

    tc.assertEqual(serialise([], 19), [])
    tc.assertEqual(interpret([], 19), [])
    tc.assertEqual(serialise([((7, 0), (5, 2)), ((4, 3), (2, 5))], 9),
                   [b'ab:cd', b'de:fg'])
    tc.assertEqual(interpret([b'ab:cd', b'de:fg'], 9),
                   [((7, 0), (5, 2)), ((4, 3), (2, 5))])
    tc.assertRaises(ValueError, serialise, [((7, 0), None)], 9)
    tc.assertRaises(ValueError, interpret, [b'ab:tt', b'de:fg'], 9)

def test_FG(tc):
    def serialise(arg):
        context = sgf_properties._Context(19, "UTF-8")
        return sgf_properties.serialise_FG(arg, context)
    def interpret(arg):
        context = sgf_properties._Context(19, "UTF-8")
        return sgf_properties.interpret_FG(arg, context)
    tc.assertEqual(serialise(None), b"")
    tc.assertEqual(interpret(b""), None)
    tc.assertEqual(serialise((515, "th]is")), b"515:th\\]is")
    tc.assertEqual(interpret(b"515:th\\]is"), (515, "th]is"))

def test_LB(tc):
    def serialise(arg, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.serialise_LB_list(arg, context)
    def interpret(arg, size):
        context = sgf_properties._Context(size, "UTF-8")
        return sgf_properties.interpret_LB_list(arg, context)
    tc.assertEqual(serialise([], 19), [])
    tc.assertEqual(interpret([], 19), [])
    tc.assertEqual(
        serialise([((6, 0), "lbl"), ((6, 1), "lb]l2")], 9),
        [b"ac:lbl", b"bc:lb\\]l2"])
    tc.assertEqual(
        interpret([b"ac:lbl", b"bc:lb\\]l2"], 9),
        [((6, 0), "lbl"), ((6, 1), "lb]l2")])
    tc.assertRaises(ValueError, serialise, [(None, "lbl")], 9)
    tc.assertRaises(ValueError, interpret, [b':lbl', b'de:lbl2'], 9)


def test_presenter_interpret(tc):
    p9 = sgf_properties.Presenter(9, "UTF-8")
    p19 = sgf_properties.Presenter(19, "UTF-8")
    tc.assertEqual(p9.interpret('KO', [b""]), True)
    tc.assertEqual(p9.interpret('SZ', [b"9"]), 9)
    tc.assertRaisesRegex(ValueError, "multiple values",
                          p9.interpret, 'SZ', [b"9", b"blah"])
    tc.assertEqual(p9.interpret('CR', [b"ab", b"cd"]), {(5, 2), (7, 0)})
    tc.assertRaises(ValueError, p9.interpret, 'SZ', [])
    tc.assertRaises(ValueError, p9.interpret, 'CR', [])
    tc.assertEqual(p9.interpret('DD', [b""]), set())
    # all lists are treated like elists
    tc.assertEqual(p9.interpret('CR', [b""]), set())

def test_presenter_serialise(tc):
    p9 = sgf_properties.Presenter(9, "UTF-8")
    p19 = sgf_properties.Presenter(19, "UTF-8")

    tc.assertEqual(p9.serialise('KO', True), [b""])
    tc.assertEqual(p9.serialise('SZ', 9), [b"9"])
    tc.assertEqual(p9.serialise('KM', 3.5), [b"3.5"])
    tc.assertEqual(p9.serialise('C', "foo\\:b]ar\n"), [b"foo\\\\:b\\]ar\n"])
    tc.assertEqual(p19.serialise('B', (1, 2)), [b"cr"])
    tc.assertEqual(p9.serialise('B', None), [b"tt"])
    tc.assertEqual(p19.serialise('AW', {(17, 1), (18, 0)}), [b"aa", b"bb"])
    tc.assertEqual(p9.serialise('DD', [(1, 2), (3, 4)]), [b"ch", b"ef"])
    tc.assertEqual(p9.serialise('DD', []), [b""])
    tc.assertRaisesRegex(ValueError, "empty list", p9.serialise, 'CR', [])
    tc.assertEqual(p9.serialise('AP', ("na:me", "2.3")), [b"na\\:me:2.3"])
    tc.assertEqual(p9.serialise('FG', (515, "th]is")), [b"515:th\\]is"])
    tc.assertEqual(p9.serialise('XX', "foo\\bar"), [b"foo\\\\bar"])

    tc.assertRaises(ValueError, p9.serialise, 'B', (1, 9))

def test_presenter_private_properties(tc):
    p9 = sgf_properties.Presenter(9, "UTF-8")
    tc.assertEqual(p9.serialise('XX', "9"), [b"9"])
    tc.assertEqual(p9.interpret('XX', [b"9"]), "9")
    p9.set_private_property_type(p9.get_property_type("SZ"))
    tc.assertEqual(p9.serialise('XX', 9), [b"9"])
    tc.assertEqual(p9.interpret('XX', [b"9"]), 9)
    p9.set_private_property_type(None)
    tc.assertRaisesRegex(ValueError, "unknown property",
                         p9.serialise, 'XX', "foo\\bar")
    tc.assertRaisesRegex(ValueError, "unknown property",
                         p9.interpret, 'XX', [b"asd"])

