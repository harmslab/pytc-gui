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
        self._line_template = "<span style=\"{}\">&#9642; {}</span>"
        self.setReadOnly(True)

        self._message_format = {"warning":"color:red;",
                                "info":"color:gray; font-style:italic;",
                                "fit_start":"color:blue; font-weight:bold;",
                                "happy":"color:green; font-weight:bold;",
                                "normal":"color:black;"}

    def write_message(self,message,message_class):
        """
        Write a message to the message window.  If the message is blank, 
        append a new line.
        """

        try:
            fmt = self._message_format[message_class]
        except KeyError:
            fmt = ""

        if message != "":
            self.insertHtml(self._line_template.format(fmt,message))

        self.insertPlainText("\n")
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

        self.update()

    def delete(self):
        """
        Delete with widget.
        """

        self.clear()
        self.setParent(None)  
     
          
        
