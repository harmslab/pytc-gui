__description__ = \
"""
message box visual element for pytc gui.
"""
__author__ = "Hiranmayi Duvvuri, Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtCore as QC
from PyQt5 import QtWidgets as QW

import sys

class MessageBox(QW.QScrollArea):
    """
    Widget for holding the message box.
    """

    def __init__(self,parent):
    
        super().__init__()

        self._parent = parent
        self.layout()

    def layout(self):

        self._text = QW.QTextEdit(self._parent)
        self._text.setReadOnly(True)

        self.setWidget(self._text)
        self.setWidgetResizable(True)

        # redirect stdout to the message box
        self._temp = sys.stdout
        sys.stdout = OutputStream()
        sys.stdout.text_printed.connect(self._read_stdout_callback)

    def clear(self):
        """
        Clear the widget.
        """

        self._text.clear()
    
    @QC.pyqtSlot(str)
    def _read_stdout_callback(self, text):
        """
        Write standard out to the main message box, automatically scrolling to
        the bottom.
        """
        self._text.insertPlainText(text)
        self._text.verticalScrollBar().setValue(self._text.verticalScrollBar().maximum())

    @property
    def parent(self):
        return self._parent


class OutputStream(QC.QObject):

	text_printed = QC.pyqtSignal(str)

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
