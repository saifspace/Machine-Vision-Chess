import os
import sys
import unittest
from ImageRepresentation import create_image
sys.path.append(os.getcwd() + '..\..\Libraries\chess_helper')
import chess


class ImageRepresentationTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		chess.load('rnbqkbnr/ppppppp1/7p/8/8/1P6/P1PPPPPP/RNBQKBNR w KQkq - 0 1')
		self.test_setup = chess.get_setup()

	# @classmethod
	# def tearDownClass(cls):
	# 	os.remove(os.getcwd() + "\Resources\modifiedChessboard.png")

	def test_create_image(self):
		create_image(self.test_setup)
		self.assertTrue(os.path.exists(os.getcwd() + "\Resources\modifiedChessboard.png"))


if __name__ == '__main__':
	unittest.main()
