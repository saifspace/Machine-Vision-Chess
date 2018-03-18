from enum import Enum
from numpy import ndarray
test_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

DEFAULT_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


BLACK = 'b'
WHITE = 'w'

EMPTY = -1

PAWN = 'p'
KNIGHT = 'n'
BISHOP = 'b'
ROOK = 'r'
QUEEN = 'q'
KING = 'k'

SYMBOLS = 'pnbrqkPNBRQK'

SQUARES = {
    'a8': 0, 'b8': 1, 'c8': 2, 'd8': 3, 'e8': 4, 'f8': 5, 'g8': 6, 'h8': 7,
    'a7': 16, 'b7': 17, 'c7': 18, 'd7': 19, 'e7': 20, 'f7': 21, 'g7': 22, 'h7': 23,
    'a6': 32, 'b6': 33, 'c6': 34, 'd6': 35, 'e6': 36, 'f6': 37, 'g6':  38, 'h6': 39,
    'a5': 48, 'b5': 49, 'c5': 50, 'd5': 51, 'e5': 52, 'f5': 53, 'g5':  54, 'h5': 55,
    'a4': 64, 'b4': 65, 'c4': 66, 'd4': 67, 'e4': 68, 'f4': 69, 'g4':  70, 'h4': 71,
    'a3': 80, 'b3': 81, 'c3': 82, 'd3': 83, 'e3': 84, 'f3': 85, 'g3':  86, 'h3': 87,
    'a2': 96, 'b2': 97, 'c2': 98, 'd2': 99, 'e2': 100,'f2': 101,'g2': 102, 'h2': 103,
    'a1': 112,'b1': 113,'c1': 114,'d1':115, 'e1': 116,'f1': 117,'g1': 118, 'h1': 119
  }

BITS = {
    'NORMAL' : 1,
    'CAPTURE' : 2,
    'BIG_PAWN' : 4,
    'EP_CAPTURE' : 8,
    'PROMOTION' : 16,
    'KSIDE_CASTLE' : 32,
    'QSIDE_CASTLE' : 64
}

board = [None] * 128
kings = {'w': EMPTY, 'b': EMPTY}
turn = WHITE
castling = {'w': 0, 'b':0}
ep_square = EMPTY
half_moves = 0
move_number = 1
history = []
header = {}


def load(fen_param):
    global turn
    tokens = fen_param.split(" ")
    # position = tokens[0]
    square = 0

    for i, s in enumerate(tokens):
        for j in range(len(s)):
            piece = s[j]

            if(piece == '/'):
                square += 8
            elif piece.isdigit():
                square+= int(piece)
            else:
                color = WHITE if piece < 'a' else BLACK


                temp_dict = put({'type': piece.lower(), 'color': color}, algebraic(square))


                square += 1

    turn = tokens[1];

    if(tokens[2].find('K') > -1):
        castling['w'] = castling['w'] | BITS['KSIDE_CASTLE']

    if(tokens[2].find('Q') > -1):
        castling['w'] = castling['w'] | BITS['QSIDE_CASTLE']

    if(tokens[2].find('k') > -1):
        castling['b'] = castling['b'] | BITS['KSIDE_CASTLE']

    if(tokens[2].find('q') > -1):
        castling['b'] = castling['b'] | BITS['QSIDE_CASTLE']

    global ep_square
    global half_moves
    global  move_number

    ep_square = EMPTY if (tokens[3] == '-') else SQUARES[tokens[3]]
    half_moves = int(tokens[4], 10)
    move_number = int(tokens[5], 10)

    update_setup(generate_fen())

def algebraic(i):
    f = file(i)
    r = rank(i)
    return 'abcdefgh'[f:f+1] + '87654321'[r:r+1]

def rank(i):
    return i >> 4
def file(i):
    return i & 15

def generate_fen():
    empty = 0
    fen = ''

    i = SQUARES['a8']
    j = SQUARES['h1']

    while(i <= j):
        if board[i] == None:
            empty += 1
        else:
            if empty > 0:
                fen += str(empty)
                empty = 0
            color = board[i]['color']
            piece = board[i]['type']
            fen += piece.upper() if (color == WHITE) else piece.lower()

        if ((i + 1) & 0x88):
            if empty > 0:
                fen += str(empty)

            if i != SQUARES['h1']:
                fen += '/'

            empty = 0
            i += 8

        i += 1

    cflags = ''
    if castling[WHITE] & BITS['KSIDE_CASTLE']:
        cflags += 'K'
    if castling[WHITE] & BITS['QSIDE_CASTLE']:
        cflags += 'Q'
    if castling[BLACK] & BITS['KSIDE_CASTLE']:
        cflags += 'k'
    if castling[BLACK] & BITS['QSIDE_CASTLE']:
        cflags += 'q'

    cflags = cflags or '-'
    epflags = '-' if (ep_square == EMPTY) else algebraic(ep_square)
    info_arr = [fen, turn, cflags, epflags, str(half_moves), str(move_number)]
    joined_string = ' '.join(info_arr)

    return joined_string

def update_setup(fen):
    global history
    if len(history) > 0:
        return

    if fen != DEFAULT_POSITION:
        header['SetUp'] = '1'
        header['FEN'] = fen
    else:
        del header['SetUp']
        del header['FEN']

def ascii():
    s = '   +------------------------+\n'

    i = SQUARES['a8']
    j = SQUARES['h1']

    while (i <= j):

        if(file(i) == 0):
            s += ' ' + '87654321' [rank(i)] + ' |'

        if (board[i] == None):
            s += ' . '
        else:
            piece = board[i]['type']
            color = board[i]['color']
            symbol = piece.upper() if(color == WHITE) else piece.lower()
            s += ' ' + symbol + ' '

        if ((i + 1) & 0x88):
            s += '|\n'
            i += 8
        i += 1

    s += '   +------------------------+\n'
    s += '     a  b  c  d  e  f  g  h\n'

    return s

def put(piece, square):
    print piece, ' ', square
    global board


    if (not('type' in piece and 'color' in piece)):
        print 'a'
        return False

    if (SYMBOLS.find(str(piece['type']).lower()) == -1):
        print 'b'
        return False

    if (not(square in SQUARES)):
        print 'c'
        return False

    sq = SQUARES[square]

    if (piece['type'] == KING and not( kings[piece['color']] == EMPTY or kings[piece['color']] == sq) ):
        print 'd'
        return False

    board[sq] = {'type': piece['type'], 'color': piece['color']}

    if (piece['type'] == KING):
        kings[piece['color']] = sq

    update_setup(generate_fen())

    print 'e'
    return True


def remove(square):
    global board
    global kings

    piece = get(square)
    board[SQUARES[square]] = None
    if (piece!= None and piece['type'] == KING):
        kings[piece['color']] = EMPTY

    update_setup(generate_fen())

    return piece


def get(square):
    piece = board[SQUARES[square]]
    return {'type': piece['type'], 'color': piece['color']} if (piece != None) else None

def fen():
    return generate_fen()

def get_setup():
    square_ids = [
        'a1','a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
        'b1','b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
        'c1','c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
        'd1','d2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
        'e1','e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
        'f1','f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
        'g1','g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
        'h1','h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8',
        ]
    non_empty_squares = {}
    for s in square_ids:
        piece = board[SQUARES[s]]
        if (piece != None):
            non_empty_squares[s] = (piece['type'], piece['color'])

    return non_empty_squares


# Local tests:

# load('rnbqkbnr/ppppppp1/7p/8/8/1P6/P1PPPPPP/RNBQKBNR w KQkq - 0 1')
# print ascii()
# print(fen())
# print remove('h8')
# print ascii()