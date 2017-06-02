__description__ = \
"""
AIC test dialog for pytc-gui.
"""
__author__ = "Hiranmayi Duvvuri"
__date__ = "2017-06-01"

from pytc import util

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets as QW

import sys, logging, copy

class AICTest(QW.QDialog):
    """
    AIC test dialog for pytc-gui.
    """

    def __init__(self, parent):
        """
        Initialize class.
        """
        super().__init__()

        self._fitter_list = parent._fitter_list
        self._fitter = parent._fitter

        self.layout()

    def layout(self):
        """
        Lay out the dialog.
        """
        main_layout = QW.QVBoxLayout(self)
        test_layout = QW.QHBoxLayout()
        button_layout = QW.QVBoxLayout()

        self._fitter_select = QW.QListWidget()
        self._fitter_select.setSelectionMode(QW.QAbstractItemView.ExtendedSelection)

        for k,v in self._fitter_list.items():
            self._fitter_select.addItem(k)

        self._fitter_select.setFixedSize(150, 100)

        ftest_button = QW.QPushButton("Perform AIC Test", self)
        ftest_button.clicked.connect(self.perform_test)

        add_fit_button = QW.QPushButton("Append New Fit", self)
        add_fit_button.clicked.connect(self.add_fitter)

        self._data_out = QW.QTextEdit()
        self._data_out.setReadOnly(True)
        self._data_out.setMinimumWidth(400)

        # redirect stdout to textedit
        #self._temp = sys.stdout
        #sys.stdout = OutputStream()
        #sys.stdout.text_printed.connect(self.read_stdout)

        # add buttons to layout
        button_layout.addWidget(ftest_button)
        button_layout.addWidget(add_fit_button)

        # add widgets to layout
        test_layout.addWidget(self._fitter_select)
        test_layout.addLayout(button_layout)
        main_layout.addLayout(test_layout)
        main_layout.addWidget(self._data_out)

        self.setWindowTitle('AIC Test')

    def add_fitter(self):
        """
        Add current fitter to list for testing
        """
        text, ok = QW.QInputDialog.getText(self, 'Save Fitter', 'Enter Name:')

        # save deepcopy of fitter
        if ok:
            self._fitter_list[text] = copy.deepcopy(self._fitter)
            self._fitter_select.addItem(text)
            print("Fitter " + text + " saved to list.")

    def perform_test(self):
        """
        Take selected objects and use them in AIC test.
        """
        selected = [self._fitter_list[i.text()] for i in self._fitter_select.selectedItems()] 

        if len(selected) < 2:
            err = "You must select at least two fits to compare.\n"
            QW.QMessageBox.warning(self, "warning", err, QW.QMessageBox.Ok)
            return 

        output, plots = util.compare_models(*selected)

        # translate output
        print("\n")
        for o, v in output.items():
            print("Value: ", o)
            print("Best Model: ", v[0])
            print("Weights: ", v[1], "\n")

    @pyqtSlot(str)
    def read_stdout(self, text):
        """
        """
        self._data_out.insertPlainText(text)

    def closeEvent(self, evnt):
        """
        """
        sys.stdout = self._temp
