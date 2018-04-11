# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
import os

# path for Windows
sys.path.append(os.getcwd() + '\Libraries\chess_helper')

import chess
import stockfishchess as engine
import ImageRepresentation
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


	def openSettingsWindow(self):
		self.window = QtWidgets.QMainWindow()
		self.ui.setupUi(self.window)
		self.window.show()

	def call_capture_image(self):
		self.image_handler.capture_image()

	def call_capture_and_exit(self):
		self.image_handler.set_exit_true()
		self.image_handler.load_captured_image(flag='win')

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
		engine.set_fen("r1b1kr2/2ppQ1pp/p4p2/5p2/1pB5/5PPN/PP3K1P/RNB1R3 b - - 0 2")
		response = engine.best_move()
		self.prediction_text.setText(response)


	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.setFixedSize(799, 695)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

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
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.a_label.setFont(font)
		self.a_label.setObjectName("a_label")
		self.b_label = QtWidgets.QLabel(self.centralwidget)
		self.b_label.setGeometry(QtCore.QRect(390, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.b_label.setFont(font)
		self.b_label.setObjectName("b_label")
		self.c_label = QtWidgets.QLabel(self.centralwidget)
		self.c_label.setGeometry(QtCore.QRect(450, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.c_label.setFont(font)
		self.c_label.setObjectName("c_label")
		self.d_label = QtWidgets.QLabel(self.centralwidget)
		self.d_label.setGeometry(QtCore.QRect(510, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.d_label.setFont(font)
		self.d_label.setObjectName("d_label")
		self.e_label = QtWidgets.QLabel(self.centralwidget)
		self.e_label.setGeometry(QtCore.QRect(580, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.e_label.setFont(font)
		self.e_label.setObjectName("e_label")
		self.f_label = QtWidgets.QLabel(self.centralwidget)
		self.f_label.setGeometry(QtCore.QRect(640, 510, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.f_label.setFont(font)
		self.f_label.setObjectName("f_label")
		self.g_label = QtWidgets.QLabel(self.centralwidget)
		self.g_label.setGeometry(QtCore.QRect(700, 510, 16, 21))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.g_label.setFont(font)
		self.g_label.setObjectName("g_label")
		self.h_label = QtWidgets.QLabel(self.centralwidget)
		self.h_label.setGeometry(QtCore.QRect(760, 510, 16, 21))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.h_label.setFont(font)
		self.h_label.setObjectName("h_label")
		self.one_label = QtWidgets.QLabel(self.centralwidget)
		self.one_label.setGeometry(QtCore.QRect(280, 460, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.one_label.setFont(font)
		self.one_label.setObjectName("one_label")
		self.two_label = QtWidgets.QLabel(self.centralwidget)
		self.two_label.setGeometry(QtCore.QRect(280, 400, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.two_label.setFont(font)
		self.two_label.setObjectName("two_label")
		self.three_label = QtWidgets.QLabel(self.centralwidget)
		self.three_label.setGeometry(QtCore.QRect(280, 340, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.three_label.setFont(font)
		self.three_label.setObjectName("three_label")
		self.four_label = QtWidgets.QLabel(self.centralwidget)
		self.four_label.setGeometry(QtCore.QRect(280, 280, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.four_label.setFont(font)
		self.four_label.setObjectName("four_label")
		self.five_label = QtWidgets.QLabel(self.centralwidget)
		self.five_label.setGeometry(QtCore.QRect(280, 220, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.five_label.setFont(font)
		self.five_label.setObjectName("five_label")
		self.six_label = QtWidgets.QLabel(self.centralwidget)
		self.six_label.setGeometry(QtCore.QRect(280, 160, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.six_label.setFont(font)
		self.six_label.setObjectName("six_label")
		self.seven_label = QtWidgets.QLabel(self.centralwidget)
		self.seven_label.setGeometry(QtCore.QRect(280, 90, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.seven_label.setFont(font)
		self.seven_label.setObjectName("seven_label")
		self.eight_label = QtWidgets.QLabel(self.centralwidget)
		self.eight_label.setGeometry(QtCore.QRect(280, 20, 16, 16))
		font = QtGui.QFont()
		font.setFamily("Helvetica")
		font.setPointSize(18)
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
		self.piece_combo_box.addItems(['Piece Type','wpawn', 'wrook', 'wknight', 'wbishop', 'wking', 'wqueen',
									   'bpawn', 'brook', 'bknight', 'bbishop', 'bking', 'bqueen'])

		self.second_detect_button = QtWidgets.QPushButton(self.manual_input_frame)
		self.second_detect_button.setGeometry(QtCore.QRect(140, 50, 151, 31))
		self.second_detect_button.setObjectName("second_detect_button")
		self.manual_fix_button = QtWidgets.QPushButton(self.manual_input_frame)
		self.manual_fix_button.setGeometry(QtCore.QRect(140, 80, 151, 31))
		self.manual_fix_button.setObjectName("manual_fix_button")
		self.fix_title_label = QtWidgets.QLabel(self.manual_input_frame)
		self.fix_title_label.setGeometry(QtCore.QRect(90, 10, 100, 16))
		self.fix_title_label.setObjectName("fix_title_label")

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

		self.second_detect_button.setText(_translate("MainWindow", "ML: Second Detect", None))
		self.manual_fix_button.setText(_translate("MainWindow", "Manual Fix", None))
		self.fix_title_label.setText(_translate("MainWindow", "Fix Chessboard", None))

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

if __name__ == "__main__":
	load_model()
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

