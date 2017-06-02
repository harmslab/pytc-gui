from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pkg_resources

class Documentation(QDialog):

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

		pytc_docs = "<a href=\"https://pytc.readthedocs.io/en/latest/\">documentation</a>"
		gui_docs = "<a href=\"https://pytc-gui.readthedocs.io/en/latest/\">documentation</a>"

		pytc_label = QLabel(pytc_docs)
		pytc_label.setOpenExternalLinks(True)

		gui_label = QLabel(gui_docs)
		gui_label.setOpenExternalLinks(True)

		form_layout.addRow(QLabel("pytc:"), pytc_label)
		form_layout.addRow(QLabel("pytc-gui:"), gui_label)

		OK_button = QPushButton("OK", self)
		OK_button.clicked.connect(self.close)

		main_layout.addLayout(form_layout)
		main_layout.addWidget(OK_button)

		self.setWindowTitle("Documentation")
