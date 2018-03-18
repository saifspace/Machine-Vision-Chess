import sys
sys.path.append('/Users/omgitsmotrix/desktop/finalYearProject/preperation/stockfish_integration')

from ImageHandler import ImageHandler
import chess


class MainClass:

	classLevel = 'Class Variable'

	def __init__(self):
		self.test_thresholds = [(429, 616), (502, 693), (427, 539), (501, 611), (429, 458), (504, 531), (430, 382), (504, 453), (430, 303), (505, 376), (431, 231), (504, 299), (435, 151), (505, 224), (430, 70), (505, 147), (507, 616), (579, 694), (508, 536), (580, 611), (508, 458), (581, 532), (508, 382), (582, 453), (509, 303), (582, 376), (509, 226), (582, 300), (509, 152), (582, 225), (510, 69), (583, 148), (585, 616), (658, 694), (585, 539), (658, 611), (585, 460), (656, 528), (587, 382), (658, 454), (583, 305), (659, 377), (585, 228), (657, 300), (588, 152), (659, 223), (582, 73), (660, 144), (664, 616), (737, 698), (660, 538), (736, 615), (662, 459), (736, 533), (661, 383), (736, 455), (662, 303), (736, 375), (662, 228), (738, 297), (664, 153), (737, 223), (667, 68), (736, 142), (741, 617), (818, 696), (741, 538), (819, 603), (741, 462), (815, 531), (739, 383), (816, 447), (741, 304), (813, 378), (740, 226), (814, 300), (738, 151), (818, 224), (740, 72), (815, 141), (821, 618), (899, 696), (819, 540), (898, 613), (819, 460), (894, 533), (818, 381), (893, 456), (820, 304), (894, 374), (817, 228), (894, 299), (817, 150), (892, 223), (820, 68), (895, 141), (900, 620), (983, 699), (898, 540), (976, 613), (896, 461), (977, 534), (895, 384), (974, 455), (896, 304), (974, 375), (897, 226), (972, 297), (892, 149), (975, 221), (897, 69), (972, 145), (981, 623), (1061, 695), (978, 542), (1061, 615), (980, 460), (1059, 536), (974, 383), (1057, 453), (975, 306), (1055, 375), (978, 224), (1054, 300), (976, 147), (1054, 220), (975, 67), (1056, 141)]
		self.image_handler = ImageHandler()
		# print len(self.test_thresholds)


	def main(self):
		# # self.image_handler.capture_image()
		# self.image_handler.load_captured_image(flag='mac_test')
        #
		# self.image_handler.set_thresholds_manually(self.test_thresholds) # image_handler.set_thresholds()
		# # self.image_handler.set_thresholds()
        #
		# self.image_handler.create_block_id_threshold_dictionary()
        #
		# piece_square_info = self.image_handler.iterate_blocks()
        #
		# for s in piece_square_info.keys():
		# 	chess.put(piece_square_info[s], s)
        #
		# print chess.ascii()

		self.image_handler.load_captured_image(flag='mac_test')
		self.image_handler.set_thresholds()

		# self.image_handler.crop_and_save()
		self.image_handler.slice_image()
		self.image_handler.new_create_block_id_threshold_dictionary()
		piece_square_info = self.image_handler.new_iterate_blocks()

		for s in piece_square_info.keys():
			chess.put(piece_square_info[s], s)

		print chess.ascii()
		print chess.fen()





main_obj = MainClass()
main_obj.main()
