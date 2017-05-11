from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from pytc import util
from .qlogging_handler import OutputStream
import sys, logging

class ModelPlots(QDialog):

    def __init__(self, plot1, plot2):
        """
        """
        super().__init__()

        self._plot1 = plot1
        self._plot2 = plot2

        self.layout()

    def layout(self):
        """
        """
        main_layout = QHBoxLayout(self)

        fig1, ax1 = self._plot1
        fig2, ax2 = self._plot2

        plot_fig1 = FigureCanvas(fig1)
        plot_fig2 = FigureCanvas(fig2)

        main_layout.addWidget(plot_fig1)
        main_layout.addWidget(plot_fig2)

class DoAICTest(QDialog):

    def __init__(self, parent):
        """
        """
        super().__init__()

        self._fitter_list = parent._fitter_list

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
        self._data_out.setReadOnly(True)
        self._data_out.setMinimumWidth(400)

        # redirect stdout to textedit
        self._temp = sys.stdout
        sys.stdout = OutputStream()
        sys.stdout.text_printed.connect(self.read_stdout)

        test_layout.addWidget(self._fitter_select)
        test_layout.addWidget(ftest_button)
        main_layout.addLayout(test_layout)
        main_layout.addWidget(self._data_out)

    def perform_test(self):
        """
        take selected objects and use them in f-test
        """
        selected = [self._fitter_list[i.text()] for i in self._fitter_select.selectedItems()]
        if len(selected) == 2:  
            output, plot1, plot2 = util.choose_model(*selected)
            self._plots = ModelPlots(plot1, plot2)
            self._plots.show()
        else:
            print("compares 2 models")

    @pyqtSlot(str)
    def read_stdout(self, text):
        """
        """
        self._data_out.insertPlainText(text)

    def closeEvent(self, evnt):
        """
        """
        sys.stdout = self._temp
