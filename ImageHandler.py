from Libraries.machine_learning.label_image import predict_label
import Libraries.image_slicer.image_slicer.main as image_slicer
from ColourDetector import ColourDetector
import cv2
import os


class ImageHandler:
	"""
	This class handles all operations on the image e.g. capture image, save image, crop/slice image,
	chess block iterations etc.
	"""

	def __init__(self):

		self.block_intervals = [8, 16, 24, 32, 40, 48, 56] # intervals for block switch points

		self.blocks = [
			'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
			'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
			'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
			'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
			'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
			'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
			'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
			'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']

		self.reverse_blocks = [
			'a8', 'a7', 'a6', 'a5', 'a4', 'a3', 'a2', 'a1',
			'b8', 'b7', 'b6', 'b5', 'b4', 'b3', 'b2', 'b1',
			'c8', 'c7', 'c6', 'c5', 'c4', 'c3', 'c2', 'c1',
			'd8', 'd7', 'd6', 'd5', 'd4', 'd3', 'd2', 'd1',
			'e8', 'e7', 'e6', 'e5', 'e4', 'e3', 'e2', 'e1',
			'f8', 'f7', 'f6', 'f5', 'f4', 'f3', 'f2', 'f1',
			'g8', 'g7', 'g6', 'g5', 'g4', 'g3', 'g2', 'g1',
			'h8', 'h7', 'h6', 'h5', 'h4', 'h3', 'h2', 'h1']

		self.crop_thresholds = []
		self.pointers = []

		self.block_id_threshold_dictionary = {}
		self.block_thresholds = {}

		self.second_square_values = {}

		self.captured_image_path_win = os.getcwd() + '\Resources\CapturedImage\\board.png'

		self.captured_image = ''
		self.cropped_image = ''

		self.exit = False
		self.crop_x_value = 0
		self.crop_y_value = 0

	def capture_image(self):
		"""
		This method performs a still capture from a video stream and saves the image
		onto disk on a given absolute path.

		Returns:
			Will return nothing, thus None is returned by default.
		"""
		print('Video Stream Loaded.')

		video_cap = cv2.VideoCapture(0)
		video_cap.set(3,640)
		video_cap.set(4,480)

		while True:
			_, feed = video_cap.read()
			cv2.namedWindow('FEED')
			cv2.imshow('FEED', feed)

			if len(self.block_thresholds) == 64:
				i = 1
				for b in self.blocks:
					cv2.rectangle(feed, (self.block_thresholds[i][0] + self.crop_x_value, self.block_thresholds[i][1] + self.crop_y_value), (self.block_thresholds[i][2] + self.crop_x_value, self.block_thresholds[i][3] + self.crop_y_value), (255,255,255),1)
					i = i + 1

			cv2.imshow("FEED", feed) # update the feed here with drawn thresholds set.

			if cv2.waitKey(33) == ord('c') or self.exit == True:
				cv2.imwrite(self.captured_image_path_win, feed)
				print('Image Captured.')
				break

		self.set_exit_false()
		cv2.destroyAllWindows()
		video_cap.release()

	def load_captured_image(self, flag=''):
		"""
		The method loads the image from the given paths as a numpy array and assigns it to the
		class attribute named captured_image.

		Returns:
			Nothing, None.
		"""

		path = self.captured_image_path_win

		self.captured_image = cv2.imread(path)

		print("Image Loaded.")

	def mouse_click_crop(self, event, x, y, flags, param):
		"""
		This is a method that will be called every time there is a mouse click during the threshold
		setting (Region of Interest) step. All thresholds that are gathered are stored in the crop_thresholds lists.

		Returns:
			Nothing, None.
		"""

		if event == cv2.EVENT_LBUTTONDOWN:
			self.pointers = [(x,y)]
		elif event == cv2.EVENT_LBUTTONUP:
			self.pointers.append((x,y))
			self.crop_thresholds.append(self.pointers[0])
			self.crop_thresholds.append(self.pointers[1])
			cv2.rectangle(self.captured_image, self.pointers[0], self.pointers[1], (0,0,0),1)
			cv2.imshow('image', self.captured_image)


	def set_thresholds_manually(self, thresholds_arr):
		self.crop_thresholds = thresholds_arr

	def set_thresholds(self):
		"""
		This method invokes the mouse_click_crop_function to setup the thresholds.
		The method exits when 'q' keypress is detected. Press twice due to waitKey.

		Returns:
			Nothing, None.
		"""

		cv2.namedWindow('image')
		cv2.imshow('image', self.captured_image)

		while True:
			cv2.setMouseCallback('image', self.mouse_click_crop)
			cv2.waitKey(0)
			if cv2.waitKey() == ord('q'):
				print('Thresholds Set.')
				break
		cv2.destroyAllWindows()

	def crop_and_save(self):
		"""
		This method crops everything in the image except the region of interest.

		Returns:
		 	Nothing, None.
		"""

		tuple_one = self.crop_thresholds[0]
		tuple_two = self.crop_thresholds[1]

		win_path = os.getcwd() + '\Resources\CapturedImage\cropped_board.png'

		x1 = tuple_one[0]
		x2 = tuple_two[0]
		y1 = tuple_one[1]
		y2 = tuple_two[1]

		self.crop_x_value = x1
		self.crop_y_value = y1

		self.cropped_image = self.captured_image[y1:y2, x1:x2]
		cv2.imwrite(win_path, self.cropped_image)

	def iterate_blocks(self):
		"""
		This method applies colour detection classification to every block/square.

		Returns:
		 	Returns a dictionary contain the block/square information i.e. what piece it contains.
		"""

		piece_square_info = {}
		colour_detection = ColourDetector()

		print('Detecting Pieces.')

		for b in self.reverse_blocks:

			print(b)

			threshold = self.block_id_threshold_dictionary[b]

			x1 = threshold[0] + self.crop_x_value
			x2 = threshold[2] + self.crop_x_value
			y1 = threshold[1] + self.crop_y_value
			y2 = threshold[3] + self.crop_y_value

			win_path = os.getcwd() + '\Resources\CapturedImage\\board.png'

			cropped_image = cv2.imread(win_path)
			cropped_image_hsv = cv2.cvtColor(cropped_image[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)

			# Colour Detection method applied here: Mask, Closest colour threshold or Image Classification.

			piece = colour_detection.apply_masks_and_return_dominant(cropped_image_hsv)

			if(piece[0] != 'None'):
				piece_square_info[b] = colour_detection.get_piece_dictionary_from_enum(piece[0]) # a dictionary mapping block id to piece info dictionary.
		return piece_square_info

	def ml_iterate_blocks(self):
		"""
		This method applies machine learning classification to every block/square.

		Returns:
		 	Nothing, None.
		"""

		piece_square_info = {}
		colour_detection = ColourDetector()

		win_path = os.getcwd() + "\Resources\CapturedImage\piece.png"

		print ('Detecting Pieces.')

		for b in self.reverse_blocks:

			threshold = self.block_id_threshold_dictionary[b]

			x1 = threshold[0] + self.crop_x_value
			x2 = threshold[2] + self.crop_x_value
			y1 = threshold[1] + self.crop_y_value
			y2 = threshold[3] + self.crop_y_value

			cropped_image = cv2.imread(os.getcwd() + '\Resources\CapturedImage\\board.png')

			cv2.imwrite(win_path, cropped_image[y1:y2, x1:x2])
			top_two_predictions = predict_label(win_path)
			piece_one = top_two_predictions[0].replace(" ", "")
			piece_two = top_two_predictions[1].replace(" ", "")

			print("block/square: ", b,  " prediction-1: ", piece_one, " prediction-2: " , piece_two)

			if(piece_two == "empty"):
				self.second_square_values[b] = "empty"
			else:
				self.second_square_values[b] = colour_detection.get_piece_dictionary_from_enum(piece_two)

			if(piece_one != "empty"):
				piece_square_info[b] = colour_detection.get_piece_dictionary_from_enum(piece_one)
		return piece_square_info


	def slice_image(self):
		"""
		This method acquires the pair of coordinates for each block/square of the chessboard.

		Returns:
		 	Nothing, None.
		"""

		win_path = os.getcwd() + '\Resources\CapturedImage\\cropped_board.png'
		self.block_thresholds = image_slicer.slice(win_path, 64)

	def create_block_id_threshold_dictionary(self):
		"""
		Algorithm implementation to create a mapping between block/square id to its pair of coordinates
		that are set using the slice_image method.

		Returns:
		 	Nothing, None.
		"""

		i = 1
		for count, b in enumerate(self.reverse_blocks):

			if count in self.block_intervals:
				i = (self.block_intervals.index(count)) + 2

			self.block_id_threshold_dictionary[b] = self.block_thresholds[i]

			i+=8

	def set_exit_true(self):
		self.exit = True

	def set_exit_false(self):
		self.exit = False

	def get_crop_thresholds(self):
		return self.crop_thresholds

	def get_second_square_value_dict(self):
		return self.second_square_values

	def close_all_windows(self):
		cv2.destroyAllWindows()