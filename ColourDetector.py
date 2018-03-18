import cv2
import numpy as np
from enum import Enum



class Pieces(Enum):
	"""
	TODO: Add enum docstring 
	"""
	
	SG_CB_GREY = {'type': 'p', 'color': 'w'}
	GREY = {'type': 'r', 'color': 'w'}
	MY = {'type': 'n', 'color': 'w'}
	OR = {'type': 'b', 'color': 'w'}
	CEROLB = {'type': 'k', 'color': 'w'}
	PINK = {'type': 'q', 'color': 'w'}

	EG = {'type': 'p', 'color': 'b'}
	VIO = {'type': 'r', 'color': 'b'}
	YO = {'type': 'n', 'color': 'b'}
	HG = {'type': 'b', 'color': 'b'}
	CRIM_RED = {'type': 'k', 'color': 'b'}
	CB_FLESH = {'type': 'q', 'color': 'b'}


class ColourDetector:

	"""
	This class handles the method of identifying the colour present in a provided block.
	Once a colour is identified it is matched against the piece it represents. 
	"""

	def apply_masks_and_return_dominant(self, image):
		"""
		This method will pass the cropped image received through the various coloured masks,
		then the most significant colour mask will be chosen to decide on the piece type and side
		using the Pieces enum class.
		"""

		pixel_dictionary = {}

		yo_pixels = self.apply_yo_mask(image)
		my_pixels = self.apply_my_mask(image)
		vio_pixels = self.apply_vio_mask(image)
		grey_pixels = self.apply_grey_mask(image)
		pink_pixels = self.apply_pink_mask(image)
		crim_red_pixels = self.apply_crim_red_mask(image)
		hg_pixels = self.apply_hg_mask(image)
		eg_pixels = self.apply_eg_mask(image)
		cb_flesh_pixels = self.apply_cb_flesh_mask(image)
		sg_cb_grey_pixels = self.apply_sg_cb_grey_mask(image)
		o_pixels = self.apply_o_mask(image)
		cerolb_pixels = self.apply_cerolb_mask(image)
	
		pixel_dictionary['YO'] =  yo_pixels
		pixel_dictionary['MY'] = my_pixels
		pixel_dictionary['VIO'] = vio_pixels
		pixel_dictionary['GREY'] = grey_pixels
		pixel_dictionary['PINK'] = pink_pixels
		pixel_dictionary['CRIM_RED'] = crim_red_pixels
		pixel_dictionary['HG'] = hg_pixels
		pixel_dictionary['EG'] = eg_pixels
		pixel_dictionary['CB_FLESH'] = cb_flesh_pixels
		pixel_dictionary['SG_CB_GREY'] = sg_cb_grey_pixels
		pixel_dictionary['OR'] = o_pixels
		pixel_dictionary['CEROLB'] = cerolb_pixels
	
		# print pixel_dictionary
	
		maximum_key = 'None'
		maximum_value = 0
		for key,value in pixel_dictionary.items():
			if pixel_dictionary[key] > maximum_value:
				maximum_key = key
				maximum_value = pixel_dictionary[key]
		

		return (maximum_key, maximum_value)


	def apply_vio_mask(self, image):
		lb_vio1 = np.array([123, 120, 40])
		ub_vio1 = np.array([135, 255, 103])
		vio_mask1 = cv2.inRange(image, lb_vio1, ub_vio1)
	
		lb_vio2 = np.array([124, 74, 36])
		ub_vio2 = np.array([138, 255, 255])
		vio_mask2 = cv2.inRange(image, lb_vio2, ub_vio2)
	
		lb_vio3 = np.array([122, 104, 33])
		ub_vio3 = np.array([158, 230, 87])
		vio_mask3 = cv2.inRange(image, lb_vio3, ub_vio3)
	
		lb_vio4 = np.array([119, 99, 66])
		ub_vio4 = np.array([126, 154, 138])
		vio_mask4 = cv2.inRange(image, lb_vio4, ub_vio4)
	
		lb_vio5 = np.array([112, 146, 30])
		ub_vio5 = np.array([129, 195, 113])
		vio_mask5 = cv2.inRange(image, lb_vio5, ub_vio5)
	
		vio_mask = vio_mask1 + vio_mask2 + vio_mask3 + vio_mask4 + vio_mask5
	
		result = cv2.bitwise_and(image, image, mask = vio_mask)
		non_zero_pixels = len(np.nonzero(result)[0])
	
		return non_zero_pixels


	def apply_eg_mask(self, image):
		lb_eg3 = np.array([50, 58, 195])
		ub_eg3 = np.array([61, 114, 255])
		eg_mask3 = cv2.inRange(image, lb_eg3, ub_eg3)
	
		eg_mask =  eg_mask3
	
		result = cv2.bitwise_and(image, image, mask = eg_mask)
		non_zero_pixels = len(np.nonzero(result)[0])
	
		return non_zero_pixels


	def apply_sg_cb_grey_mask(self, image):
		lb_sg_cb_grey = np.array([68, 59, 91])
		ub_sg_cb_grey = np.array([91, 255, 255])
		sg_cb_grey_mask = cv2.inRange(image, lb_sg_cb_grey, ub_sg_cb_grey)

		result = cv2.bitwise_and(image, image, mask = sg_cb_grey_mask)
		non_zero_pixels = len(np.nonzero(result)[0])
	
		return non_zero_pixels


	def apply_o_mask(self, image):
		lb_o4 = np.array([6, 219, 181])
		ub_o4 = np.array([16, 255, 255])
		o_mask4 = cv2.inRange(image, lb_o4, ub_o4)
	
		o_mask = o_mask4
	
		result = cv2.bitwise_and(image, image, mask = o_mask)
		non_zero_pixels = len(np.nonzero(result)[0])
	
		return non_zero_pixels

	def apply_my_mask(self, image):
		lb_my = np.array([26, 234, 243])
		ub_my = np.array([70, 255, 255])
		my_mask = cv2.inRange(image, lb_my, ub_my)
	
		result = cv2.bitwise_and(image, image, mask = my_mask)
		denoise_result = cv2.fastNlMeansDenoisingColored(result, None , 40, 40, 7, 21)
		non_zero_pixels = len(np.nonzero(denoise_result)[0])
	
		return non_zero_pixels


	def apply_pink_mask(self, image):
		lb_pink4 = np.array([177, 140, 192])
		ub_pink4 = np.array([181, 218, 255])
		pink_mask4 = cv2.inRange(image, lb_pink4, ub_pink4)
	
		pink_mask = pink_mask4
	
		result = cv2.bitwise_and(image, image, mask = pink_mask)
		non_zero_pixels = len(np.nonzero(result)[0])
	
		return non_zero_pixels

	def apply_hg_mask(self, image):
		lb_hg9 = np.array([45, 100, 40])
		ub_hg9 = np.array([52, 255, 93])
		hg_mask9 = cv2.inRange(image, lb_hg9, ub_hg9)
	
		lb_hg10 = np.array([39, 100, 62])
		ub_hg10 = np.array([71, 211, 105])
		hg_mask10 = cv2.inRange(image, lb_hg10, ub_hg10)
	
		hg_mask = hg_mask9 + hg_mask10
	
		result = cv2.bitwise_and(image, image, mask = hg_mask)
		non_zero_pixels = len(np.nonzero(result)[0])
	
		return non_zero_pixels

	def apply_crim_red_mask(self, image):
		lb_crim_red6 = np.array([0, 205, 73])
		ub_crim_red6 = np.array([4, 255, 255])
		crim_red_mask6 = cv2.inRange(image, lb_crim_red6, ub_crim_red6)

		crim_red_mask = crim_red_mask6

		result = cv2.bitwise_and(image, image, mask = crim_red_mask)
		non_zero_pixels = len(np.nonzero(result)[0])

		return non_zero_pixels


	def apply_cb_flesh_mask(self, image):
		lb_cb_flesh = np.array([96, 89, 113])
		ub_cb_flesh = np.array([105, 150, 255])
		cb_flesh_mask = cv2.inRange(image, lb_cb_flesh, ub_cb_flesh)

		result = cv2.bitwise_and(image, image, mask = cb_flesh_mask)
		denoise_result = cv2.fastNlMeansDenoisingColored(result, None , 40, 40, 7, 21)
		non_zero_pixels = len(np.nonzero(denoise_result)[0])

		return non_zero_pixels


	def apply_cerolb_mask(self, image):
		lb_cerolb1 = np.array([94, 204, 137])
		ub_cerolb1 = np.array([130, 255, 255])
		cerolb_mask1 = cv2.inRange(image, lb_cerolb1, ub_cerolb1)
	
		lb_cerolb2 = np.array([94, 194, 139])
		ub_cerolb2 = np.array([150, 255, 255])
		cerolb_mask2 = cv2.inRange(image, lb_cerolb2, ub_cerolb2)
	
		cerolb_mask = cerolb_mask1 + cerolb_mask2
	
		result = cv2.bitwise_and(image, image, mask = cerolb_mask)
		denoise_result = cv2.fastNlMeansDenoisingColored(result, None , 40, 40, 7, 21)
		non_zero_pixels = len(np.nonzero(denoise_result)[0])
	
		return non_zero_pixels


	def apply_grey_mask(self, image):
		lb_grey8 = np.array([45, 0, 173])
		ub_grey8 = np.array([115, 14, 216])
		grey_mask8 = cv2.inRange(image, lb_grey8, ub_grey8)
	
		lb_grey9 = np.array([23, 0, 173])
		ub_grey9 = np.array([115, 14, 216])
		grey_mask9 = cv2.inRange(image, lb_grey9, ub_grey9)
	
		grey_mask = grey_mask8 + grey_mask9
	
		result = cv2.bitwise_and(image, image, mask = grey_mask)
		denoise_result = cv2.fastNlMeansDenoisingColored(result, None , 40, 40, 7, 21)
	
		non_zero_pixels = len(np.nonzero(denoise_result)[0])
	
		return non_zero_pixels


	def apply_yo_mask(self, image):
		lb_yo5 = np.array([15, 206, 177])
		ub_yo5 = np.array([23, 255, 238])
		yo_mask5 = cv2.inRange(image, lb_yo5, ub_yo5)
	
		yo_mask = yo_mask5
	
		result = cv2.bitwise_and(image, image, mask = yo_mask)
		denoise_result = cv2.fastNlMeansDenoisingColored(result, None , 40, 40, 7, 21)
	
		non_zero_pixels = len(np.nonzero(denoise_result)[0])
	
		return non_zero_pixels


	def get_piece_dictionary_from_colour(self,colour):
		"""
		This method takes in a colour decided by the dominant colour method and
		returns a dictionary for the piece that maps to that colour.
		
		Args:
			colour: a parameter representing a valid colour.

		Returns:
			A dictionary that states the piece 'type' and colour (side) i.e. white or black

		"""
		return Pieces[colour].value 

	