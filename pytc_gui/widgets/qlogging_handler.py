from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys

class OutputStream(QObject):

	text_printed = pyqtSignal(str)

	def __init__(self):
		"""
		redirect print statements to text edit
		"""
		super().__init__()

	def write(self, text):
		"""
		"""
		self.text_printed.emit(str(text))

	def flush(self):
		"""
		"""
		pass
