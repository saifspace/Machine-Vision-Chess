import sys
sys.path.append('/Users/omgitsmotrix/Desktop/finalYearProject/preperation/image-processing/flood_light_day7/MachineVision')
sys.path.append('/Users/omgitsmotrix/desktop/finalYearProject/preperation/stockfish_integration')
sys.path.append('C:\Users\Saif\Desktop\\finalyearproject\preperation\stockfish_integration')

from ImageHandler import ImageHandler
from PyQt4 import QtGui, QtCore
import chess
import stockfishchess as engine
import ImageRepresentation as ir


class MainClass(QtGui.QMainWindow):

	def __init__(self):
		super(MainClass, self).__init__()
		self.setGeometry(50,50, 500, 500)
		self.setWindowTitle('Machine Vision System')
		self.image_handler = ImageHandler()

		self.draw()



	def draw(self):

		capture_image_button = QtGui.QPushButton("Capture Image", self)
		capture_image_button.clicked.connect(self.call_capture_image)
		capture_image_button.resize(150, 50)
		capture_image_button.move(20,30)

		load_captured_image_button = QtGui.QPushButton("Load Image", self)
		load_captured_image_button.clicked.connect(self.call_load_captured_image)
		load_captured_image_button.resize(150, 50)
		load_captured_image_button.move(20, 80)

		set_thresholds_button = QtGui.QPushButton("Set Thresholds", self)
		set_thresholds_button.clicked.connect(self.call_set_thresholds)
		set_thresholds_button.resize(150, 50)
		set_thresholds_button.move(20, 130)

		get_thresholds_button = QtGui.QPushButton("Get Thresholds", self)
		get_thresholds_button.clicked.connect(self.call_get_thresholds)
		get_thresholds_button.resize(150, 50)
		get_thresholds_button.move(20, 180)

		iterate_blocks_button = QtGui.QPushButton("Detect", self)
		iterate_blocks_button.clicked.connect(self.call_iterate_blocks)
		iterate_blocks_button.resize(150, 50)
		iterate_blocks_button.move(20, 230)

		close_all_windows_button = QtGui.QPushButton("Close Windows", self)
		close_all_windows_button.clicked.connect(self.close_all_windows)
		close_all_windows_button.resize(150, 50)
		close_all_windows_button.move(20, 280)

		quit_button = QtGui.QPushButton("Quit", self)
		quit_button.clicked.connect(self.quit_button_event)
		quit_button.resize(150, 50)
		quit_button.move(20, 330)

		capture = QtGui.QPushButton("Capture", self)
		capture.clicked.connect(self.capture_and_exit)
		capture.resize(150, 50)
		capture.move(20, 380)

		self.show()


	def call_capture_image(self):
		self.image_handler.capture_image()

	def call_load_captured_image(self):
		self.image_handler.load_captured_image(flag='win')

	def call_set_thresholds(self):
		self.image_handler.set_thresholds()
		self.image_handler.crop_and_save()
		self.image_handler.slice_image()
		self.image_handler.new_create_block_id_threshold_dictionary()

	def call_get_thresholds(self):
		print self.image_handler.get_crop_thresholds()

	def call_iterate_blocks(self):
		piece_square_info = self.image_handler.new_iterate_blocks()

		for s in piece_square_info.keys():
			chess.put(piece_square_info[s], s)

		print chess.ascii()
		setup = chess.get_setup()

		ir.create_image(setup)

		# engine.set_fen(chess.fen())
		# engine.best_move()

	def close_all_windows(self):
		self.image_handler.close_all_windows()

	def capture_and_exit(self):
		self.image_handler.set_exit_true()


	def quit_button_event(self):
		choice  = QtGui.QMessageBox.question(self, 'Extract!',
											 'Quit application?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

		if choice == QtGui.QMessageBox.Yes:
			self.image_handler.close_all_windows()
			print 'Quiting App'
			self.close()
			sys.exit()
		else:
			pass



def run():
	app = QtGui.QApplication(sys.argv)
	gui = MainClass()
	sys.exit(app.exec_())

run()