from pystockfish import *

deep = Engine()
deep.newgame()

def set_fen(fen):
    print fen
    deep.setfenposition(fen)

def best_move():
    print deep.bestmove()