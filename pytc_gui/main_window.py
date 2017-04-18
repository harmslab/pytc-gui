"""
pytc GUI using qtpy bindings
"""
from pytc.global_fit import GlobalFit

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .exp_setup import AddExperimentWindow
from .fit_update import AllExp, PlotBox

from matplotlib.backends.backend_pdf import PdfPages

import pickle

class Splitter(QWidget):
    """
    hold main experiment based widgets
    """

    def __init__(self, parent):
        super().__init__()

        self._fitter = parent._fitter

        self.layout()

    def layout(self):
        """
        """
        main_layout = QVBoxLayout(self)
        self._plot_frame = PlotBox(self)
        self._exp_frame = AllExp(self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._plot_frame)
        splitter.addWidget(self._exp_frame)
        splitter.setSizes([200, 200])

        main_layout.addWidget(splitter)

        gen_fit = QPushButton("Fit Experiments", self)
        gen_fit.clicked.connect(self.fit_shortcut)
        main_layout.addWidget(gen_fit)

    def clear(self):
        """
        """
        self._plot_frame.clear()
        self._exp_frame.clear()

    def fit_shortcut(self):
        """
        """
        self._exp_frame.perform_fit()
        self._plot_frame.update()

class Main(QMainWindow):
    """
    """
    def __init__(self):
        super().__init__()

        self._fitter = GlobalFit()

        self.layout()

    def layout(self):
        """
        make the menu bar
        """
        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        file_menu = menu.addMenu("File")
        fitting_commands = menu.addMenu("Fitting")

        fit_exp = QAction("Fit Experiments", self)
        fit_exp.setShortcut("Ctrl+F")
        fit_exp.triggered.connect(self.fit_exp)
        fitting_commands.addAction(fit_exp)

        add_exp = QAction("Add Experiment", self)
        add_exp.setShortcut("Ctrl+Shift+N")
        add_exp.triggered.connect(self.add_file)
        file_menu.addAction(add_exp)

        save_exp = QAction("Export Results", self)
        save_exp.setShortcut("Ctrl+S")
        save_exp.triggered.connect(self.save_file)
        file_menu.addAction(save_exp)

        file_menu.addSeparator()

        new_exp = QAction("New Session", self)
        new_exp.setShortcut("Ctrl+N")
        new_exp.triggered.connect(self.new_exp)
        file_menu.addAction(new_exp)

        close_window = QAction("Close Window", self)
        close_window.setShortcut("Ctrl+W")
        close_window.triggered.connect(self.close_program)
        file_menu.addAction(close_window)

        self._exp = Splitter(self)
        self.setCentralWidget(self._exp)

        self.resize(1000, 600)
        self.move(QApplication.desktop().screen().rect().center()-self.rect().center())
        self.setWindowTitle('pytc')
        self.show()

    def print_exp(self):
        """
        testing, check pytc experiments loading
        """
        print(self._fitter.experiments, self._fitter.global_param)

    def fit_exp(self):
        """
        fitting shortcut
        """
        self._exp.fit_shortcut()

    def add_file(self):
        """
        add a new pytc experiment.
        """
        self._new_exp = AddExperimentWindow(self._fitter, self._exp)
        self._new_exp.show()

    def new_exp(self):
        """
        clear everything and start over
        """
        warning_message = QMessageBox.warning(self, "warning!", "Are you sure you want to start a new session?", QMessageBox.Yes | QMessageBox.No)

        if warning_message == QMessageBox.Yes:
            self._exp.clear()
        else:
            print("don't start over!")

    def save_file(self):
        """
        save out fit data and plot
        """

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Experiment Output", "", "Text Files (*.txt);;CSV Files (*.csv)")
        plot_name = file_name.split(".")[0] + "_plot.pdf"

        try:
            data_file = open(file_name, "w")
            data_file.write(self._fitter.fit_as_csv)
            data_file.close()

            plot_save = PdfPages(plot_name)
            fig, ax = self._fitter.plot()
            plot_save.savefig(fig)
            plot_save.close()
        except:
            print("save failed")

    def close_program(self):
        """
        close window
        """
        self.close()
