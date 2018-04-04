import unittest
from ColourDetector import ColourDetector
import cv2


class ColourDetectorTest(unittest.TestCase):

	def test_apply_masks_and_return_dominant(self):
		b_pawn = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/b_pawn.png'), cv2.COLOR_BGR2HSV)
		b_rook =  cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/b_rook.png'), cv2.COLOR_BGR2HSV)
		b_knight =  cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/b_knight.png'), cv2.COLOR_BGR2HSV)
		b_bishop =  cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/b_bishop.png'), cv2.COLOR_BGR2HSV)
		b_king = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/b_king.png'), cv2.COLOR_BGR2HSV)
		b_queen = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/b_queen.png'), cv2.COLOR_BGR2HSV)

		w_pawn = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/w_pawn.png'), cv2.COLOR_BGR2HSV)
		w_rook = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/w_rook.png'), cv2.COLOR_BGR2HSV)
		w_knight = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/w_knight.png'), cv2.COLOR_BGR2HSV)
		w_bishop = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/w_bishop.png'), cv2.COLOR_BGR2HSV)
		w_king = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/w_king.png'), cv2.COLOR_BGR2HSV)
		w_queen = cv2.cvtColor(cv2.imread('./Resources/ColourDetectorTest/w_queen.png'), cv2.COLOR_BGR2HSV)

		colour_detector_test = ColourDetector()

		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(b_pawn)[0], "EG")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(b_rook)[0], "VIO")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(b_knight)[0], "YO")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(b_bishop)[0], "HG")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(b_king)[0], "CRIM_RED")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(b_queen)[0], "CB_FLESH")

		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(w_pawn)[0], "SG_CB_GREY")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(w_rook)[0], "GREY")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(w_knight)[0], "MY")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(w_bishop)[0], "OR")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(w_king)[0], "CEROLB")
		self.assertEqual(colour_detector_test.apply_masks_and_return_dominant(w_queen)[0], "PINK")




if __name__ == '__main__':
	unittest.main()
