__description__ = \
"""
Documentation dialog for pytc-gui.
"""
__author__ = "Hiranmayi Duvvuri"
__date__ = "2017-06-01"

from PyQt5 import QtWidgets as QW

import pkg_resources

class Documentation(QW.QDialog):
    """
    Documentation dialog for pytc-gui.
    """
    def __init__(self):
        """
        """
        super().__init__()

        self.layout()

    def layout(self):
        """
        """
        main_layout = QW.QVBoxLayout(self)
        form_layout = QW.QFormLayout()

        pytc_docs = "<a href=\"https://pytc.readthedocs.io/en/latest/\">documentation</a>"
        gui_docs = "<a href=\"https://pytc-gui.readthedocs.io/en/latest/\">documentation</a>"

        pytc_label = QW.QLabel(pytc_docs)
        pytc_label.setOpenExternalLinks(True)

        gui_label = QW.QLabel(gui_docs)
        gui_label.setOpenExternalLinks(True)

        form_layout.addRow(QW.QLabel("pytc:"), pytc_label)
        form_layout.addRow(QW.QLabel("pytc-gui:"), gui_label)

        OK_button = QW.QPushButton("OK", self)
        OK_button.clicked.connect(self.close)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(OK_button)

        self.setWindowTitle("Documentation")
