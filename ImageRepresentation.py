from PIL import Image
import os

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
	'w_p': os.getcwd() + '\Resources\pieces\w_pawn.png', 'w_n': os.getcwd() + '\Resources\pieces\w_knight.png', 'w_b':os.getcwd() + '\Resources\pieces\w_bishop.png',
	'w_r': os.getcwd() + '\Resources\pieces\w_rook.png', 'w_q': os.getcwd() + '\Resources\pieces\w_queen.png', 'w_k': os.getcwd() + '\Resources\pieces\w_king.png',
	'b_p': os.getcwd() + '\Resources\pieces\\b_pawn.png', 'b_n': os.getcwd() + '\Resources\pieces\\b_knight.png', 'b_b':os.getcwd() + '\Resources\pieces\\b_bishop.png',
	'b_r': os.getcwd() + '\Resources\pieces\\b_rook.png', 'b_q': os.getcwd() + '\Resources\pieces\\b_queen.png', 'b_k': os.getcwd() + '\Resources\pieces\\b_king.png'
}

def create_image(setup_dict):
	"""
	This method creates the image representation of the physical and ASCII generated chessboards.

	Args:
		setup_dict: dictionary containing the setup created using the translated JavaScript chess module.

	Returns:
		Nothing, None.
	"""

	background = Image.open(os.getcwd() + '\Resources\chessboard2.png')
	for key, value in setup_dict.items():
		print(key)
		print(value)
		piece = value[1] + '_' + value[0]
		position = block_dict[key]
		foreground = Image.open(pieces_paths[piece])
		background.paste(foreground, position, foreground)
	background.save(os.getcwd() + '\Resources\\' + 'modifiedChessboard.png')