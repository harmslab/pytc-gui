"""
pytc GUI using PyQt5
"""
from pytc.global_fit import GlobalFit

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .exp_setup import AddExperimentWindow
from .fit_update import AllExp, PlotBox

from matplotlib.backends.backend_pdf import PdfPages

import sys

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
        button_layout = QHBoxLayout()

        button_tot_width = self.width()

        self._timer = QBasicTimer()
        self._step = 0

        gen_fit = QPushButton("Fit Experiments", self)
        gen_fit.clicked.connect(self.fit_shortcut)
        #gen_fit.setFixedWidth(button_tot_width*1.2)

        self._progress = QProgressBar(self)
        self._progress.setFixedWidth(button_tot_width*0.3)
        button_layout.addWidget(self._progress)
        button_layout.addStretch(2)

        self._plot_frame = PlotBox(self)
        self._exp_frame = AllExp(self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._plot_frame)
        splitter.addWidget(self._exp_frame)
        splitter.setSizes([200, 200])

        main_layout.addWidget(splitter)
        main_layout.addWidget(gen_fit)
        main_layout.addLayout(button_layout)

        self._exp_frame.fit_signal.connect(self.count_progress)

    def clear(self):
        """
        """
        self._plot_frame.clear()
        self._exp_frame.clear()

    def timerEvent(self, e):
        """
        """
        if self._step >= 100:
            self._timer.stop()
            return

        self._step += 1
        print(self._step)
        self._progress.setValue(self._step)

    def count_progress(self):
        """
        """
        curr_length = len(self._exp_frame._slider_list["Local"])+len(self._exp_frame._slider_list["Global"])
        self._progress.setMaximum(curr_length)

    def testing(self):
        """
        """
        print("Sliders: ", self._exp_frame._slider_list)
        print("Global Tracker: ", self._exp_frame._global_tracker)

    def fit_shortcut(self):
        """
        """
        curr_length = len(self._exp_frame._slider_list["Local"])+len(self._exp_frame._slider_list["Global"])
        self._progress.setMaximum(curr_length)
        self._progress.setValue(0)

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

        test = QAction("Test Shit", self)
        test.setShortcut("Ctrl+P")
        test.triggered.connect(self.print_tests)
        fitting_commands.addAction(test)

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

        # add shortcut actions to main window, for qt5 bug
        self.addAction(add_exp)
        self.addAction(fit_exp)
        self.addAction(save_exp)
        self.addAction(new_exp)
        self.addAction(close_window)
        self.addAction(test)

        self._exp = Splitter(self)
        self.setCentralWidget(self._exp)

        self.resize(1000, 600)
        self.move(QApplication.desktop().screen().rect().center()-self.rect().center())
        self.setWindowTitle('pytc')
        self.show()

    def print_tests(self):
        """
        fitting shortcut
        """
        self._exp.testing()

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
            pass

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
            pass

    def close_program(self):
        """
        close window
        """
        self.close()

def main():
    """
    """
    try:
        app = QApplication(sys.argv)
        with open("pytc_gui/style/style.qss") as ss:
            app.setStyleSheet(ss.read())

        pytc_run = Main()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
