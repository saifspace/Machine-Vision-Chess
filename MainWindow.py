# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
sys.path.append('/Users/omgitsmotrix/desktop/finalYearProject/preperation/stockfish_integration')
import os
import chess
import ImageRepresentation

from PyQt4 import QtCore, QtGui
from SettingsWindow import Ui_SettingsWindow
from ImageHandler import ImageHandler

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

	def __init__(self):
		self.ui = Ui_SettingsWindow()
		self.image_handler = ImageHandler()
		self.ui.set_image_handler(self.image_handler)


	def openSettingsWindow(self):
		self.window = QtGui.QMainWindow()
		self.ui.setupUi(self.window)
		self.window.show()

	def call_capture_image(self):
		self.image_handler.captured_image()

	def call_capture_and_exit(self):
		# self.image_handler.set_exit_true()
		self.image_handler.load_captured_image(flag='2')

	def call_iterate_blocks(self):
		piece_square_info = self.image_handler.new_iterate_blocks()

		for s in piece_square_info.keys():
			chess.put(piece_square_info[s], s)

		print chess.ascii()
		setup = chess.get_setup()
		ImageRepresentation.create_image(setup)
		self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "/resources/modifiedChessboard.png"))


	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(799, 557)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

		self.board_image_label = QtGui.QLabel(self.centralwidget)
		self.board_image_label.setGeometry(QtCore.QRect(295, 2, 500, 500))
		self.board_image_label.setFrameShape(QtGui.QFrame.Box)
		self.board_image_label.setObjectName(_fromUtf8("board_image_label"))
		self.board_image_label.setPixmap(QtGui.QPixmap(os.getcwd() + "/resources/chessboard2.png"))

		self.video_button = QtGui.QPushButton(self.centralwidget)
		self.video_button.setGeometry(QtCore.QRect(0, 80, 221, 41))
		self.video_button.setObjectName(_fromUtf8("video_button"))
		self.video_button.clicked.connect(self.call_capture_image)

		self.colour_detect_button = QtGui.QPushButton(self.centralwidget)
		self.colour_detect_button.setEnabled(True)
		self.colour_detect_button.setGeometry(QtCore.QRect(0, 180, 221, 41))
		self.colour_detect_button.setCheckable(False)
		self.colour_detect_button.setAutoDefault(False)
		self.colour_detect_button.setDefault(False)
		self.colour_detect_button.setFlat(False)
		self.colour_detect_button.setObjectName(_fromUtf8("colour_detect_button"))
		self.colour_detect_button.clicked.connect(self.call_iterate_blocks)

		self.ml_detect_button = QtGui.QPushButton(self.centralwidget)
		self.ml_detect_button.setEnabled(True)
		self.ml_detect_button.setGeometry(QtCore.QRect(0, 230, 221, 41))
		self.ml_detect_button.setCheckable(False)
		self.ml_detect_button.setAutoDefault(False)
		self.ml_detect_button.setDefault(False)
		self.ml_detect_button.setFlat(False)
		self.ml_detect_button.setObjectName(_fromUtf8("ml_detect_button"))

		self.settings_button = QtGui.QPushButton(self.centralwidget)
		self.settings_button.setGeometry(QtCore.QRect(0, 30, 221, 41))
		self.settings_button.setObjectName(_fromUtf8("settings_button"))
		self.settings_button.clicked.connect(self.openSettingsWindow)

		self.vertical_line = QtGui.QFrame(self.centralwidget)
		self.vertical_line.setGeometry(QtCore.QRect(230, 0, 21, 421))
		self.vertical_line.setFrameShape(QtGui.QFrame.VLine)
		self.vertical_line.setFrameShadow(QtGui.QFrame.Sunken)
		self.vertical_line.setObjectName(_fromUtf8("vertical_line"))

		self.horizontal_line = QtGui.QFrame(self.centralwidget)
		self.horizontal_line.setGeometry(QtCore.QRect(0, 410, 241, 16))
		self.horizontal_line.setFrameShape(QtGui.QFrame.HLine)
		self.horizontal_line.setFrameShadow(QtGui.QFrame.Sunken)
		self.horizontal_line.setObjectName(_fromUtf8("horizontal_line"))

		self.prediction_text = QtGui.QLineEdit(self.centralwidget)
		self.prediction_text.setGeometry(QtCore.QRect(80, 440, 141, 31))
		self.prediction_text.setText(_fromUtf8(""))
		self.prediction_text.setObjectName(_fromUtf8("prediction_text"))
		self.prediction_label = QtGui.QLabel(self.centralwidget)
		self.prediction_label.setGeometry(QtCore.QRect(10, 440, 71, 31))

		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Arial"))
		font.setPointSize(14)
		font.setBold(False)
		font.setItalic(False)
		font.setWeight(50)

		self.prediction_label.setFont(font)
		self.prediction_label.setObjectName(_fromUtf8("prediction_label"))

		self.quit_button = QtGui.QPushButton(self.centralwidget)
		self.quit_button.setEnabled(True)
		self.quit_button.setGeometry(QtCore.QRect(0, 330, 221, 41))
		self.quit_button.setCheckable(False)
		self.quit_button.setAutoDefault(False)
		self.quit_button.setDefault(False)
		self.quit_button.setFlat(False)
		self.quit_button.setObjectName(_fromUtf8("quit_button"))

		self.capture_image_button = QtGui.QPushButton(self.centralwidget)
		self.capture_image_button.setGeometry(QtCore.QRect(0, 130, 221, 41))
		self.capture_image_button.setObjectName(_fromUtf8("capture_image_button"))
		self.capture_image_button.clicked.connect(self.call_capture_and_exit)

		self.predict_button = QtGui.QPushButton(self.centralwidget)
		self.predict_button.setEnabled(True)
		self.predict_button.setGeometry(QtCore.QRect(0, 280, 221, 41))
		self.predict_button.setCheckable(False)
		self.predict_button.setAutoDefault(False)
		self.predict_button.setDefault(False)
		self.predict_button.setFlat(False)
		self.predict_button.setObjectName(_fromUtf8("predict_button"))

		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtGui.QStatusBar(MainWindow)
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


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

