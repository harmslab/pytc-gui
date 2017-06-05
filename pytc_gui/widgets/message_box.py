__description__ = \
"""
message box visual element for pytc gui.
"""
__author__ = "Hiranmayi Duvvuri, Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtCore as QC
from PyQt5 import QtWidgets as QW

import sys, os

class MessageBox(QW.QScrollArea):
    """
    Widget for holding the message box.
    """

    def __init__(self,parent,fit):
    
        super().__init__()

        self._parent = parent
        self._fit = fit
        self.layout()

    def layout(self):

        self._main_layout = QW.QVBoxLayout(self)

        self._text = QW.QTextEdit(self)
        self.setWidget(self._text)
        self.setWidgetResizable(True)
        self._text.setReadOnly(True)

        # redirect stdout to the message box
        self._temp = sys.stdout
        sys.stdout = OutputStream()
        sys.stdout.text_printed.connect(self._read_stdout_callback)
        
        self._main_layout.addWidget(self._text)

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
        Write standard out to the text box
        """
   
        # Print everything except blank lines
        text = str(text)
        if text.strip() == "":
            return

        self.text_printed.emit(text) 
        self.text_printed.emit(os.linesep)
       

    def flush(self):
        """
        """
        pass
