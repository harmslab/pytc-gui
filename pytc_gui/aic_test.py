from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from pytc import util
from .qlogging_handler import OutputStream
import sys, logging, copy

class ModelPlots(QDialog):

    def __init__(self, plots):
        """
        """
        super().__init__()

        self._plots = plots

        self.layout()

    def layout(self):
        """
        """
        main_layout = QHBoxLayout(self)
        tabs = QTabWidget()
        
        for p, i in self._plots:
            fig, ax = p
            plot_fig = FigureCanvas(fig)
            tabs.addTab(plot_fig, "Model {}".format(i))

        main_layout.addWidget(tabs)

class DoAICTest(QDialog):

    def __init__(self, parent):
        """
        """
        super().__init__()

        self._fitter_list = parent._fitter_list
        self._fitter = parent._fitter

        self.layout()

    def layout(self):
        """
        """
        main_layout = QVBoxLayout(self)
        test_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        self._fitter_select = QListWidget()
        self._fitter_select.setSelectionMode(QAbstractItemView.ExtendedSelection)

        for k,v in self._fitter_list.items():
            self._fitter_select.addItem(k)

        self._fitter_select.setFixedSize(150, 100)

        ftest_button = QPushButton("Perform AIC Test", self)
        ftest_button.clicked.connect(self.perform_test)

        add_fit_button = QPushButton("Add Global Fit Obj", self)
        add_fit_button.clicked.connect(self.add_fitter)

        self._data_out = QTextEdit()
        self._data_out.setReadOnly(True)
        self._data_out.setMinimumWidth(400)

        # redirect stdout to textedit
        self._temp = sys.stdout
        sys.stdout = OutputStream()
        sys.stdout.text_printed.connect(self.read_stdout)

        # add buttons to layout
        button_layout.addWidget(ftest_button)
        button_layout.addWidget(add_fit_button)

        # add widgets to layout
        test_layout.addWidget(self._fitter_select)
        test_layout.addLayout(button_layout)
        main_layout.addLayout(test_layout)
        main_layout.addWidget(self._data_out)

    def add_fitter(self):
        """
        add current fitter to list for testing
        """
        text, ok = QInputDialog.getText(self, 'Save Fitter', 'Enter Name:')

        # save deepcopy of fitter
        if ok:
            self._fitter_list[text] = copy.deepcopy(self._fitter)
            self._fitter_select.addItem(text)
            print("Fitter " + text + " saved to list.")

    def perform_test(self):
        """
        take selected objects and use them in f-test
        """
        try:
            selected = [self._fitter_list[i.text()] for i in self._fitter_select.selectedItems()] 
            output, plots = util.compare_models(*selected)
            self._plots = ModelPlots(plots)
            self._plots.show()

            # translate output
            print("\n")
            for o, v in output.items():
                print("Value: ", o)
                print("Best Model: ", v[0])
                print("Weights: ", v[1], "\n")
        except:
            print("Test Failed")

    @pyqtSlot(str)
    def read_stdout(self, text):
        """
        """
        self._data_out.insertPlainText(text)

    def closeEvent(self, evnt):
        """
        """
        sys.stdout = self._temp
