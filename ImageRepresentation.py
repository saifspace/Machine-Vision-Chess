import image_slicer
import os
from PIL import Image



class ChessboardImage:

	def __init__(self):

		self.reverse_blocks = [
			'a8', 'a7', 'a6', 'a5', 'a4', 'a3', 'a2', 'a1',
			'b8', 'b7', 'b6', 'b5', 'b4', 'b3', 'b2', 'b1',
			'c8', 'c7', 'c6', 'c5', 'c4', 'c3', 'c2', 'c1',
			'd8', 'd7', 'd6', 'd5', 'd4', 'd3', 'd2', 'd1',
			'e8', 'e7', 'e6', 'e5', 'e4', 'e3', 'e2', 'e1',
			'f8', 'f7', 'f6', 'f5', 'f4', 'f3', 'f2', 'f1',
			'g8', 'g7', 'g6', 'g5', 'g4', 'g3', 'g2', 'g1',
			'h8', 'h7', 'h6', 'h5', 'h4', 'h3', 'h2', 'h1']

		self.block_intervals = [8, 16, 24, 32, 40, 48, 56]

		self.block_id_threshold_dictionary = {}
		self.block_thresholds = {}

		self.board_image_path = ''
		self.board_image = Image.open(self.board_image_path)
		self.piece_image = Image.open('')




	def set_block_thresholds(self):
		self.block_thresholds = image_slicer.slice(self.board_image_path, 64)

	def create_block_id_threshold_dictionary(self):
		i = 1
		for count, b in enumerate(self.reverse_blocks):

			# print b
			if count in self.block_intervals:
				i = (self.block_intervals.index(count)) + 2

			# print i
			self.block_id_threshold_dictionary[b] = self.block_thresholds[i]

			i+=8

	def put_piece(self):
		return ''



# (x,y), where x = +65 , y = +65

# 'a5':(12, 160), 'a4':(12, 210), 'a3':(12, 260), 'a2':(12, 310), 'a1':(12, 360)

block_dict = {
	'a8':(12, 10), 'a7':(12, 75), 'a6':(12, 140-5), 'a5':(12, 205-5), 'a4':(12, 270-10), 'a3':(12, 335-10), 'a2':(12, 400-15), 'a1':(12, 465-15),
	'b8':(77, 10), 'b7':(77, 75), 'b6':(77, 140-5), 'b5':(77, 205-5), 'b4':(77, 270-10), 'b3':(77, 335-10), 'b2':(77, 400-15), 'b1':(77, 465-15),
	'c8':(142, 10), 'c7':(142, 75), 'c6':(142, 140-5), 'c5':(142, 205-5), 'c4':(142, 270-10), 'c3':(142, 335-10), 'c2':(142, 400-15), 'c1':(142, 465-15),
	'd8':(207-5, 10), 'd7':(207-5, 75), 'd6':(207-5, 140-5), 'd5':(207-5, 205-5), 'd4':(207-5, 270-10), 'd3':(207-5, 335-10), 'd2':(207-5, 400-15), 'd1':(207-5, 465-15),
	'e8':(272-5, 10), 'e7':(272-5, 75), 'e6':(272-5, 140-5), 'e5':(272-5, 205-5), 'e4':(272-5, 270-10), 'e3':(272-5, 335-10), 'e2':(272-5, 400-15), 'e1':(272-5, 465-15),
	'f8':(337-10, 10), 'f7':(337-10, 75), 'f6':(337-10, 140-5), 'f5':(337-10, 205-5), 'f4':(337-10, 270-10), 'f3':(337-10, 335-10), 'f2':(337-10, 400-15), 'f1':(337-10, 465-15),
	'g8':(402-10, 10), 'g7':(402-10, 75), 'g6':(402-10, 140-5), 'g5':(402-10, 205-5), 'g4':(402-10, 270-10), 'g3':(402-10, 335-10), 'g2':(402-10, 400-15), 'g1':(402-10, 465-15),
	'h8':(467-15, 10), 'h7':(467-15, 75), 'h6':(467-15, 140-5), 'h5':(467-15, 205-5), 'h4':(467-15, 270-10), 'h3':(467-15, 335-10), 'h2':(467-15, 400-15), 'h1':(467-15, 465-15)

			  }

pieces_paths = {
	'w_p': os.getcwd() + '/Resources/pieces/w_pawn.png', 'w_n': os.getcwd() +'/Resources/pieces/w_knight.png', 'w_b':os.getcwd() + '/Resources/pieces/w_bishop.png',
	'w_r': os.getcwd() + '/Resources/pieces/w_rook.png', 'w_q': os.getcwd() +'/Resources/pieces/w_queen.png', 'w_k': os.getcwd() +'/Resources/pieces/w_king.png',
	'b_p': os.getcwd() + '/Resources/pieces/b_pawn.png', 'b_n': os.getcwd() +'/Resources/pieces/b_knight.png', 'b_b':os.getcwd() + '/Resources/pieces/b_bishop.png',
	'b_r': os.getcwd() + '/Resources/pieces/b_rook.png', 'b_q': os.getcwd() +'/Resources/pieces/b_queen.png', 'b_k': os.getcwd() +'/Resources/pieces/b_king.png'
}


def create_image(setup_dict):
	background = Image.open(os.getcwd() + '/Resources/chessboard2.png')
	for key, value in setup_dict.items():
		print(key)
		print(value)
		piece = value[1] + '_' + value[0]
		position = block_dict[key]
		# print key
		# print value
		# print position
		foreground = Image.open(pieces_paths[piece])
		background.paste(foreground, position, foreground)
	background.save(os.getcwd() + '/Resources/' + 'modifiedChessboard.png')