from PyQt5 import QtCore, QtWidgets
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

class Ui_SettingsWindow(object):

	def __init__(self):
		self.image_handler = None
		self.settings_window = None
		self.settings_window_video_open = False

	def set_image_handler(self, imageHandler):
		self.image_handler = imageHandler

	def call_capture_image(self):
		self.settings_window_video_open = True
		self.image_handler.capture_image()


	def call_capture_and_exit(self):
		if (self.settings_window_video_open == True):
			self.image_handler.set_exit_true()
			self.settings_window_video_open = False
		else:
			message_box = QtWidgets.QMessageBox()
			message_box.move(self.settings_window.rect().center())
			message_box.question(message_box, 'Error', "Video Stream not open",
								 QtWidgets.QMessageBox.Ok)


	def call_set_threshold(self):
		self.image_handler.load_captured_image()
		self.image_handler.set_thresholds()
		self.image_handler.crop_and_save()
		self.image_handler.slice_image()
		self.image_handler.create_block_id_threshold_dictionary()

	def call_exit_window(self):
		self.image_handler.close_all_windows()
		self.settings_window.close()

	def setupUi(self, SettingsWindow):
		SettingsWindow.setObjectName(_fromUtf8("SettingsWindow"))
		SettingsWindow.setFixedSize(427, 270)
		self.settings_window = SettingsWindow
		self.centralwidget = QtWidgets.QWidget(SettingsWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

		self.show_video_stream_button = QtWidgets.QPushButton(self.centralwidget)
		self.show_video_stream_button.setGeometry(QtCore.QRect(140, 40, 121, 41))
		self.show_video_stream_button.setObjectName(_fromUtf8("show_video_stream_button"))
		self.show_video_stream_button.clicked.connect(self.call_capture_image)

		self.capture_image_button = QtWidgets.QPushButton(self.centralwidget)
		self.capture_image_button.setGeometry(QtCore.QRect(140, 90, 121, 41))
		self.capture_image_button.setObjectName(_fromUtf8("capture_image_button"))
		self.capture_image_button.clicked.connect(self.call_capture_and_exit)

		self.set_threshold_button = QtWidgets.QPushButton(self.centralwidget)
		self.set_threshold_button.setGeometry(QtCore.QRect(140, 140, 121, 41))
		self.set_threshold_button.setObjectName(_fromUtf8("set_threshold_button"))
		self.set_threshold_button.clicked.connect(self.call_set_threshold)

		self.exit_button = QtWidgets.QPushButton(self.centralwidget)
		self.exit_button.setGeometry(QtCore.QRect(140, 190, 121, 41))
		self.exit_button.setObjectName(_fromUtf8("exit_button"))
		self.exit_button.clicked.connect(self.call_exit_window)

		SettingsWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(SettingsWindow)
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
	app = QtWidgets.QApplication(sys.argv)
	SettingsWindow = QtWidgets.QMainWindow()
	ui = Ui_SettingsWindow()
	ui.setupUi(SettingsWindow)
	SettingsWindow.show()
	sys.exit(app.exec_())

