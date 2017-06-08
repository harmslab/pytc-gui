__description__ = \
"""
message box visual element for pytc gui.
"""
__author__ = "Hiranmayi Duvvuri, Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtCore as QC
from PyQt5 import QtWidgets as QW

import sys, os

class MessageBox(QW.QTextEdit):
    """
    Widget for holding the message box.
    """

    def __init__(self,parent,fit):
    
        super().__init__()

        self._parent = parent
        self._fit = fit

        self._fit.event_logger.connect(self.write_message)
        self._line_template = "<p style=\"{}\">{}</p><br/><br/>"
        self.setReadOnly(True)

        self._message_format = {"warning":"color:red;",
                                "info":"color:gray; font-style:italic"}

    def write_message(self,message,message_class):
        """
        Write a message to the message window.
        """

        try:
            fmt = self._message_format[message_class]
        except KeyError:
            fmt = ""

        self.insertHtml(self._line_template.format(fmt,message))
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

