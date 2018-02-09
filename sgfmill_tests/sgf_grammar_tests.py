"""Tests for sgf_grammar.py."""

from . import sgfmill_test_support

from sgfmill import sgf_grammar

def make_tests(suite):
    suite.addTests(sgfmill_test_support.make_simple_tests(globals()))

def test_is_valid_property_identifier(tc):
    ivpi = sgf_grammar.is_valid_property_identifier
    tc.assertIs(ivpi("B"), True)
    tc.assertIs(ivpi("PB"), True)
    tc.assertIs(ivpi("ABCDEFGH"), True)
    tc.assertIs(ivpi("MULTIGOGM"), True)
    tc.assertIs(ivpi(64*"X"), True)
    tc.assertIs(ivpi(65*"X"), False)
    tc.assertIs(ivpi(""), False)
    tc.assertIs(ivpi("b"), False)
    tc.assertIs(ivpi("Player"), False)
    tc.assertIs(ivpi("P2"), False)
    tc.assertIs(ivpi(" PB"), False)
    tc.assertIs(ivpi("PB "), False)
    tc.assertIs(ivpi("P B"), False)
    tc.assertIs(ivpi("PB\x00"), False)

def test_is_valid_property_value(tc):
    ivpv = sgf_grammar.is_valid_property_value
    tc.assertIs(ivpv(b""), True)
    tc.assertIs(ivpv(b"hello world"), True)
    tc.assertIs(ivpv(b"hello\nworld"), True)
    tc.assertIs(ivpv(b"hello \x00 world"), True)
    tc.assertIs(ivpv(b"hello \xa3 world"), True)
    tc.assertIs(ivpv(b"hello \xc2\xa3 world"), True)
    tc.assertIs(ivpv(b"hello \\-) world"), True)
    tc.assertIs(ivpv(b"hello (;[) world"), True)
    tc.assertIs(ivpv(b"[hello world]"), False)
    tc.assertIs(ivpv(b"hello ] world"), False)
    tc.assertIs(ivpv(b"hello \\] world"), True)
    tc.assertIs(ivpv(b"hello world \\"), False)
    tc.assertIs(ivpv(b"hello world \\\\"), True)
    tc.assertIs(ivpv(b"x" * 70000), True)

def test_tokeniser(tc):
    tokenise = sgf_grammar.tokenise

    tc.assertEqual(tokenise(b"(;B[ah][]C[a\xa3b])")[0],
                   [('D', b'('),
                    ('D', b';'),
                    ('I', b'B'),
                    ('V', b'ah'),
                    ('V', b''),
                    ('I', b'C'),
                    ('V', b'a\xa3b'),
                    ('D', b')')])

    def check_complete(bb, *args):
        tokens, tail_index = tokenise(bb, *args)
        tc.assertEqual(tail_index, len(bb))
        return len(tokens)

    def check_incomplete(bb, *args):
        tokens, tail_index = tokenise(bb, *args)
        return len(tokens), tail_index

    # check surrounding junk
    tc.assertEqual(check_complete(b""), 0)
    tc.assertEqual(check_complete(b"junk (;B[ah])"), 5)
    tc.assertEqual(check_incomplete(b"junk"), (0, 0))
    tc.assertEqual(check_incomplete(b"junk (B[ah])"), (0, 0))
    tc.assertEqual(check_incomplete(b"(;B[ah]) junk"), (5, 8))

    # check paren-balance count
    tc.assertEqual(check_incomplete(b"(; ))(([ag]B C[ah])"), (3, 4))
    tc.assertEqual(check_incomplete(b"(;( )) (;)"), (5, 6))
    tc.assertEqual(check_incomplete(b"(;(()())) (;)"), (9, 9))

    # check start_position
    tc.assertEqual(check_complete(b"(; ))(;B[ah])", 4), 5)
    tc.assertEqual(check_complete(b"(; ))junk (;B[ah])", 4), 5)

    tc.assertEqual(check_complete(b"(;XX[abc][def]KO[];B[bc])"), 11)
    tc.assertEqual(check_complete(b"( ;XX[abc][def]KO[];B[bc])"), 11)
    tc.assertEqual(check_complete(b"(; XX[abc][def]KO[];B[bc])"), 11)
    tc.assertEqual(check_complete(b"(;XX [abc][def]KO[];B[bc])"), 11)
    tc.assertEqual(check_complete(b"(;XX[abc] [def]KO[];B[bc])"), 11)
    tc.assertEqual(check_complete(b"(;XX[abc][def] KO[];B[bc])"), 11)
    tc.assertEqual(check_complete(b"(;XX[abc][def]KO [];B[bc])"), 11)
    tc.assertEqual(check_complete(b"(;XX[abc][def]KO[] ;B[bc])"), 11)
    tc.assertEqual(check_complete(b"(;XX[abc][def]KO[]; B[bc])"), 11)
    tc.assertEqual(check_complete(b"(;XX[abc][def]KO[];B [bc])"), 11)
    tc.assertEqual(check_complete(b"(;XX[abc][def]KO[];B[bc] )"), 11)

    tc.assertEqual(check_complete(b"( ;\nB\t[ah]\f[ef]\v)"), 6)
    tc.assertEqual(check_complete(b"(;[Ran\xc2\xa3dom :\nstu@ff][ef]"), 4)
    tc.assertEqual(check_complete(b"(;[ah)])"), 4)

    # check PropIdent rule
    tc.assertEqual(check_complete(b"(;" + (8*b"X")), 3)
    tc.assertEqual(check_complete(b"(;" + (9*b"X")), 3)
    tc.assertEqual(check_complete(b"(;" + (64*b"X")), 3)
    tc.assertEqual(check_complete(b"(;" + (65*b"X")), 4)

    tc.assertEqual(check_incomplete(b"(;B[ag"), (3, 3))
    tc.assertEqual(check_incomplete(b"(;B[ag)"), (3, 3))
    tc.assertEqual(check_incomplete(b"(;+B[ag])"), (2, 2))
    tc.assertEqual(check_incomplete(b"(;B+[ag])"), (3, 3))
    tc.assertEqual(check_incomplete(b"(;B[ag]+)"), (4, 7))

    tc.assertEqual(check_complete(br"(;[ab \] cd][ef]"), 4)
    tc.assertEqual(check_complete(br"(;[ab \] cd\\][ef]"), 4)
    tc.assertEqual(check_complete(br"(;[ab \] cd\\\\][ef]"), 4)
    tc.assertEqual(check_complete(br"(;[ab \] \\\] cd][ef]"), 4)
    tc.assertEqual(check_incomplete(br"(;B[ag\])"), (3, 3))
    tc.assertEqual(check_incomplete(br"(;B[ag\\\])"), (3, 3))

def test_tokeniser_lower_case_propidents(tc):
    tokenise = sgf_grammar.tokenise

    tc.assertEqual(tokenise(b"(;AddBlack[ag])")[0],
                   [('D', b'('),
                    ('D', b';'),
                    ('I', b'AB'),
                    ('V', b'ag'),
                    ('D', b')')])

def test_parser_structure(tc):
    parse_sgf_game = sgf_grammar.parse_sgf_game

    def shape(bb):
        coarse_game = parse_sgf_game(bb)
        return len(coarse_game.sequence), len(coarse_game.children)

    tc.assertEqual(shape(b"(;C[abc]KO[];B[bc])"), (2, 0))
    tc.assertEqual(shape(b"initial junk (;C[abc]KO[];B[bc])"), (2, 0))
    tc.assertEqual(shape(b"(;C[abc]KO[];B[bc]) final junk"), (2, 0))
    tc.assertEqual(shape(b"(;C[abc]KO[];B[bc]) (;B[ag])"), (2, 0))

    tc.assertRaisesRegex(ValueError, "no SGF data found",
                         parse_sgf_game, b"")
    tc.assertRaisesRegex(ValueError, "no SGF data found",
                         parse_sgf_game, b"junk")
    tc.assertRaisesRegex(ValueError, "no SGF data found",
                         parse_sgf_game, b"()")
    tc.assertRaisesRegex(ValueError, "no SGF data found",
                         parse_sgf_game, b"(B[ag])")
    tc.assertRaisesRegex(ValueError, "no SGF data found",
                         parse_sgf_game, b"B[ag]")
    tc.assertRaisesRegex(ValueError, "no SGF data found",
                         parse_sgf_game, b"[ag]")

    tc.assertEqual(shape(b"(;C[abc]AB[ab][bc];B[bc])"), (2, 0))
    tc.assertEqual(shape(b"(;C[abc] AB[ab]\n[bc]\t;B[bc])"), (2, 0))
    tc.assertEqual(shape(b"(;C[abc]KO[];;B[bc])"), (3, 0))
    tc.assertEqual(shape(b"(;)"), (1, 0))

    tc.assertRaisesRegex(ValueError, "property with no values",
                         parse_sgf_game, b"(;B)")
    tc.assertRaisesRegex(ValueError, "unexpected value",
                         parse_sgf_game, b"(;[ag])")
    tc.assertRaisesRegex(ValueError, "unexpected value",
                         parse_sgf_game, b"(;[ag][ah])")
    tc.assertRaisesRegex(ValueError, "unexpected value",
                         parse_sgf_game, b"(;[B][ag])")
    tc.assertRaisesRegex(ValueError, "unexpected end of SGF data",
                         parse_sgf_game, b"(;B[ag]")
    tc.assertRaisesRegex(ValueError, "unexpected end of SGF data",
                         parse_sgf_game, b"(;B[ag][)]")
    tc.assertRaisesRegex(ValueError, "property with no values",
                         parse_sgf_game, b"(;B;W[ah])")
    tc.assertRaisesRegex(ValueError, "unexpected value",
                         parse_sgf_game, b"(;B[ag](;[ah]))")
    tc.assertRaisesRegex(ValueError, "property with no values",
                         parse_sgf_game, b"(;B W[ag])")

def test_parser_tree_structure(tc):
    parse_sgf_game = sgf_grammar.parse_sgf_game

    def shape(bb):
        coarse_game = parse_sgf_game(bb)
        return len(coarse_game.sequence), len(coarse_game.children)

    tc.assertEqual(shape(b"(;C[abc]AB[ab](;B[bc]))"), (1, 1))
    tc.assertEqual(shape(b"(;C[abc]AB[ab](;B[bc])))"), (1, 1))
    tc.assertEqual(shape(b"(;C[abc]AB[ab](;B[bc])(;B[bd]))"), (1, 2))

    def shapetree(bb):
        def _shapetree(coarse_game):
            return (
                len(coarse_game.sequence),
                [_shapetree(pg) for pg in coarse_game.children])
        return _shapetree(parse_sgf_game(bb))

    tc.assertEqual(shapetree(b"(;C[abc]AB[ab](;B[bc])))"),
                   (1, [(1, [])])
                   )
    tc.assertEqual(shapetree(b"(;C[abc]AB[ab](;B[bc]))))"),
                   (1, [(1, [])])
                   )
    tc.assertEqual(shapetree(b"(;C[abc]AB[ab](;B[bc])(;B[bd])))"),
                   (1, [(1, []), (1, [])])
                   )
    tc.assertEqual(shapetree(b"""
        (;C[abc]AB[ab];C[];C[]
          (;B[bc])
          (;B[bd];W[ca] (;B[da])(;B[db];W[ea]) )
        )"""),
        (3, [
            (1, []),
            (2, [(1, []), (2, [])])
        ])
    )

    tc.assertRaisesRegex(ValueError, "unexpected end of SGF data",
                         parse_sgf_game, b"(;B[ag];W[ah](;B[ai])")
    tc.assertRaisesRegex(ValueError, "empty sequence",
                         parse_sgf_game, b"(;B[ag];())")
    tc.assertRaisesRegex(ValueError, "empty sequence",
                         parse_sgf_game, b"(;B[ag]())")
    tc.assertRaisesRegex(ValueError, "empty sequence",
                         parse_sgf_game, b"(;B[ag]((;W[ah])(;W[ai]))")
    tc.assertRaisesRegex(ValueError, "unexpected node",
                         parse_sgf_game, b"(;B[ag];W[ah](;B[ai]);W[bd])")
    tc.assertRaisesRegex(ValueError, "property value outside a node",
                         parse_sgf_game, b"(;B[ag];(W[ah];B[ai]))")
    tc.assertRaisesRegex(ValueError, "property value outside a node",
                         parse_sgf_game, b"(;B[ag](;W[ah];)B[ai])")
    tc.assertRaisesRegex(ValueError, "property value outside a node",
                         parse_sgf_game, b"(;B[ag](;W[ah])(B[ai]))")

def test_parser_properties(tc):
    parse_sgf_game = sgf_grammar.parse_sgf_game

    def props(bb):
        coarse_game = parse_sgf_game(bb)
        return coarse_game.sequence

    tc.assertEqual(props(b"(;C[abc]KO[]AB[ai][bh][ee];B[ bc])"),
                   [{'C': [b'abc'], 'KO': [b''], 'AB': [b'ai', b'bh', b'ee']},
                    {'B': [b' bc']}])

    tc.assertEqual(props(br"(;C[ab \] \) cd\\])"),
                   [{'C': [br"ab \] \) cd\\"]}])

    tc.assertEqual(props(b"(;XX[1]YY[2]XX[3]YY[4])"),
                   [{'XX': [b'1', b'3'], 'YY' : [b'2', b'4']}])

def test_parse_sgf_collection(tc):
    parse_sgf_collection = sgf_grammar.parse_sgf_collection

    tc.assertRaisesRegex(ValueError, "no SGF data found",
                         parse_sgf_collection, b"")
    tc.assertRaisesRegex(ValueError, "no SGF data found",
                         parse_sgf_collection, b"()")

    games = parse_sgf_collection(b"(;C[abc]AB[ab];X[];X[](;B[bc]))")
    tc.assertEqual(len(games), 1)
    tc.assertEqual(len(games[0].sequence), 3)

    games = parse_sgf_collection(b"(;X[1];X[2];X[3](;B[bc])) (;Y[1];Y[2])")
    tc.assertEqual(len(games), 2)
    tc.assertEqual(len(games[0].sequence), 3)
    tc.assertEqual(len(games[1].sequence), 2)

    games = parse_sgf_collection(
        b"dummy (;X[1];X[2];X[3](;B[bc])) junk (;Y[1];Y[2]) Nonsense")
    tc.assertEqual(len(games), 2)
    tc.assertEqual(len(games[0].sequence), 3)
    tc.assertEqual(len(games[1].sequence), 2)

    games = parse_sgf_collection(
        b"(( (;X[1];X[2];X[3](;B[bc])) ();) (;Y[1];Y[2]) )(Nonsense")
    tc.assertEqual(len(games), 2)
    tc.assertEqual(len(games[0].sequence), 3)
    tc.assertEqual(len(games[1].sequence), 2)

    with tc.assertRaises(ValueError) as ar:
        parse_sgf_collection(
            b"(( (;X[1];X[2];X[3](;B[bc])) ();) (;Y[1];Y[2]")
    tc.assertEqual(str(ar.exception),
                   "error parsing game 1: unexpected end of SGF data")


def test_parse_compose(tc):
    pc = sgf_grammar.parse_compose
    tc.assertEqual(pc(b"word"), (b"word", None))
    tc.assertEqual(pc(b"word:"), (b"word", b""))
    tc.assertEqual(pc(b"word:?"), (b"word", b"?"))
    tc.assertEqual(pc(b"word:123"), (b"word", b"123"))
    tc.assertEqual(pc(b"word:123:456"), (b"word", b"123:456"))
    tc.assertEqual(pc(b":123"), (b"", b"123"))
    tc.assertEqual(pc(br"word\:more"), (br"word\:more", None))
    tc.assertEqual(pc(br"word\:more:?"), (br"word\:more", b"?"))
    tc.assertEqual(pc(br"word\\:more:?"), (b"word\\\\", b"more:?"))
    tc.assertEqual(pc(br"word\\\:more:?"), (br"word\\\:more", b"?"))
    tc.assertEqual(pc(b"word\\\nmore:123"), (b"word\\\nmore", b"123"))

def test_text_value(tc):
    text_value = sgf_grammar.text_value
    tc.assertEqual(text_value(b"abc "), b"abc ")
    tc.assertEqual(text_value(b"ab c"), b"ab c")
    tc.assertEqual(text_value(b"ab\tc"), b"ab c")
    tc.assertEqual(text_value(b"ab \tc"), b"ab  c")
    tc.assertEqual(text_value(b"ab\nc"), b"ab\nc")
    tc.assertEqual(text_value(b"ab\\\nc"), b"abc")
    tc.assertEqual(text_value(b"ab\\\\\nc"), b"ab\\\nc")
    tc.assertEqual(text_value(b"ab\xa0c"), b"ab\xa0c")

    tc.assertEqual(text_value(b"ab\rc"), b"ab\nc")
    tc.assertEqual(text_value(b"ab\r\nc"), b"ab\nc")
    tc.assertEqual(text_value(b"ab\n\rc"), b"ab\nc")
    tc.assertEqual(text_value(b"ab\r\n\r\nc"), b"ab\n\nc")
    tc.assertEqual(text_value(b"ab\r\n\r\n\rc"), b"ab\n\n\nc")
    tc.assertEqual(text_value(b"ab\\\r\nc"), b"abc")
    tc.assertEqual(text_value(b"ab\\\n\nc"), b"ab\nc")

    tc.assertEqual(text_value(b"ab\\\tc"), b"ab c")

    # These can't actually appear as SGF PropValues; anything sane will do
    tc.assertEqual(text_value(b"abc\\"), b"abc")
    tc.assertEqual(text_value(b"abc]"), b"abc]")

def test_simpletext_value(tc):
    simpletext_value = sgf_grammar.simpletext_value
    tc.assertEqual(simpletext_value(b"abc "), b"abc ")
    tc.assertEqual(simpletext_value(b"ab c"), b"ab c")
    tc.assertEqual(simpletext_value(b"ab\tc"), b"ab c")
    tc.assertEqual(simpletext_value(b"ab \tc"), b"ab  c")
    tc.assertEqual(simpletext_value(b"ab\nc"), b"ab c")
    tc.assertEqual(simpletext_value(b"ab\\\nc"), b"abc")
    tc.assertEqual(simpletext_value(b"ab\\\\\nc"), b"ab\\ c")
    tc.assertEqual(simpletext_value(b"ab\xa0c"), b"ab\xa0c")

    tc.assertEqual(simpletext_value(b"ab\rc"), b"ab c")
    tc.assertEqual(simpletext_value(b"ab\r\nc"), b"ab c")
    tc.assertEqual(simpletext_value(b"ab\n\rc"), b"ab c")
    tc.assertEqual(simpletext_value(b"ab\r\n\r\nc"), b"ab  c")
    tc.assertEqual(simpletext_value(b"ab\r\n\r\n\rc"), b"ab   c")
    tc.assertEqual(simpletext_value(b"ab\\\r\nc"), b"abc")
    tc.assertEqual(simpletext_value(b"ab\\\n\nc"), b"ab c")

    tc.assertEqual(simpletext_value(b"ab\\\tc"), b"ab c")

    # These can't actually appear as SGF PropValues; anything sane will do
    tc.assertEqual(simpletext_value(b"abc\\"), b"abc")
    tc.assertEqual(simpletext_value(b"abc]"), b"abc]")

def test_escape_text(tc):
    tc.assertEqual(sgf_grammar.escape_text(b"abc"), b"abc")
    tc.assertEqual(sgf_grammar.escape_text(br"a\bc"), br"a\\bc")
    tc.assertEqual(sgf_grammar.escape_text(br"ab[c]"), br"ab[c\]")
    tc.assertEqual(sgf_grammar.escape_text(br"a\]bc"), br"a\\\]bc")

def test_text_roundtrip(tc):
    def roundtrip(bb):
        return sgf_grammar.text_value(sgf_grammar.escape_text(bb))
    tc.assertEqual(roundtrip(br"abc"), br"abc")
    tc.assertEqual(roundtrip(br"a\bc"), br"a\bc")
    tc.assertEqual(roundtrip(b"abc\\"), b"abc\\")
    tc.assertEqual(roundtrip(b"ab]c"), b"ab]c")
    tc.assertEqual(roundtrip(b"abc]"), b"abc]")
    tc.assertEqual(roundtrip(br"abc\]"), br"abc\]")
    tc.assertEqual(roundtrip(b"ab\nc"), b"ab\nc")
    tc.assertEqual(roundtrip(b"ab\n  c"), b"ab\n  c")

    tc.assertEqual(roundtrip(b"ab\tc"), b"ab c")
    tc.assertEqual(roundtrip(b"ab\r\nc\n"), b"ab\nc\n")

def test_serialise_game_tree(tc):
    serialised = (b"(;AB[aa][ab][ac]C[comment \xa3];W[ab];C[];C[]"
                  b"(;B[bc])(;B[bd];W[ca](;B[da])(;B[db];\n"
                  b"W[ea])))\n")
    coarse_game = sgf_grammar.parse_sgf_game(serialised)
    tc.assertEqual(sgf_grammar.serialise_game_tree(coarse_game), serialised)
    tc.assertEqual(sgf_grammar.serialise_game_tree(coarse_game, wrap=None),
                   serialised.replace(b"\n", b"")+b"\n")

def test_parse_bytearray(tc):
    # We document that these functions accept a "bytes-like object"
    bb = b'(;C[abc]AB[ab](;B[bc])(;B[bd])))'
    cg1 = sgf_grammar.parse_sgf_game(bb)
    cg2 = sgf_grammar.parse_sgf_game(bytearray(bb))
    tc.assertEqual(sgf_grammar.serialise_game_tree(cg1),
                   sgf_grammar.serialise_game_tree(cg2))

