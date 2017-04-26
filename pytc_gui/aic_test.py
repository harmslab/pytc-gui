from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pytc import util
import sys

class DoAICTest(QDialog):

	def __init__(self, parent):
		"""
		"""
		super().__init__()

		self._fitter_list = parent._fitter_list

		sys.stdout = OutputStream()

		self.layout()

	def layout(self):
		"""
		"""
		main_layout = QVBoxLayout(self)
		test_layout = QHBoxLayout()

		self._fitter_select = QListWidget()
		self._fitter_select.setSelectionMode(QAbstractItemView.ExtendedSelection)

		for k,v in self._fitter_list.items():
			self._fitter_select.addItem(k)

		self._fitter_select.setFixedSize(150, 100)

		ftest_button = QPushButton("Perform AIC Test", self)
		ftest_button.clicked.connect(self.perform_test)

		self._data_out = QTextEdit()

		test_layout.addWidget(self._fitter_select)
		test_layout.addWidget(ftest_button)
		main_layout.addLayout(test_layout)
		main_layout.addWidget(self._data_out)

	def perform_test(self):
		"""
		take selected objects and use them in f-test
		"""
		selected = [self._fitter_list[i.text()] for i in self._fitter_select.selectedItems()]
		print(selected)
		if len(selected) == 2:	
			output = util.choose_model(*selected)
			self._process.start(output)
		else:
			print("compares 2 models")

	def read_stdout(self):
		"""
		"""
		text = str(self._process.readAllStandardOutput())
		self._data_out.insertText(text)

class OutputStream(QObject):

	def __init__(self):
		"""
		"""
		super().__init__()

		text_printed = pyqtSignal(str)

	def write(self, text):
		"""
		"""
		self.text_printed.emit(str(text))
