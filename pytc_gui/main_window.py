__description__ = \
"""
pytc GUI using PyQt5.
"""
__author__ = "Hiranmyai Duvvuri"
__date__ = "2017-01-06"

from . import dialogs, widgets
from .fit_container import FitContainer

from pytc.global_fit import GlobalFit

from PyQt5.QtCore import pyqtSignal 
from PyQt5 import QtWidgets as QW

from matplotlib.backends.backend_pdf import PdfPages
import sys, pkg_resources, pickle

import os

class MainWindow(QW.QMainWindow):
    """
    Main fitting window. 
    """

    def __init__(self,app):

        super().__init__()

        self._app = app
        self._fit = FitContainer()

        self._fitter_list = {}
        self._version = pkg_resources.require("pytc-gui")[0].version

        self._accept_exit_program = False

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
        prog_info = QW.QAction("About", self)
        prog_info.triggered.connect(self.about_dialog)
        help_menu.addAction(prog_info)

        doc_info = QW.QAction("Documentation", self)
        doc_info.triggered.connect(self.docs_dialog)
        help_menu.addAction(doc_info)

        # ------------- Fitting Menu -------------------
        do_fit = QW.QAction("Do fit", self)
        do_fit.setShortcut("Ctrl+F")
        do_fit.triggered.connect(self.do_fit_callback)
        fitting_commands.addAction(do_fit)

        fitting_commands.addSeparator()

        aic_test = QW.QAction("AIC Test", self)
        aic_test.triggered.connect(self.aic_dialog)
        fitting_commands.addAction(aic_test)

        fitting_commands.addSeparator()

        fitting_options = QW.QAction("Fit Options", self)
        fitting_options.triggered.connect(self.fit_options_dialog)
        fitting_commands.addAction(fitting_options)

        # ------------------ File Menu ---------------------------
        add_exp = QW.QAction("Add Experiment", self)
        add_exp.setShortcut("Ctrl+Shift+N")
        add_exp.triggered.connect(self.add_exp_dialog)
        file_menu.addAction(add_exp)

        export_results = QW.QAction("Export Results", self)
        export_results.setShortcut("Ctrl+S")
        export_results.triggered.connect(self.export_results_dialog)
        file_menu.addAction(export_results)

        file_menu.addSeparator()

        #save_fitter = QW.QAction("Save Fitter", self)
        #save_fitter.setShortcut("Ctrl+Shift+S")
        #save_fitter.triggered.connect(self.save_fitter_dialog)
        #file_menu.addAction(save_fitter)

        #open_fitter = QW.QAction("Open Fitter", self)
        #open_fitter.setShortcut("Ctrl+O")
        #open_fitter.triggered.connect(self.open_fitter_dialog)
        #file_menu.addAction(open_fitter)

        file_menu.addSeparator()

        #new_session = QW.QAction("New Session", self)
        #new_session.setShortcut("Ctrl+N")
        #new_session.triggered.connect(self.new_session_callback)
        #file_menu.addAction(new_session)

        close_window = QW.QAction("Exit", self)
        close_window.setShortcut("Ctrl+W")
        close_window.triggered.connect(self.close_program_callback)
        file_menu.addAction(close_window)

        # add shortcut actions to main window, for qt5 bug
        self.addAction(add_exp)
        self.addAction(do_fit)
        self.addAction(export_results)
        #self.addAction(new_session)
        self.addAction(close_window)
        #self.addAction(save_fitter)
        #self.addAction(open_fitter)

        # Set up central widget
        self._main_widgets = widgets.MainWidgets(self,self._fit)
        self.setCentralWidget(self._main_widgets)

        self.resize(1000, 600)
        self.move(QW.QApplication.desktop().screen().rect().center()-self.rect().center())
        self.setWindowTitle('pytc')
        self.show()

    def docs_dialog(self):
        """
        Open a transient documentation dialog.
        """
        self._tmp = dialogs.Documentation()
        self._tmp.show()

    def about_dialog(self):
        """
        Open a transient about dialog.
        """
        self._tmp = dialogs.About()
        self._tmp.show()

    def add_exp_dialog(self):
        """
        Open a transient dialog for adding a new experiment.
        """

        self._tmp = dialogs.AddExperiment(self._fit)
        self._tmp.show()

    def aic_dialog(self):
        """
        Load persistent dialog box for doing AIC calculation.
        """
    
        try:
            self._aic_dialog.show()
        except AttributeError:
            self._aic_dialog = dialogs.AICTest(self,self._fit)
            self._aic_dialog.show()
    
        self._aic_dialog.raise_()

    def fit_options_dialog(self):
        """
        Load persistent dialog for setting fit options.
        """

        # Try to show the window -- if it's not created already, make it
        try:
            self._fit_options_dialog.show()
        except AttributeError:
            self._fit_options_dialog = dialogs.FitOptions(self, self._fit)
            self._fit_options_dialog.show()

        self._fit_options_dialog.raise_()

    def save_fitter_dialog(self):
        """
        Open a transient dialog for saving a fit object.
        """

        file_name, _ = QW.QFileDialog.getSaveFileName(self, "Save Global Fit", "", "Pickle Files (*.pkl);;")
        pickle.dump([self._fit,self._version], open(file_name, "wb"))
 
    def open_fitter_dialog(self):
        """
        Open a transient dialog for opening a saved fit object.
        """
        file_name, _ = QW.QFileDialog.getOpenFileName(self, "Save Global Fit", "", "Pickle Files (*.pkl);;")

        opened_fitter, version = pickle.load(open(file_name, "rb"))
        if self._version == version:
            self._fit = opened_fitter
            self._fit.emit_changed()
        else:
            err = "Could not load fit. Current version is {}, but file version is {}.".format(self._version,version)
            error_message = QW.QMessageBox.warning(self,err, QW.QMessageBox.Ok)

    def export_results_dialog(self):
        """
        Bring up transient dialog for exporting results.
        """

        out_dir, _ = QW.QFileDialog.getSaveFileName(self, "Export Experiment Output", "", "*")

        try:

            os.mkdir(out_dir) 

            data_file = open(os.path.join(out_dir,"fit_param.csv"), "w")
            data_file.write(self._fit.fitter.fit_as_csv)
            data_file.close()

            plot_save = PdfPages(os.path.join(out_dir,"main_plot.pdf"))
            fig, ax = self._fit.fitter.plot()
            plot_save.savefig(fig)
            plot_save.close()

            plot_save = PdfPages(os.path.join(out_dir,"corner_plot.pdf"))
            fig = self._fit.fitter.corner_plot()
            plot_save.savefig(fig)
            plot_save.close()

            log_save = open(os.path.join(out_dir,"session.log"),"w")
            spew = self._main_widgets.message_box.toPlainText()
            log_save.write(spew)
            log_save.close()


        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            err = template.format(type(ex).__name__,ex.args)
            error_message = QW.QMessageBox.warning(self,err, QW.QMessageBox.Ok)

    def do_fit_callback(self):
        """
        Do the fit.
        """
        self._main_widgets.do_fit_callback()


    def new_session_callback(self):
        """
        Start a competely new session.
        """

        warning = "Are you sure you want to start a new session?"
        warning_message = QW.QMessageBox.warning(self, "warning!",warning, 
                                                 QW.QMessageBox.Yes | QW.QMessageBox.No)
        if warning_message == QW.QMessageBox.Yes:
            self._fit.clear()
            self._fit.fitter_list = {}
            self._main_widgets.clear()

    def close_program_callback(self):
        """
        Close the program out.
        """

        ret = QW.QMessageBox.Ok
        if not self._accept_exit_program:
            if len(self._fit.experiments) > 0:
                m = QW.QMessageBox()
                m.setText("Are you sure you want to exit?")
                m.setIcon(QW.QMessageBox.Warning)
                m.setStandardButtons(QW.QMessageBox.Ok  | QW.QMessageBox.Cancel)
                m.setDefaultButton(QW.QMessageBox.Cancel)
                ret = m.exec_()

        if ret == QW.QMessageBox.Ok:
            self._accept_exit_program = True
            self._main_widgets.clear()
            self._app.instance().closeAllWindows()
        else:
            self._accept_exit_program = False

    def closeEvent(self,event):
        """
        Override closeEvent so all windows close and clean up.
        """
        self.close_program_callback()

        if self._accept_exit_program:
            event.accept()
        else:
            event.ignore()
 

def main():
    """
    Main function, staring GUI.
    """
    version = pkg_resources.require("pytc-gui")[0].version

    try:
        app = QW.QApplication(sys.argv)
        app.setApplicationName("pytc")
        app.setApplicationVersion(version)
        pytc_run = MainWindow(app)
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
