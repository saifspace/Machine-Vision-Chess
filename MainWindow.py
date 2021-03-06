import sys
import os

# path for Windows
sys.path.append(os.getcwd() + '\Libraries\chess_helper')

import chess
import stockfishchess as engine
import ImageRepresentation
from ColourDetector import Pieces
from Libraries.machine_learning.label_image import load_model

from PyQt5 import QtCore, QtWidgets, QtGui
from SettingsWindow import Ui_SettingsWindow
from ImageHandler import ImageHandler

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtWidgets.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

	def __init__(self):
		self.ui = Ui_SettingsWindow()
		self.image_handler = ImageHandler()
		self.ui.set_image_handler(self.image_handler)
		self.clicked_square = ""
		self.main_window_video_open = False
		self.main_window = None


	def openSettingsWindow(self):
		self.window = QtWidgets.QMainWindow()
		self.ui.setupUi(self.window)
		self.window.show()

	def call_capture_image(self):
		self.main_window_video_open = True
		self.image_handler.capture_image()

	def call_capture_and_exit(self):
		if (self.main_window_video_open == True):
			self.image_handler.set_exit_true()
			self.image_handler.load_captured_image(flag='win')
			self.main_window_video_open = False
		else:
			message_box = QtWidgets.QMessageBox()
			message_box.move(self.main_window.rect().center())
			message_box.question(message_box, 'Error', "Video Stream not open",
								 QtWidgets.QMessageBox.Ok)

	def call_iterate_blocks(self):
		piece_square_info = self.image_handler.iterate_blocks()
		chess.clear_setup()
		for s in piece_square_info.keys():
			chess.put(piece_square_info[s], s)

		print (chess.ascii())
		setup = chess.get_setup()
		ImageRepresentation.create_image(setup)
		self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\modifiedChessboard.png"))

	def call_ml_iterate_blocks(self):
		piece_square_info = self.image_handler.ml_iterate_blocks()
		chess.clear_setup()
		for s in piece_square_info.keys():
			chess.put(piece_square_info[s], s)

		print (chess.ascii())
		setup = chess.get_setup()
		ImageRepresentation.create_image(setup)
		self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\modifiedChessboard.png"))

	def call_predict(self):
		fen = chess.fen()
		engine.set_fen(fen)
		response = engine.best_move()
		self.prediction_text.setText(response)

	def updated_clicked_square(self, square):
		self.clicked_square = square
		self.call_second_detect()

	def call_second_detect(self):

		second_square_value_dict = self.image_handler.get_second_square_value_dict()

		if (len(second_square_value_dict) == 0):
			message_box = QtWidgets.QMessageBox()
			message_box.move(MainWindow.rect().center())
			message_box.question(message_box, 'Error', "No values: Run detect through Machine Learning first.", QtWidgets.QMessageBox.Ok)
		else:
			square_id = self.clicked_square
			if (second_square_value_dict[square_id] == "empty"):
				chess.remove(square_id)
				setup = chess.get_setup()
				ImageRepresentation.create_image(setup)
				self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\modifiedChessboard.png"))
			elif (second_square_value_dict[square_id]['type'] == "k"):
				colour = second_square_value_dict[square_id]['color']
				message_box = QtWidgets.QMessageBox()
				message_box.move(MainWindow.rect().center())
				message_box.question(message_box, "Note", "Second value is " + colour + " King. If board doesn't update, remove existing " + colour + " King.", QtWidgets.QMessageBox.Ok)
				chess.put(second_square_value_dict[square_id], square_id)
				setup = chess.get_setup()
				ImageRepresentation.create_image(setup)
				self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\modifiedChessboard.png"))
			else:
				print('2nd value ', second_square_value_dict[square_id], " square id: ", square_id)
				chess.remove(square_id)
				chess.put(second_square_value_dict[square_id], square_id)
				setup = chess.get_setup()
				ImageRepresentation.create_image(setup)
				self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\modifiedChessboard.png"))

	def call_quit(self):
		choice = QtWidgets.QMessageBox.question(self.main_window, 'Exit', 'Exit System?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if choice == QtWidgets.QMessageBox.Yes:
			print('Exiting the system.')
			sys.exit(0)
		else:
			pass

	def call_manual_fix(self):

		square_id = self.square_id_combo_box.currentText()
		piece_type = self.piece_combo_box.currentText()
		selection_checks = True
		if (square_id == "Square ID"):
			selection_checks = False
			message_box = QtWidgets.QMessageBox()
			message_box.move(MainWindow.rect().center())
			message_box.question(message_box, 'Error', "No Square ID selected. Please select from first drop-down menu.", QtWidgets.QMessageBox.Ok)
		if (piece_type == "Piece Type"):
			selection_checks = False
			message_box = QtWidgets.QMessageBox()
			message_box.move(MainWindow.rect().center())
			message_box.question(message_box, 'Error', "No Piece Type selected. Please select from second drop-down menu.", QtWidgets.QMessageBox.Ok)
		if (piece_type == "empty" and selection_checks):
			chess.remove(square_id)
			setup = chess.get_setup()
			ImageRepresentation.create_image(setup)
			self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\modifiedChessboard.png"))
		elif ("king" in piece_type and selection_checks):
			print("inserting KING")
			message_box = QtWidgets.QMessageBox()
			message_box.move(MainWindow.rect().center())
			message_box.question(message_box, "Note","Value is " + piece_type[0] + " King. If board doesn't update, remove existing " + piece_type[0] + " King.", QtWidgets.QMessageBox.Ok)
			chess.put(Pieces[piece_type].value, square_id)
			setup = chess.get_setup()
			ImageRepresentation.create_image(setup)
			self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\modifiedChessboard.png"))
		elif(selection_checks):
			chess.remove(square_id)
			chess.put(Pieces[piece_type].value, square_id)
			setup = chess.get_setup()
			ImageRepresentation.create_image(setup)
			self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\modifiedChessboard.png"))

	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.setFixedSize(799, 695)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.main_window = MainWindow

		self.board_image_label = QtWidgets.QLabel(self.centralwidget)
		self.board_image_label.setGeometry(QtCore.QRect(295, 2, 500, 500))
		self.board_image_label.setFrameShape(QtWidgets.QFrame.Box)
		self.board_image_label.setObjectName(_fromUtf8("board_image_label"))
		self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "\Resources\chessboard2.png"))

		self.video_button = QtWidgets.QPushButton(self.centralwidget)
		self.video_button.setGeometry(QtCore.QRect(0, 80, 221, 41))
		self.video_button.setObjectName(_fromUtf8("video_button"))
		self.video_button.clicked.connect(self.call_capture_image)

		self.colour_detect_button = QtWidgets.QPushButton(self.centralwidget)
		self.colour_detect_button.setEnabled(True)
		self.colour_detect_button.setGeometry(QtCore.QRect(0, 180, 221, 41))
		self.colour_detect_button.setCheckable(False)
		self.colour_detect_button.setAutoDefault(False)
		self.colour_detect_button.setDefault(False)
		self.colour_detect_button.setFlat(False)
		self.colour_detect_button.setObjectName(_fromUtf8("colour_detect_button"))
		self.colour_detect_button.clicked.connect(self.call_iterate_blocks)

		self.ml_detect_button = QtWidgets.QPushButton(self.centralwidget)
		self.ml_detect_button.setEnabled(True)
		self.ml_detect_button.setGeometry(QtCore.QRect(0, 230, 221, 41))
		self.ml_detect_button.setCheckable(False)
		self.ml_detect_button.setAutoDefault(False)
		self.ml_detect_button.setDefault(False)
		self.ml_detect_button.setFlat(False)
		self.ml_detect_button.setObjectName(_fromUtf8("ml_detect_button"))
		self.ml_detect_button.clicked.connect(self.call_ml_iterate_blocks)

		self.settings_button = QtWidgets.QPushButton(self.centralwidget)
		self.settings_button.setGeometry(QtCore.QRect(0, 30, 221, 41))
		self.settings_button.setObjectName(_fromUtf8("settings_button"))
		self.settings_button.clicked.connect(self.openSettingsWindow)

		self.vertical_line = QtWidgets.QFrame(self.centralwidget)
		self.vertical_line.setGeometry(QtCore.QRect(230, 0, 21, 421))
		self.vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
		self.vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.vertical_line.setObjectName(_fromUtf8("vertical_line"))

		self.horizontal_line = QtWidgets.QFrame(self.centralwidget)
		self.horizontal_line.setGeometry(QtCore.QRect(0, 410, 241, 16))
		self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
		self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.horizontal_line.setObjectName(_fromUtf8("horizontal_line"))

		self.prediction_text = QtWidgets.QLineEdit(self.centralwidget)
		self.prediction_text.setGeometry(QtCore.QRect(80, 440, 141, 31))
		self.prediction_text.setText(_fromUtf8(""))
		self.prediction_text.setObjectName(_fromUtf8("prediction_text"))
		self.prediction_label = QtWidgets.QLabel(self.centralwidget)
		self.prediction_label.setGeometry(QtCore.QRect(5, 440, 71, 31))

		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Arial"))
		font.setPointSize(11)
		font.setBold(False)
		font.setItalic(False)
		font.setWeight(50)

		self.prediction_label.setFont(font)
		self.prediction_label.setObjectName(_fromUtf8("prediction_label"))

		self.quit_button = QtWidgets.QPushButton(self.centralwidget)
		self.quit_button.setEnabled(True)
		self.quit_button.setGeometry(QtCore.QRect(0, 330, 221, 41))
		self.quit_button.setCheckable(False)
		self.quit_button.setAutoDefault(False)
		self.quit_button.setDefault(False)
		self.quit_button.setFlat(False)
		self.quit_button.setObjectName(_fromUtf8("quit_button"))
		self.quit_button.clicked.connect(self.call_quit)

		self.capture_image_button = QtWidgets.QPushButton(self.centralwidget)
		self.capture_image_button.setGeometry(QtCore.QRect(0, 130, 221, 41))
		self.capture_image_button.setObjectName(_fromUtf8("capture_image_button"))
		self.capture_image_button.clicked.connect(self.call_capture_and_exit)

		self.predict_button = QtWidgets.QPushButton(self.centralwidget)
		self.predict_button.setEnabled(True)
		self.predict_button.setGeometry(QtCore.QRect(0, 280, 221, 41))
		self.predict_button.setCheckable(False)
		self.predict_button.setAutoDefault(False)
		self.predict_button.setDefault(False)
		self.predict_button.setFlat(False)
		self.predict_button.setObjectName(_fromUtf8("predict_button"))
		self.predict_button.clicked.connect(self.call_predict)

		self.a_label = QtWidgets.QLabel(self.centralwidget)
		self.a_label.setGeometry(QtCore.QRect(330, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.a_label.setFont(font)
		self.a_label.setObjectName("a_label")
		self.b_label = QtWidgets.QLabel(self.centralwidget)
		self.b_label.setGeometry(QtCore.QRect(390, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.b_label.setFont(font)
		self.b_label.setObjectName("b_label")
		self.c_label = QtWidgets.QLabel(self.centralwidget)
		self.c_label.setGeometry(QtCore.QRect(450, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.c_label.setFont(font)
		self.c_label.setObjectName("c_label")
		self.d_label = QtWidgets.QLabel(self.centralwidget)
		self.d_label.setGeometry(QtCore.QRect(510, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.d_label.setFont(font)
		self.d_label.setObjectName("d_label")
		self.e_label = QtWidgets.QLabel(self.centralwidget)
		self.e_label.setGeometry(QtCore.QRect(580, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.e_label.setFont(font)
		self.e_label.setObjectName("e_label")
		self.f_label = QtWidgets.QLabel(self.centralwidget)
		self.f_label.setGeometry(QtCore.QRect(640, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.f_label.setFont(font)
		self.f_label.setObjectName("f_label")
		self.g_label = QtWidgets.QLabel(self.centralwidget)
		self.g_label.setGeometry(QtCore.QRect(700, 510, 16, 21))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.g_label.setFont(font)
		self.g_label.setObjectName("g_label")
		self.h_label = QtWidgets.QLabel(self.centralwidget)
		self.h_label.setGeometry(QtCore.QRect(760, 510, 16, 21))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.h_label.setFont(font)
		self.h_label.setObjectName("h_label")
		self.one_label = QtWidgets.QLabel(self.centralwidget)
		self.one_label.setGeometry(QtCore.QRect(280, 460, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.one_label.setFont(font)
		self.one_label.setObjectName("one_label")
		self.two_label = QtWidgets.QLabel(self.centralwidget)
		self.two_label.setGeometry(QtCore.QRect(280, 400, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.two_label.setFont(font)
		self.two_label.setObjectName("two_label")
		self.three_label = QtWidgets.QLabel(self.centralwidget)
		self.three_label.setGeometry(QtCore.QRect(280, 340, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.three_label.setFont(font)
		self.three_label.setObjectName("three_label")
		self.four_label = QtWidgets.QLabel(self.centralwidget)
		self.four_label.setGeometry(QtCore.QRect(280, 280, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.four_label.setFont(font)
		self.four_label.setObjectName("four_label")
		self.five_label = QtWidgets.QLabel(self.centralwidget)
		self.five_label.setGeometry(QtCore.QRect(280, 220, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.five_label.setFont(font)
		self.five_label.setObjectName("five_label")
		self.six_label = QtWidgets.QLabel(self.centralwidget)
		self.six_label.setGeometry(QtCore.QRect(280, 160, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.six_label.setFont(font)
		self.six_label.setObjectName("six_label")
		self.seven_label = QtWidgets.QLabel(self.centralwidget)
		self.seven_label.setGeometry(QtCore.QRect(280, 90, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.seven_label.setFont(font)
		self.seven_label.setObjectName("seven_label")
		self.eight_label = QtWidgets.QLabel(self.centralwidget)
		self.eight_label.setGeometry(QtCore.QRect(280, 20, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(15)
		font.setBold(True)
		font.setWeight(75)
		self.eight_label.setFont(font)
		self.eight_label.setObjectName("eight_label")

		self.manual_input_frame = QtWidgets.QFrame(self.centralwidget)
		self.manual_input_frame.setGeometry(QtCore.QRect(10, 530, 301, 141))
		self.manual_input_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.manual_input_frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.manual_input_frame.setObjectName("manual_input_frame")

		self.square_id_combo_box = QtWidgets.QComboBox(self.manual_input_frame)
		self.square_id_combo_box.setGeometry(QtCore.QRect(0, 50, 141, 31))
		self.square_id_combo_box.setFrame(False)
		self.square_id_combo_box.setObjectName("square_id_combo_box")
		self.square_id_combo_box.addItems(['Square ID','a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
										   'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
										   'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
										   'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
										   'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
										   'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
										   'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
										   'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'])

		self.piece_combo_box = QtWidgets.QComboBox(self.manual_input_frame)
		self.piece_combo_box.setGeometry(QtCore.QRect(0, 80, 141, 31))
		self.piece_combo_box.setFrame(False)
		self.piece_combo_box.setObjectName("piece_combo_box")
		self.piece_combo_box.addItems(['Piece Type','empty' ,'wpawn', 'wrook', 'wknight', 'wbishop', 'wking', 'wqueen',
									   'bpawn', 'brook', 'bknight', 'bbishop', 'bking', 'bqueen'])

		self.manual_fix_button = QtWidgets.QPushButton(self.manual_input_frame)
		self.manual_fix_button.setGeometry(QtCore.QRect(150, 65, 151, 31))
		self.manual_fix_button.setObjectName("manual_fix_button")
		self.manual_fix_button.clicked.connect(self.call_manual_fix)

		self.fix_title_label = QtWidgets.QLabel(self.manual_input_frame)
		self.fix_title_label.setGeometry(QtCore.QRect(115, 10, 150, 16))
		self.fix_title_label.setObjectName("fix_title_label")

		self.a1_button = QtWidgets.QPushButton(self.centralwidget)
		self.a1_button.setGeometry(QtCore.QRect(295, 439, 63, 63))
		self.a1_button.setObjectName("a1_button")
		self.a1_button.setStyleSheet("background: transparent")
		self.a1_button.clicked.connect(lambda: self.updated_clicked_square("a1"))

		self.a2_button = QtWidgets.QPushButton(self.centralwidget)
		self.a2_button.setGeometry(QtCore.QRect(295, 377, 63, 63))
		self.a2_button.setObjectName("a2_button")
		self.a2_button.setStyleSheet("background: transparent")
		self.a2_button.clicked.connect(lambda: self.updated_clicked_square("a2"))

		self.a3_button = QtWidgets.QPushButton(self.centralwidget)
		self.a3_button.setGeometry(QtCore.QRect(295, 315, 63, 63))
		self.a3_button.setObjectName("a3_button")
		self.a3_button.setStyleSheet("background: transparent")
		self.a3_button.clicked.connect(lambda: self.updated_clicked_square("a3"))

		self.a4_button = QtWidgets.QPushButton(self.centralwidget)
		self.a4_button.setGeometry(QtCore.QRect(295, 253, 63, 63))
		self.a4_button.setObjectName("a4_button")
		self.a4_button.setStyleSheet("background: transparent")
		self.a4_button.clicked.connect(lambda: self.updated_clicked_square("a4"))

		self.a5_button = QtWidgets.QPushButton(self.centralwidget)
		self.a5_button.setGeometry(QtCore.QRect(295, 191, 63, 63))
		self.a5_button.setObjectName("a5_button")
		self.a5_button.setStyleSheet("background: transparent")
		self.a5_button.clicked.connect(lambda: self.updated_clicked_square("a5"))

		self.a6_button = QtWidgets.QPushButton(self.centralwidget)
		self.a6_button.setGeometry(QtCore.QRect(295, 129, 63, 63))
		self.a6_button.setObjectName("a6_button")
		self.a6_button.setStyleSheet("background: transparent")
		self.a6_button.clicked.connect(lambda: self.updated_clicked_square("a6"))

		self.a7_button = QtWidgets.QPushButton(self.centralwidget)
		self.a7_button.setGeometry(QtCore.QRect(295, 67, 63, 63))
		self.a7_button.setObjectName("a7_button")
		self.a7_button.setStyleSheet("background: transparent")
		self.a7_button.clicked.connect(lambda: self.updated_clicked_square("a7"))

		self.a8_button = QtWidgets.QPushButton(self.centralwidget)
		self.a8_button.setGeometry(QtCore.QRect(295, 5, 63, 63))
		self.a8_button.setObjectName("a8_button")
		self.a8_button.setStyleSheet("background: transparent")
		self.a8_button.clicked.connect(lambda: self.updated_clicked_square("a8"))

		self.b1_button = QtWidgets.QPushButton(self.centralwidget)
		self.b1_button.setGeometry(QtCore.QRect(358, 439, 63, 63))
		self.b1_button.setObjectName("b1_button")
		self.b1_button.setStyleSheet("background: transparent")
		self.b1_button.clicked.connect(lambda: self.updated_clicked_square("b1"))

		self.b2_button = QtWidgets.QPushButton(self.centralwidget)
		self.b2_button.setGeometry(QtCore.QRect(358, 377, 63, 63))
		self.b2_button.setObjectName("b2_button")
		self.b2_button.setStyleSheet("background: transparent")
		self.b2_button.clicked.connect(lambda: self.updated_clicked_square("b2"))

		self.b3_button = QtWidgets.QPushButton(self.centralwidget)
		self.b3_button.setGeometry(QtCore.QRect(358, 315, 63, 63))
		self.b3_button.setObjectName("b3_button")
		self.b3_button.setStyleSheet("background: transparent")
		self.b3_button.clicked.connect(lambda: self.updated_clicked_square("b3"))

		self.b4_button = QtWidgets.QPushButton(self.centralwidget)
		self.b4_button.setGeometry(QtCore.QRect(358, 253, 63, 63))
		self.b4_button.setObjectName("b4_button")
		self.b4_button.setStyleSheet("background: transparent")
		self.b4_button.clicked.connect(lambda: self.updated_clicked_square("b4"))

		self.b5_button = QtWidgets.QPushButton(self.centralwidget)
		self.b5_button.setGeometry(QtCore.QRect(358, 191, 63, 63))
		self.b5_button.setObjectName("b5_button")
		self.b5_button.setStyleSheet("background: transparent")
		self.b5_button.clicked.connect(lambda: self.updated_clicked_square("b5"))

		self.b6_button = QtWidgets.QPushButton(self.centralwidget)
		self.b6_button.setGeometry(QtCore.QRect(358, 129, 63, 63))
		self.b6_button.setObjectName("b6_button")
		self.b6_button.setStyleSheet("background: transparent")
		self.b6_button.clicked.connect(lambda: self.updated_clicked_square("b6"))

		self.b7_button = QtWidgets.QPushButton(self.centralwidget)
		self.b7_button.setGeometry(QtCore.QRect(358, 67, 63, 63))
		self.b7_button.setObjectName("b7_button")
		self.b7_button.setStyleSheet("background: transparent")
		self.b7_button.clicked.connect(lambda: self.updated_clicked_square("b7"))

		self.b8_button = QtWidgets.QPushButton(self.centralwidget)
		self.b8_button.setGeometry(QtCore.QRect(358, 5, 63, 63))
		self.b8_button.setObjectName("b8_button")
		self.b8_button.setStyleSheet("background: transparent")
		self.b8_button.clicked.connect(lambda: self.updated_clicked_square("b8"))

		self.c1_button = QtWidgets.QPushButton(self.centralwidget)
		self.c1_button.setGeometry(QtCore.QRect(421, 439, 63, 63))
		self.c1_button.setObjectName("c1_button")
		self.c1_button.setStyleSheet("background: transparent")
		self.c1_button.clicked.connect(lambda: self.updated_clicked_square("c1"))

		self.c2_button = QtWidgets.QPushButton(self.centralwidget)
		self.c2_button.setGeometry(QtCore.QRect(421, 377, 63, 63))
		self.c2_button.setObjectName("c2_button")
		self.c2_button.setStyleSheet("background: transparent")
		self.c2_button.clicked.connect(lambda: self.updated_clicked_square("c2"))

		self.c3_button = QtWidgets.QPushButton(self.centralwidget)
		self.c3_button.setGeometry(QtCore.QRect(421, 315, 63, 63))
		self.c3_button.setObjectName("c3_button")
		self.c3_button.setStyleSheet("background: transparent")
		self.c3_button.clicked.connect(lambda: self.updated_clicked_square("c3"))

		self.c4_button = QtWidgets.QPushButton(self.centralwidget)
		self.c4_button.setGeometry(QtCore.QRect(421, 253, 63, 63))
		self.c4_button.setObjectName("c4_button")
		self.c4_button.setStyleSheet("background: transparent")
		self.c4_button.clicked.connect(lambda: self.updated_clicked_square("c4"))

		self.c5_button = QtWidgets.QPushButton(self.centralwidget)
		self.c5_button.setGeometry(QtCore.QRect(421, 191, 63, 63))
		self.c5_button.setObjectName("c5_button")
		self.c5_button.setStyleSheet("background: transparent")
		self.c5_button.clicked.connect(lambda: self.updated_clicked_square("c5"))

		self.c6_button = QtWidgets.QPushButton(self.centralwidget)
		self.c6_button.setGeometry(QtCore.QRect(421, 129, 63, 63))
		self.c6_button.setObjectName("c6_button")
		self.c6_button.setStyleSheet("background: transparent")
		self.c6_button.clicked.connect(lambda: self.updated_clicked_square("c6"))

		self.c7_button = QtWidgets.QPushButton(self.centralwidget)
		self.c7_button.setGeometry(QtCore.QRect(421, 67, 63, 63))
		self.c7_button.setObjectName("c7_button")
		self.c7_button.setStyleSheet("background: transparent")
		self.c7_button.clicked.connect(lambda: self.updated_clicked_square("c7"))

		self.c8_button = QtWidgets.QPushButton(self.centralwidget)
		self.c8_button.setGeometry(QtCore.QRect(421, 5, 63, 63))
		self.c8_button.setObjectName("c8_button")
		self.c8_button.setStyleSheet("background: transparent")
		self.c8_button.clicked.connect(lambda: self.updated_clicked_square("c8"))

		self.d1_button = QtWidgets.QPushButton(self.centralwidget)
		self.d1_button.setGeometry(QtCore.QRect(484, 439, 63, 63))
		self.d1_button.setObjectName("d1_button")
		self.d1_button.setStyleSheet("background: transparent")
		self.d1_button.clicked.connect(lambda: self.updated_clicked_square("d1"))

		self.d2_button = QtWidgets.QPushButton(self.centralwidget)
		self.d2_button.setGeometry(QtCore.QRect(484, 377, 63, 63))
		self.d2_button.setObjectName("d2_button")
		self.d2_button.setStyleSheet("background: transparent")
		self.d2_button.clicked.connect(lambda: self.updated_clicked_square("d2"))

		self.d3_button = QtWidgets.QPushButton(self.centralwidget)
		self.d3_button.setGeometry(QtCore.QRect(484, 315, 63, 63))
		self.d3_button.setObjectName("d3_button")
		self.d3_button.setStyleSheet("background: transparent")
		self.d3_button.clicked.connect(lambda: self.updated_clicked_square("d3"))

		self.d4_button = QtWidgets.QPushButton(self.centralwidget)
		self.d4_button.setGeometry(QtCore.QRect(484, 253, 63, 63))
		self.d4_button.setObjectName("d4_button")
		self.d4_button.setStyleSheet("background: transparent")
		self.d4_button.clicked.connect(lambda: self.updated_clicked_square("d4"))

		self.d5_button = QtWidgets.QPushButton(self.centralwidget)
		self.d5_button.setGeometry(QtCore.QRect(484, 191, 63, 63))
		self.d5_button.setObjectName("d5_button")
		self.d5_button.setStyleSheet("background: transparent")
		self.d5_button.clicked.connect(lambda: self.updated_clicked_square("d5"))

		self.d6_button = QtWidgets.QPushButton(self.centralwidget)
		self.d6_button.setGeometry(QtCore.QRect(484, 129, 63, 63))
		self.d6_button.setObjectName("d6_button")
		self.d6_button.setStyleSheet("background: transparent")
		self.d6_button.clicked.connect(lambda: self.updated_clicked_square("d6"))

		self.d7_button = QtWidgets.QPushButton(self.centralwidget)
		self.d7_button.setGeometry(QtCore.QRect(484, 67, 63, 63))
		self.d7_button.setObjectName("d7_button")
		self.d7_button.setStyleSheet("background: transparent")
		self.d7_button.clicked.connect(lambda: self.updated_clicked_square("d7"))

		self.d8_button = QtWidgets.QPushButton(self.centralwidget)
		self.d8_button.setGeometry(QtCore.QRect(484, 5, 63, 63))
		self.d8_button.setObjectName("d8_button")
		self.d8_button.setStyleSheet("background: transparent")
		self.d8_button.clicked.connect(lambda: self.updated_clicked_square("d8"))

		self.e1_button = QtWidgets.QPushButton(self.centralwidget)
		self.e1_button.setGeometry(QtCore.QRect(547, 439, 63, 63))
		self.e1_button.setObjectName("e1_button")
		self.e1_button.setStyleSheet("background: transparent")
		self.e1_button.clicked.connect(lambda: self.updated_clicked_square("e1"))

		self.e2_button = QtWidgets.QPushButton(self.centralwidget)
		self.e2_button.setGeometry(QtCore.QRect(547, 377, 63, 63))
		self.e2_button.setObjectName("e2_button")
		self.e2_button.setStyleSheet("background: transparent")
		self.e2_button.clicked.connect(lambda: self.updated_clicked_square("e2"))

		self.e3_button = QtWidgets.QPushButton(self.centralwidget)
		self.e3_button.setGeometry(QtCore.QRect(547, 315, 63, 63))
		self.e3_button.setObjectName("e3_button")
		self.e3_button.setStyleSheet("background: transparent")
		self.e3_button.clicked.connect(lambda: self.updated_clicked_square("e3"))

		self.e4_button = QtWidgets.QPushButton(self.centralwidget)
		self.e4_button.setGeometry(QtCore.QRect(547, 253, 63, 63))
		self.e4_button.setObjectName("e4_button")
		self.e4_button.setStyleSheet("background: transparent")
		self.e4_button.clicked.connect(lambda: self.updated_clicked_square("e4"))

		self.e5_button = QtWidgets.QPushButton(self.centralwidget)
		self.e5_button.setGeometry(QtCore.QRect(547, 191, 63, 63))
		self.e5_button.setObjectName("e5_button")
		self.e5_button.setStyleSheet("background: transparent")
		self.e5_button.clicked.connect(lambda: self.updated_clicked_square("e5"))

		self.e6_button = QtWidgets.QPushButton(self.centralwidget)
		self.e6_button.setGeometry(QtCore.QRect(547, 129, 63, 63))
		self.e6_button.setObjectName("e6_button")
		self.e6_button.setStyleSheet("background: transparent")
		self.e6_button.clicked.connect(lambda: self.updated_clicked_square("e6"))

		self.e7_button = QtWidgets.QPushButton(self.centralwidget)
		self.e7_button.setGeometry(QtCore.QRect(547, 67, 63, 63))
		self.e7_button.setObjectName("e7_button")
		self.e7_button.setStyleSheet("background: transparent")
		self.e7_button.clicked.connect(lambda: self.updated_clicked_square("e7"))

		self.e8_button = QtWidgets.QPushButton(self.centralwidget)
		self.e8_button.setGeometry(QtCore.QRect(547, 5, 63, 63))
		self.e8_button.setObjectName("e8_button")
		self.e8_button.setStyleSheet("background: transparent")
		self.e8_button.clicked.connect(lambda: self.updated_clicked_square("e8"))

		self.f1_button = QtWidgets.QPushButton(self.centralwidget)
		self.f1_button.setGeometry(QtCore.QRect(610, 439, 63, 63))
		self.f1_button.setObjectName("f1_button")
		self.f1_button.setStyleSheet("background: transparent")
		self.f1_button.clicked.connect(lambda: self.updated_clicked_square("f1"))

		self.f2_button = QtWidgets.QPushButton(self.centralwidget)
		self.f2_button.setGeometry(QtCore.QRect(610, 377, 63, 63))
		self.f2_button.setObjectName("f2_button")
		self.f2_button.setStyleSheet("background: transparent")
		self.f2_button.clicked.connect(lambda: self.updated_clicked_square("f2"))

		self.f3_button = QtWidgets.QPushButton(self.centralwidget)
		self.f3_button.setGeometry(QtCore.QRect(610, 315, 63, 63))
		self.f3_button.setObjectName("f3_button")
		self.f3_button.setStyleSheet("background: transparent")
		self.f3_button.clicked.connect(lambda: self.updated_clicked_square("f3"))

		self.f4_button = QtWidgets.QPushButton(self.centralwidget)
		self.f4_button.setGeometry(QtCore.QRect(610, 253, 63, 63))
		self.f4_button.setObjectName("f4_button")
		self.f4_button.setStyleSheet("background: transparent")
		self.f4_button.clicked.connect(lambda: self.updated_clicked_square("f4"))

		self.f5_button = QtWidgets.QPushButton(self.centralwidget)
		self.f5_button.setGeometry(QtCore.QRect(610, 191, 63, 63))
		self.f5_button.setObjectName("f5_button")
		self.f5_button.setStyleSheet("background: transparent")
		self.f5_button.clicked.connect(lambda: self.updated_clicked_square("f5"))

		self.f6_button = QtWidgets.QPushButton(self.centralwidget)
		self.f6_button.setGeometry(QtCore.QRect(610, 129, 63, 63))
		self.f6_button.setObjectName("f6_button")
		self.f6_button.setStyleSheet("background: transparent")
		self.f6_button.clicked.connect(lambda: self.updated_clicked_square("f6"))

		self.f7_button = QtWidgets.QPushButton(self.centralwidget)
		self.f7_button.setGeometry(QtCore.QRect(610, 67, 63, 63))
		self.f7_button.setObjectName("f7_button")
		self.f7_button.setStyleSheet("background: transparent")
		self.f7_button.clicked.connect(lambda: self.updated_clicked_square("f7"))

		self.f8_button = QtWidgets.QPushButton(self.centralwidget)
		self.f8_button.setGeometry(QtCore.QRect(610, 5, 63, 63))
		self.f8_button.setObjectName("f8_button")
		self.f8_button.setStyleSheet("background: transparent")
		self.f8_button.clicked.connect(lambda: self.updated_clicked_square("f8"))

		self.g1_button = QtWidgets.QPushButton(self.centralwidget)
		self.g1_button.setGeometry(QtCore.QRect(673, 439, 63, 63))
		self.g1_button.setObjectName("g1_button")
		self.g1_button.setStyleSheet("background: transparent")
		self.g1_button.clicked.connect(lambda: self.updated_clicked_square("g1"))

		self.g2_button = QtWidgets.QPushButton(self.centralwidget)
		self.g2_button.setGeometry(QtCore.QRect(673, 377, 63, 63))
		self.g2_button.setObjectName("g2_button")
		self.g2_button.setStyleSheet("background: transparent")
		self.g2_button.clicked.connect(lambda: self.updated_clicked_square("g2"))

		self.g3_button = QtWidgets.QPushButton(self.centralwidget)
		self.g3_button.setGeometry(QtCore.QRect(673, 315, 63, 63))
		self.g3_button.setObjectName("g3_button")
		self.g3_button.setStyleSheet("background: transparent")
		self.g3_button.clicked.connect(lambda: self.updated_clicked_square("g3"))

		self.g4_button = QtWidgets.QPushButton(self.centralwidget)
		self.g4_button.setGeometry(QtCore.QRect(673, 253, 63, 63))
		self.g4_button.setObjectName("g4_button")
		self.g4_button.setStyleSheet("background: transparent")
		self.g4_button.clicked.connect(lambda: self.updated_clicked_square("g4"))

		self.g5_button = QtWidgets.QPushButton(self.centralwidget)
		self.g5_button.setGeometry(QtCore.QRect(673, 191, 63, 63))
		self.g5_button.setObjectName("g5_button")
		self.g5_button.setStyleSheet("background: transparent")
		self.g5_button.clicked.connect(lambda: self.updated_clicked_square("g5"))

		self.g6_button = QtWidgets.QPushButton(self.centralwidget)
		self.g6_button.setGeometry(QtCore.QRect(673, 129, 63, 63))
		self.g6_button.setObjectName("g6_button")
		self.g6_button.setStyleSheet("background: transparent")
		self.g6_button.clicked.connect(lambda: self.updated_clicked_square("g6"))

		self.g7_button = QtWidgets.QPushButton(self.centralwidget)
		self.g7_button.setGeometry(QtCore.QRect(673, 67, 63, 63))
		self.g7_button.setObjectName("g7_button")
		self.g7_button.setStyleSheet("background: transparent")
		self.g7_button.clicked.connect(lambda: self.updated_clicked_square("g7"))

		self.g8_button = QtWidgets.QPushButton(self.centralwidget)
		self.g8_button.setGeometry(QtCore.QRect(673, 5, 63, 63))
		self.g8_button.setObjectName("g8_button")
		self.g8_button.setStyleSheet("background: transparent")
		self.g8_button.clicked.connect(lambda: self.updated_clicked_square("g8"))

		self.h1_button = QtWidgets.QPushButton(self.centralwidget)
		self.h1_button.setGeometry(QtCore.QRect(736, 439, 63, 63))
		self.h1_button.setObjectName("h1_button")
		self.h1_button.setStyleSheet("background: transparent")
		self.h1_button.clicked.connect(lambda: self.updated_clicked_square("h1"))

		self.h2_button = QtWidgets.QPushButton(self.centralwidget)
		self.h2_button.setGeometry(QtCore.QRect(736, 377, 63, 63))
		self.h2_button.setObjectName("h2_button")
		self.h2_button.setStyleSheet("background: transparent")
		self.h2_button.clicked.connect(lambda: self.updated_clicked_square("h2"))

		self.h3_button = QtWidgets.QPushButton(self.centralwidget)
		self.h3_button.setGeometry(QtCore.QRect(736, 315, 63, 63))
		self.h3_button.setObjectName("h3_button")
		self.h3_button.setStyleSheet("background: transparent")
		self.h3_button.clicked.connect(lambda: self.updated_clicked_square("h3"))

		self.h4_button = QtWidgets.QPushButton(self.centralwidget)
		self.h4_button.setGeometry(QtCore.QRect(736, 253, 63, 63))
		self.h4_button.setObjectName("h4_button")
		self.h4_button.setStyleSheet("background: transparent")
		self.h4_button.clicked.connect(lambda: self.updated_clicked_square("h4"))

		self.h5_button = QtWidgets.QPushButton(self.centralwidget)
		self.h5_button.setGeometry(QtCore.QRect(736, 191, 63, 63))
		self.h5_button.setObjectName("h5_button")
		self.h5_button.setStyleSheet("background: transparent")
		self.h5_button.clicked.connect(lambda: self.updated_clicked_square("h5"))

		self.h6_button = QtWidgets.QPushButton(self.centralwidget)
		self.h6_button.setGeometry(QtCore.QRect(736, 129, 63, 63))
		self.h6_button.setObjectName("h6_button")
		self.h6_button.setStyleSheet("background: transparent")
		self.h6_button.clicked.connect(lambda: self.updated_clicked_square("h6"))

		self.h7_button = QtWidgets.QPushButton(self.centralwidget)
		self.h7_button.setGeometry(QtCore.QRect(736, 67, 63, 63))
		self.h7_button.setObjectName("h7_button")
		self.h7_button.setStyleSheet("background: transparent")
		self.h7_button.clicked.connect(lambda: self.updated_clicked_square("h7"))

		self.h8_button = QtWidgets.QPushButton(self.centralwidget)
		self.h8_button.setGeometry(QtCore.QRect(736, 5, 63, 63))
		self.h8_button.setObjectName("h8_button")
		self.h8_button.setStyleSheet("background: transparent")
		self.h8_button.clicked.connect(lambda: self.updated_clicked_square("h8"))

		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		# self.board_image_label.setText(_translate("MainWindow", "Chessboard Image Representation", None))
		self.video_button.setText(_translate("MainWindow", "Show Video Stream", None))
		self.colour_detect_button.setText(_translate("MainWindow", "Detect: Colour Detection", None))
		self.ml_detect_button.setText(_translate("MainWindow", "Detect: Machine Learning", None))
		self.settings_button.setText(_translate("MainWindow", "Settings", None))
		self.prediction_label.setText(_translate("MainWindow", "Prediction:", None))
		self.quit_button.setText(_translate("MainWindow", "Quit", None))
		self.capture_image_button.setText(_translate("MainWindow", "Capture Image", None))
		self.predict_button.setText(_translate("MainWindow", "Predict", None))

		self.manual_fix_button.setText(_translate("MainWindow", "Manual Fix", None))
		self.fix_title_label.setText(_translate("MainWindow", "Manually Fix Chessboard", None))

		self.a_label.setText(_translate("MainWindow", "a", None))
		self.b_label.setText(_translate("MainWindow", "b", None))
		self.c_label.setText(_translate("MainWindow", "c", None))
		self.d_label.setText(_translate("MainWindow", "d", None))
		self.e_label.setText(_translate("MainWindow", "e", None))
		self.f_label.setText(_translate("MainWindow", "f", None))
		self.g_label.setText(_translate("MainWindow", "g", None))
		self.h_label.setText(_translate("MainWindow", "h", None))
		self.one_label.setText(_translate("MainWindow", "1", None))
		self.two_label.setText(_translate("MainWindow", "2", None))
		self.three_label.setText(_translate("MainWindow", "3", None))
		self.four_label.setText(_translate("MainWindow", "4", None))
		self.five_label.setText(_translate("MainWindow", "5", None))
		self.six_label.setText(_translate("MainWindow", "6", None))
		self.seven_label.setText(_translate("MainWindow", "7", None))
		self.eight_label.setText(_translate("MainWindow", "8", None))

		self.a1_button.setText(_translate("MainWindow","" ,None))
		self.a2_button.setText(_translate("MainWindow", "", None))
		self.a3_button.setText(_translate("MainWindow", "", None))
		self.a4_button.setText(_translate("MainWindow", "", None))
		self.a5_button.setText(_translate("MainWindow", "", None))
		self.a6_button.setText(_translate("MainWindow", "", None))
		self.a7_button.setText(_translate("MainWindow", "", None))
		self.a8_button.setText(_translate("MainWindow", "", None))
		self.b1_button.setText(_translate("MainWindow","" ,None))
		self.b2_button.setText(_translate("MainWindow", "", None))
		self.b3_button.setText(_translate("MainWindow", "", None))
		self.b4_button.setText(_translate("MainWindow", "", None))
		self.b5_button.setText(_translate("MainWindow", "", None))
		self.b6_button.setText(_translate("MainWindow", "", None))
		self.b7_button.setText(_translate("MainWindow", "", None))
		self.b8_button.setText(_translate("MainWindow", "", None))
		self.c1_button.setText(_translate("MainWindow","" ,None))
		self.c2_button.setText(_translate("MainWindow", "", None))
		self.c3_button.setText(_translate("MainWindow", "", None))
		self.c4_button.setText(_translate("MainWindow", "", None))
		self.c5_button.setText(_translate("MainWindow", "", None))
		self.c6_button.setText(_translate("MainWindow", "", None))
		self.c7_button.setText(_translate("MainWindow", "", None))
		self.c8_button.setText(_translate("MainWindow", "", None))
		self.d1_button.setText(_translate("MainWindow","" ,None))
		self.d2_button.setText(_translate("MainWindow", "", None))
		self.d3_button.setText(_translate("MainWindow", "", None))
		self.d4_button.setText(_translate("MainWindow", "", None))
		self.d5_button.setText(_translate("MainWindow", "", None))
		self.d6_button.setText(_translate("MainWindow", "", None))
		self.d7_button.setText(_translate("MainWindow", "", None))
		self.d8_button.setText(_translate("MainWindow", "", None))
		self.e1_button.setText(_translate("MainWindow","" ,None))
		self.e2_button.setText(_translate("MainWindow", "", None))
		self.e3_button.setText(_translate("MainWindow", "", None))
		self.e4_button.setText(_translate("MainWindow", "", None))
		self.e5_button.setText(_translate("MainWindow", "", None))
		self.e6_button.setText(_translate("MainWindow", "", None))
		self.e7_button.setText(_translate("MainWindow", "", None))
		self.e8_button.setText(_translate("MainWindow", "", None))
		self.f1_button.setText(_translate("MainWindow","" ,None))
		self.f2_button.setText(_translate("MainWindow", "", None))
		self.f3_button.setText(_translate("MainWindow", "", None))
		self.f4_button.setText(_translate("MainWindow", "", None))
		self.f5_button.setText(_translate("MainWindow", "", None))
		self.f6_button.setText(_translate("MainWindow", "", None))
		self.f7_button.setText(_translate("MainWindow", "", None))
		self.f8_button.setText(_translate("MainWindow", "", None))
		self.g1_button.setText(_translate("MainWindow","" ,None))
		self.g2_button.setText(_translate("MainWindow", "", None))
		self.g3_button.setText(_translate("MainWindow", "", None))
		self.g4_button.setText(_translate("MainWindow", "", None))
		self.g5_button.setText(_translate("MainWindow", "", None))
		self.g6_button.setText(_translate("MainWindow", "", None))
		self.g7_button.setText(_translate("MainWindow", "", None))
		self.g8_button.setText(_translate("MainWindow", "", None))
		self.h1_button.setText(_translate("MainWindow","" ,None))
		self.h2_button.setText(_translate("MainWindow", "", None))
		self.h3_button.setText(_translate("MainWindow", "", None))
		self.h4_button.setText(_translate("MainWindow", "", None))
		self.h5_button.setText(_translate("MainWindow", "", None))
		self.h6_button.setText(_translate("MainWindow", "", None))
		self.h7_button.setText(_translate("MainWindow", "", None))
		self.h8_button.setText(_translate("MainWindow", "", None))

if __name__ == "__main__":
	load_model()
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

