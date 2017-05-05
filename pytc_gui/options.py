from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pytc import GlobalFit

import inspect

class FitOptions(QDialog):

	options_signal = pyqtSignal(dict)

	def __init__(self, fitter):
		"""
		"""
		super().__init__()
		self._fitter = fitter
		self._bootstrap_var = {}

		self.layout()

	def layout(self):
		"""
		"""
		main_layout = QVBoxLayout(self)

		radio_group = QHBoxLayout()
		self._bootstrap_widget = QFrame()
		bootstrap_options = QFormLayout(self._bootstrap_widget)

		fit_header = QLabel("Set Options: ")

		# radio buttons for choosing fit type
		jacobian_fit = QRadioButton("Jacobian")
		jacobian_fit.toggled.connect(self.select_fit)
		jacobian_fit.setChecked(True)

		bootstrap_fit = QRadioButton("Bootstrap")
		bootstrap_fit.toggled.connect(self.select_fit)

		radio_group.addWidget(jacobian_fit)
		radio_group.addWidget(bootstrap_fit)

		OK_button = QPushButton("Update", self)
		OK_button.clicked.connect(self.initialize)

		# widgets for bootstrap options
		fit_args = inspect.getargspec(GlobalFit().fit)
		self._bootstrap_default = {arg: param for arg, param in zip(fit_args.args[1:], fit_args.defaults)}

		for n, v in self._bootstrap_default.items():
			label_name = str(n).replace("_", " ") + ": "
			label = QLabel(label_name.title(), self)
			entry = QLineEdit(self)
			entry.setText(str(v))
			self._bootstrap_var[n] = entry

			bootstrap_options.addRow(label, entry)

		main_layout.addWidget(fit_header)
		main_layout.addLayout(radio_group)
		main_layout.addWidget(self._bootstrap_widget)
		main_layout.addWidget(OK_button)

		self.setWindowTitle("Fit Options")

	def select_fit(self):
		"""
		"""
		b = self.sender()

		if b.text() == "Bootstrap" and b.isChecked():
			self._bootstrap_widget.show()
		elif b.text() == "Jacobian" and b.isChecked():
			self._bootstrap_widget.hide()
			for n, v in self._bootstrap_var.items():
				v.setText(str(self._bootstrap_default[n]))
			self.adjustSize()

	def initialize(self):
		"""
		"""
		bootstrap_val = {}
		for n, v in self._bootstrap_var.items():
			if '.' in v.text():
				val = float(v.text())
			else:
				val = int(v.text())

			bootstrap_val[n] = val
			
		self.options_signal.emit(bootstrap_val)
