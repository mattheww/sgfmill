"""Show the position from an SGF file.

This demonstrates the sgf and ascii_boards modules.

"""

import sys
from optparse import OptionParser

from sgfmill import ascii_boards
from sgfmill import sgf
from sgfmill import sgf_moves

def show_sgf_file(pathname, move_number):
    f = open(pathname, "rb")
    sgf_src = f.read()
    f.close()
    try:
        sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
    except ValueError:
        raise Exception("bad sgf file")

    try:
        board, plays = sgf_moves.get_setup_and_moves(sgf_game)
    except ValueError as e:
        raise Exception(str(e))
    if move_number is not None:
        move_number = max(0, move_number-1)
        plays = plays[:move_number]

    for colour, move in plays:
        if move is None:
            continue
        row, col = move
        try:
            board.play(row, col, colour)
        except ValueError:
            raise Exception("illegal move in sgf file")

    print(ascii_boards.render_board(board))
    print()

_description = """\
Show the position from an SGF file. If a move number is specified, the position
before that move is shown (this is to match the behaviour of GTP loadsgf).
"""

def main(argv):
    parser = OptionParser(usage="%prog <filename> [move number]",
                          description=_description)
    opts, args = parser.parse_args(argv)
    if not args:
        parser.error("not enough arguments")
    pathname = args[0]
    if len(args) > 2:
        parser.error("too many arguments")
    if len(args) == 2:
        try:
            move_number = int(args[1])
        except ValueError:
            parser.error("invalid integer value: %s" % args[1])
    else:
        move_number = None
    try:
        show_sgf_file(pathname, move_number)
    except Exception as e:
        print("show_sgf:", str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])

