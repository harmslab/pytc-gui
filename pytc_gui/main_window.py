__description__ = \
"""
pytc GUI using PyQt5.
"""
__author__ = "Hiranmyai Duvvuri"
__date__ = "2017-01-06"

from pytc.global_fit import GlobalFit

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .exp_setup import AddExperimentWindow
from .visual import ExperimentBox, PlotBox
from .aic_test import DoAICTest
from .help_dialogs import VersionInfo, DocumentationURL
from .options import FitOptions
from .qlogging_handler import OutputStream

from matplotlib.backends.backend_pdf import PdfPages

import sys, pkg_resources, pickle, inspect, copy

class GUIMaster(QWidget):
    """
    Main class that holds all of the fitter sub-widgets.
    """

    def __init__(self, parent):

        super().__init__()

        self._parent = parent

        self._fitter = parent._fitter
        self._fitter_list = parent._fitter_list

        # Create a dictionary of GlobalFitOptions
        fit_args = inspect.getargspec(GlobalFit().fit)
        self._global_fit_options = {arg: param for arg, param
                                    in zip(fit_args.args[1:],fit_args.defaults)}

        # Lay out the widget.
        self.layout()

    def layout(self):
        """
        Create the widget layout.
        """

        # ------------ Plot widget ----------------------- 
        self._plot_box = PlotBox(self)

        # ------------ Experiments widget ----------------
        self._exp_box = ExperimentBox(self)
    
        # ------------ "Do fit" button -------------------
        do_fit_button = QPushButton("Do fit", self)
        do_fit_button.clicked.connect(self.do_fit_callback)

        # -------------- message box ---------------------
        self._message_box = QTextEdit()
        self._message_box.setReadOnly(True)

        scroll = QScrollArea(self)
        scroll.setWidget(self._message_box)
        scroll.setWidgetResizable(True)

        # redirect stdout to the message box
        self._temp = sys.stdout
        sys.stdout = OutputStream()
        sys.stdout.text_printed.connect(self.read_stdout_callback)

        # Split up the main window in a useful way

        # Split window vertically
        v_splitter = QSplitter(Qt.Vertical)
        v_splitter.addWidget(self._plot_box)
        v_splitter.addWidget(scroll)
        v_splitter.setSizes([300, 50])

        # now split horizontally
        h_splitter = QSplitter(Qt.Horizontal)
        h_splitter.addWidget(v_splitter)
        h_splitter.addWidget(self._exp_box)
        h_splitter.setSizes([200, 200])

        # Now add the split up window.
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(h_splitter)
        main_layout.addWidget(do_fit_button)

        # MJH ??? --> what is signaling architecture?
        self._parent.fit_signal.connect(self.fit_signal_update)

    def clear(self):
        """
        Clear the plot and experiment frames.
        """

        self._plot_box.clear()
        self._exp_box.clear()

    def update_fit_options(self, options_dict):
        """
        """
        self._global_fit_options = options_dict

    def do_fit_callback(self):
        """
        """
        self._exp_box.perform_fit(self._global_fit_options)
        self._plot_box.update()

    @pyqtSlot(GlobalFit)
    def fit_signal_update(self, obj):
        """
        """
        self._plot_box._fitter = obj
        self._exp_box._fitter = obj

    @pyqtSlot(str)
    def read_stdout_callback(self, text):
        """
        Wirte standard out to the main message box.
        """
        self._message_box.insertPlainText(text)

    @property
    def parent(self):
        """
        Parent window.
        """
        return self._parent

    @property
    def plot_box(self):
        """
        Main plot box.
        """ 
        return self._plot_box

    @property
    def exp_box(self):
        """
        Main experiment box.
        """
        return self._exp_box

    @property
    def message_box(self):
        """
        Main message box.
        """
        return self._message_box

class MainWindow(QMainWindow):
    """
    Main fitting window. 
    """

    fit_signal = pyqtSignal(GlobalFit)

    def __init__(self):

        super().__init__()

        self._fitter = GlobalFit()
        self._fitter_list = {}
        self._version = pkg_resources.require("pytc-gui")[0].version

        self.layout()

    def layout(self):
        """
        Create the menu bar.
        """

        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        file_menu = menu.addMenu("File")
        fitting_commands = menu.addMenu("Fitting")
        help_menu = menu.addMenu("Help")

        # ------------- Help Menu ----------------------
        prog_info = QAction("About", self)
        prog_info.triggered.connect(self.version_callback)
        help_menu.addAction(prog_info)

        doc_info = QAction("Documentation", self)
        doc_info.triggered.connect(self.docs_callback)
        help_menu.addAction(doc_info)

        # ------------- Fitting Menu -------------------
        fit_exp = QAction("Do fit", self)
        fit_exp.setShortcut("Ctrl+F")
        fit_exp.triggered.connect(self.fit_exp_callback)
        fitting_commands.addAction(fit_exp)

        fitting_commands.addSeparator()

        aic_test = QAction("AIC Test", self)
        aic_test.triggered.connect(self.perform_aic)
        fitting_commands.addAction(aic_test)

        fitting_commands.addSeparator()

        fitting_options = QAction("Fit Options", self)
        fitting_options.triggered.connect(self.fit_options)
        fitting_commands.addAction(fitting_options)

        # ------------------ File Menu ---------------------------
        add_exp = QAction("Add Experiment", self)
        add_exp.setShortcut("Ctrl+Shift+N")
        add_exp.triggered.connect(self.add_file)
        file_menu.addAction(add_exp)

        save_exp = QAction("Export Results", self)
        save_exp.setShortcut("Ctrl+S")
        save_exp.triggered.connect(self.save_file)
        file_menu.addAction(save_exp)

        file_menu.addSeparator()

        save_fitter = QAction("Save Fitter", self)
        save_fitter.setShortcut("Ctrl+Shift+S")
        save_fitter.triggered.connect(self.save_fitter)
        file_menu.addAction(save_fitter)

        open_fitter = QAction("Open Fitter", self)
        open_fitter.setShortcut("Ctrl+O")
        open_fitter.triggered.connect(self.open_fitter)
        file_menu.addAction(open_fitter)

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
        self.addAction(save_fitter)
        self.addAction(open_fitter)

        # Set up central widget
        self._exp = GUIMaster(self)
        self.setCentralWidget(self._exp)

        self.resize(1000, 600)
        self.move(QApplication.desktop().screen().rect().center()-self.rect().center())
        self.setWindowTitle('pytc')
        self.show()

    def docs_callback(self):
        """
        show pop-up with links to documentation for pytc and pytc-gui
        """
        self._doc_info = DocumentationURL()
        self._doc_info.show()

    def version_callback(self):
        """
        show pop-up with version
        """
        self._version = VersionInfo()
        self._version.show()

    def fit_exp_callback(self):
        """
        fitting shortcut
        """
        self._exp.do_fit_callback()

    def add_file(self):
        """
        add a new pytc experiment.
        """
        self._new_exp = AddExperimentWindow(self._fitter, self._exp)
        self._new_exp.show()

    def perform_aic(self):
        """
        do an f-test with saved fitters as options
        """
        self._do_aic = DoAICTest(self)
        self._do_aic.show()

    def fit_options(self):
        """
        Window for fit options
        """
        # Try to show the window -- if it's not created already, make it
        try:
            self._fit_options.show()
        except AttributeError:
            self._fit_options = FitOptions(self._fitter, self._fitter_list)
            self._fit_options.options_signal.connect(self._exp.update_fit_options)
            self._fit_options.show()

    def add_fitter(self):
        """
        save fitter to list for use in aic-test
        """
        text, ok = QInputDialog.getText(self, 'Save Fitter', 'Enter Name:')

        # save deepcopy of fitter
        if ok:
            self._fitter_list[text] = copy.deepcopy(self._fitter)
            print("Fitter " + text + " saved to list. Current List: ")
            print(self._fitter_list)

    def new_exp(self):
        """
        clear everything and start over
        """
        warning_message = QMessageBox.warning(self, "warning!", "Are you sure you want to start a new session?", QMessageBox.Yes | QMessageBox.No)

        if warning_message == QMessageBox.Yes:
            self._exp.clear()
        else:
            pass

    def save_fitter(self):
       """
       save a global_fit object
       """
       file_name, _ = QFileDialog.getSaveFileName(self, "Save Global Fit", "", "Pickle Files (*.pkl);;")
       try:
           pickle.dump([self._fitter, self._version], open(file_name, "wb"))
       except:
           print("fit not saved")
 
    def open_fitter(self):
       """
       open a saved global_fit object
       """
       file_name, _ = QFileDialog.getOpenFileName(self, "Save Global Fit", "", "Pickle Files (*.pkl);;")
       try:
            opened_fitter, version = pickle.load(open(file_name, "rb"))
            if self._version == version:
                self._fitter = opened_fitter
                self.fit_signal.emit(opened_fitter)
            else:
                print("current version is", self._version, " and file version is", version, 
                        ". versions are incompatible.")
       except:
            print("fit can't be opened")

    def save_file(self):
        """
        save out fit data and plot
        """

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Experiment Output", "", "Text Files (*.txt);;CSV Files (*.csv)")
        plot_name = file_name.split(".")[0] + "_plot.pdf"
        corner_plot_name = file_name.split(".")[0] + "_corner_plot.pdf"

        try:
            data_file = open(file_name, "w")
            data_file.write(self._fitter.fit_as_csv)
            data_file.close()

            plot_save = PdfPages(plot_name)
            fig, ax = self._fitter.plot()
            plot_save.savefig(fig)
            plot_save.close()

            plot_save = PdfPages(corner_plot_name)
            fig = self._fitter.corner_plot()
            plot_save.savefig(fig)
            plot_save.close()

        except:
            pass

    def close_program(self):
        """
        close window
        """
        sys.stdout = self._exp._temp
        self.close()

def main():
    """
    Main function, staring GUI.
    """
    version = pkg_resources.require("pytc-gui")[0].version

    try:
        app = QApplication(sys.argv)
        app.setApplicationName("pytc")
        app.setApplicationVersion(version)
        pytc_run = MainWindow()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
