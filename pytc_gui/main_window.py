"""
pytc GUI using PyQt5
"""
from pytc.global_fit import GlobalFit

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .exp_setup import AddExperimentWindow
from .fit_update import AllExp, PlotBox
from .aic_test import DoAICTest
from .help_dialogs import VersionInfo, DocumentationURL
from .options import FitOptions
from .qlogging_handler import OutputStream

from matplotlib.backends.backend_pdf import PdfPages

import sys, pkg_resources, pickle, inspect, copy

class Splitter(QWidget):
    """
    hold main experiment based widgets
    """

    def __init__(self, parent):
        super().__init__()

        self._fitter = parent._fitter
        self._parent = parent

        fit_args = inspect.getargspec(GlobalFit().fit)
        self._options_dict = {arg: param for arg, param in zip(fit_args.args[1:], fit_args.defaults)}

        self.layout()

    def layout(self):
        """
        """
        main_layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        gen_fit = QPushButton("Fit Experiments", self)
        gen_fit.clicked.connect(self.fit_shortcut)

        self._plot_frame = PlotBox(self)
        self._exp_frame = AllExp(self)

        # set up message box 
        scroll = QScrollArea(self)
        self._message_box = QTextEdit()
        self._message_box.setReadOnly(True)
        scroll.setWidget(self._message_box)
        scroll.setWidgetResizable(True)

        # redirect stdout
        self._temp = sys.stdout
        sys.stdout = OutputStream()
        sys.stdout.text_printed.connect(self.read_stdout)

        # set up splitters
        splitter = QSplitter(Qt.Horizontal)
        v_splitter = QSplitter(Qt.Vertical)
        v_splitter.addWidget(self._plot_frame)
        v_splitter.addWidget(scroll)
        v_splitter.setSizes([300, 50])

        splitter.addWidget(v_splitter)
        splitter.addWidget(self._exp_frame)
        splitter.setSizes([200, 200])

        main_layout.addWidget(splitter)
        main_layout.addWidget(gen_fit)

        self._parent.new_fitter.connect(self.fit_signal_update)

    def clear(self):
        """
        """
        self._plot_frame.clear()
        self._exp_frame.clear()

    def update_fit_options(self, options_dict):
        """
        """
        self._options_dict = options_dict

    def fit_shortcut(self):
        """
        """
        self._exp_frame.perform_fit(self._options_dict)
        self._plot_frame.update()

    @pyqtSlot(GlobalFit)
    def fit_signal_update(self, obj):
        """
        """
        self._plot_frame._fitter = obj
        self._exp_frame._fitter = obj

    @pyqtSlot(str)
    def read_stdout(self, text):
        """
        """
        self._message_box.insertPlainText(text)

class Main(QMainWindow):
    """
    """
    new_fitter = pyqtSignal(GlobalFit)

    def __init__(self):
        super().__init__()

        self._fitter = GlobalFit()
        self._fitter_list = {}
        self._version = pkg_resources.require("pytc-gui")[0].version

        self.layout()

    def layout(self):
        """
        make the menu bar
        """
        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        file_menu = menu.addMenu("File")
        fitting_commands = menu.addMenu("Fitting")
        help_menu = menu.addMenu("Help")

        # Help Menu
        prog_info = QAction("About", self)
        prog_info.triggered.connect(self.version)
        help_menu.addAction(prog_info)

        doc_info = QAction("Documentation", self)
        doc_info.triggered.connect(self.docs)
        help_menu.addAction(doc_info)

        # Fitting Menu
        fit_exp = QAction("Fit Experiments", self)
        fit_exp.setShortcut("Ctrl+F")
        fit_exp.triggered.connect(self.fit_exp)
        fitting_commands.addAction(fit_exp)

        fitting_commands.addSeparator()

        add_fitter = QAction("Add Fitter to List", self)
        add_fitter.triggered.connect(self.add_fitter)
        fitting_commands.addAction(add_fitter)

        aic_test = QAction("AIC Test", self)
        aic_test.triggered.connect(self.perform_aic)
        fitting_commands.addAction(aic_test)

        fitting_commands.addSeparator()

        fitting_options = QAction("Fit Options", self)
        fitting_options.triggered.connect(self.fit_options)
        fitting_commands.addAction(fitting_options)

        test = QAction("Test Shit", self)
        test.setShortcut("Ctrl+P")
        test.triggered.connect(self.print_tests)
        fitting_commands.addAction(test)

        # File Menu
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

        self.addAction(test)

        # Set up central widget
        self._exp = Splitter(self)
        self.setCentralWidget(self._exp)

        self.resize(1000, 600)
        self.move(QApplication.desktop().screen().rect().center()-self.rect().center())
        self.setWindowTitle('pytc')
        self.show()

    def docs(self):
        """
        show pop-up with links to documentation for pytc and pytc-gui
        """
        self._doc_info = DocumentationURL()
        self._doc_info.show()

    def version(self):
        """
        show pop-up with version
        """
        self._version = VersionInfo()
        self._version.show()

    def print_tests(self):
        """
        """
        print(self._fitter_list)

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

    def perform_aic(self):
        """
        do an f-test with saved fitters as options
        """
        self._do_aic = DoAICTest(self)
        self._do_aic.show()

    def fit_options(self):
        """
        """
        self._fit_options = FitOptions(self._fitter)
        self._fit_options.options_signal.connect(self._exp.update_fit_options)
        self._fit_options.show()

    def add_fitter(self):
        """
        save fitter to list for use in f-test
        """
        text, ok = QInputDialog.getText(self, 'Save Fitter', 'Enter Name:')

        # save deepcopy of fitter
        if ok:
            self._fitter_list[text] = copy.deepcopy(self._fitter)

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
                self.new_fitter.emit(opened_fitter)
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
        sys.stdout = self._exp._temp
        self.close()

def main():
    """
    """
    version = pkg_resources.require("pytc-gui")[0].version

    try:
        app = QApplication(sys.argv)
        app.setApplicationName("pytc")
        app.setApplicationVersion(version)
        pytc_run = Main()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
