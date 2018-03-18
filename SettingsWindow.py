# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_SettingsWindow(object):

	def __init__(self):
		self.image_handler = None

	def set_image_handler(self, imageHandler):
		self.image_handler = imageHandler

	def call_capture_image(self):
		self.image_handler.capture_image()

	def capture_and_exit(self):
		self.image_handler.set_exit_true()

	def setupUi(self, SettingsWindow):
		SettingsWindow.setObjectName(_fromUtf8("SettingsWindow"))
		SettingsWindow.resize(427, 250)
		self.centralwidget = QtGui.QWidget(SettingsWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

		self.show_video_stream_button = QtGui.QPushButton(self.centralwidget)
		self.show_video_stream_button.setGeometry(QtCore.QRect(140, 40, 121, 41))
		self.show_video_stream_button.setObjectName(_fromUtf8("show_video_stream_button"))
		self.show_video_stream_button.clicked.connect(self.call_capture_image)

		self.capture_image_button = QtGui.QPushButton(self.centralwidget)
		self.capture_image_button.setGeometry(QtCore.QRect(140, 90, 121, 41))
		self.capture_image_button.setObjectName(_fromUtf8("capture_image_button"))
		self.capture_image_button.clicked.connect(self.capture_and_exit)

		self.set_threshold_button = QtGui.QPushButton(self.centralwidget)
		self.set_threshold_button.setGeometry(QtCore.QRect(140, 140, 121, 41))
		self.set_threshold_button.setObjectName(_fromUtf8("set_threshold_button"))

		self.exit_button = QtGui.QPushButton(self.centralwidget)
		self.exit_button.setGeometry(QtCore.QRect(140, 190, 121, 41))
		self.exit_button.setObjectName(_fromUtf8("exit_button"))

		SettingsWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtGui.QStatusBar(SettingsWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		SettingsWindow.setStatusBar(self.statusbar)

		self.retranslateUi(SettingsWindow)
		QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

	def retranslateUi(self, SettingsWindow):
		SettingsWindow.setWindowTitle(_translate("SettingsWindow", "SettingsWindow", None))
		self.show_video_stream_button.setText(_translate("SettingsWindow", "Video Stream", None))
		self.capture_image_button.setText(_translate("SettingsWindow", "Capture Image", None))
		self.set_threshold_button.setText(_translate("SettingsWindow", "Set Threshold", None))
		self.exit_button.setText(_translate("SettingsWindow", "Exit", None))


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	SettingsWindow = QtGui.QMainWindow()
	ui = Ui_SettingsWindow()
	ui.setupUi(SettingsWindow)
	SettingsWindow.show()
	sys.exit(app.exec_())

