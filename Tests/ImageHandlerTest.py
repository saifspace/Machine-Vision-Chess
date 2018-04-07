import os
import unittest
from unittest.mock import patch
from ImageHandler import ImageHandler

# NOTE:
# Run each test individually: right-click on test method and click on the run option.
class ImageqHandlerTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.block_thresholds = {1: (0, 0, 77, 78), 2: (77, 0, 154, 78), 3: (154, 0, 231, 78), 4: (231, 0, 308, 78), 5: (308, 0, 385, 78), 6: (385, 0, 462, 78), 7: (462, 0, 539, 78), 8: (539, 0, 616, 78),
								 9: (0, 78, 77, 156), 10: (77, 78, 154, 156), 11: (154, 78, 231, 156), 12: (231, 78, 308, 156), 13: (308, 78, 385, 156), 14: (385, 78, 462, 156), 15: (462, 78, 539, 156),
								 16: (539, 78, 616, 156), 17: (0, 156, 77, 234), 18: (77, 156, 154, 234), 19: (154, 156, 231, 234), 20: (231, 156, 308, 234), 21: (308, 156, 385, 234), 22: (385, 156, 462, 234),
								 23: (462, 156, 539, 234), 24: (539, 156, 616, 234), 25: (0, 234, 77, 312), 26: (77, 234, 154, 312), 27: (154, 234, 231, 312), 28: (231, 234, 308, 312), 29: (308, 234, 385, 312),
								 30: (385, 234, 462, 312), 31: (462, 234, 539, 312), 32: (539, 234, 616, 312), 33: (0, 312, 77, 390), 34: (77, 312, 154, 390), 35: (154, 312, 231, 390), 36: (231, 312, 308, 390),
								 37: (308, 312, 385, 390), 38: (385, 312, 462, 390), 39: (462, 312, 539, 390), 40: (539, 312, 616, 390), 41: (0, 390, 77, 468), 42: (77, 390, 154, 468), 43: (154, 390, 231, 468),
								 44: (231, 390, 308, 468), 45: (308, 390, 385, 468), 46: (385, 390, 462, 468), 47: (462, 390, 539, 468), 48: (539, 390, 616, 468), 49: (0, 468, 77, 546), 50: (77, 468, 154, 546),
								 51: (154, 468, 231, 546), 52: (231, 468, 308, 546), 53: (308, 468, 385, 546), 54: (385, 468, 462, 546), 55: (462, 468, 539, 546), 56: (539, 468, 616, 546), 57: (0, 546, 77, 624),
								 58: (77, 546, 154, 624), 59: (154, 546, 231, 624), 60: (231, 546, 308, 624), 61: (308, 546, 385, 624), 62: (385, 546, 462, 624), 63: (462, 546, 539, 624), 64: (539, 546, 616, 624)}

		self.block_id_threshold_Dictionary = {'f8': (385, 0, 462, 78), 'g5': (462, 234, 539, 312), 'c3': (154, 390, 231, 468), 'f7': (385, 78, 462, 156), 'c5': (154, 234, 231, 312), 'e3': (308, 390, 385, 468),
											  'f4': (385, 312, 462, 390), 'a3': (0, 390, 77, 468), 'h4': (539, 312, 616, 390), 'a7': (0, 78, 77, 156), 'h7': (539, 78, 616, 156), 'e2': (308, 468, 385, 546),
											  'c1': (154, 546, 231, 624), 'b2': (77, 468, 154, 546), 'a4': (0, 312, 77, 390), 'h2': (539, 468, 616, 546), 'a2': (0, 468, 77, 546), 'd2': (231, 468, 308, 546),
											  'd1': (231, 546, 308, 624), 'b6': (77, 156, 154, 234), 'a1': (0, 546, 77, 624), 'd3': (231, 390, 308, 468), 'f3': (385, 390, 462, 468), 'g7': (462, 78, 539, 156),
											  'f6': (385, 156, 462, 234), 'h6': (539, 156, 616, 234), 'b4': (77, 312, 154, 390), 'f2': (385, 468, 462, 546), 'h1': (539, 546, 616, 624), 'a8': (0, 0, 77, 78),
											  'd8': (231, 0, 308, 78), 'd7': (231, 78, 308, 156), 'g2': (462, 468, 539, 546), 'h5': (539, 234, 616, 312), 'd4': (231, 312, 308, 390), 'b1': (77, 546, 154, 624),
											  'a5': (0, 234, 77, 312), 'f1': (385, 546, 462, 624), 'h8': (539, 0, 616, 78), 'e1': (308, 546, 385, 624), 'e5': (308, 234, 385, 312), 'b3': (77, 390, 154, 468),
											  'b5': (77, 234, 154, 312), 'c2': (154, 468, 231, 546), 'd6': (231, 156, 308, 234), 'c6': (154, 156, 231, 234), 'e4': (308, 312, 385, 390), 'c7': (154, 78, 231, 156),
											  'g4': (462, 312, 539, 390), 'c4': (154, 312, 231, 390), 'g3': (462, 390, 539, 468), 'b7': (77, 78, 154, 156), 'g1': (462, 546, 539, 624), 'd5': (231, 234, 308, 312),
											  'e6': (308, 156, 385, 234), 'f5': (385, 234, 462, 312), 'c8': (154, 0, 231, 78), 'g6': (462, 156, 539, 234), 'g8': (462, 0, 539, 78), 'e7': (308, 78, 385, 156),
											  'e8': (308, 0, 385, 78), 'h3': (539, 390, 616, 468), 'a6': (0, 156, 77, 234), 'b8': (77, 0, 154, 78)}

		self.image_handler = ImageHandler()
		self.image_handler.load_captured_image(flag='win')
		self.image_handler.set_thresholds()

	@classmethod
	def tearDownClass(cls):
		os.remove(os.getcwd() + "/Resources/CapturedImage/cropped_board.png")


	def test_load_captured_image(self):

		self.assertNotEqual(len(self.image_handler.captured_image), 0)

	def test_set_thresholds(self):
		self.assertNotEqual(len(self.image_handler.crop_thresholds), 64)

	def test_crop_and_save(self):
		self.image_handler.crop_and_save()
		self.assertTrue(os.path.exists(os.getcwd() + "/Resources/CapturedImage/cropped_board.png"))

	def test_slice_image(self):
		self.image_handler.slice_image()
		self.assertEqual(len(self.image_handler.block_thresholds),64)

	def test_create_block_id_threshold_dictionary(self):
		self.image_handler.block_thresholds = self.block_thresholds
		self.image_handler.create_block_id_threshold_dictionary()
		self.assertEqual(len(self.image_handler.block_id_threshold_dictionary), 64)

	def test_iterate_blocks(self):
		self.image_handler.block_id_threshold_dictionary = self.block_id_threshold_Dictionary
		self.assertTrue(type(self.image_handler.iterate_blocks()) is dict)

	# need to add the CNN to test resources using the same path
	# def test_ml_iterate_blocks(self):
	# 	self.image_handler.block_id_threshold_dictionary = self.block_id_threshold_Dictionary
	# 	self.assertTrue(type(self.image_handler.ml_iterate_blocks()) is dict)

if __name__ == '__main__':
	unittest.main()
