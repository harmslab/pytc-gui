from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pkg_resources

class About(QDialog):

	def __init__(self):
		"""
		"""
		super().__init__()

		self.layout()

	def layout(self):
		"""
		"""
		main_layout = QVBoxLayout(self)
		form_layout = QFormLayout()

		version = pkg_resources.require("pytc-gui")[0].version

		name_label = QLabel("pytc: GUI")
		name_font = name_label.font()
		name_font.setPointSize(20)
		name_label.setFont(name_font)
		name_label.setAlignment(Qt.AlignCenter)

		version_label = QLabel("Version " + version)
		version_font = version_label.font()
		version_font.setPointSize(14)
		version_label.setFont(version_font)
		version_label.setAlignment(Qt.AlignCenter)

		author_info = QLabel("Hiranmayi Duvvuri, Mike Harms")
		author_font = author_info.font()
		author_font.setPointSize(10)
		author_info.setFont(author_font)

		OK_button = QPushButton("OK", self)
		OK_button.clicked.connect(self.close)

		main_layout.addWidget(name_label)
		main_layout.addWidget(version_label)
		main_layout.addWidget(author_info)
		main_layout.addWidget(OK_button)

		self.setWindowTitle("About")

