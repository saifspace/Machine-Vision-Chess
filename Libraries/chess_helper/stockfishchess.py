from pystockfish import *

engine = Engine()
engine.newgame()

def set_fen(fen):
	print(fen)
	engine.setfenposition(fen)

def best_move():
	try:
		return engine.bestmove()['move']
	except:
		return "Check Chessboard"
