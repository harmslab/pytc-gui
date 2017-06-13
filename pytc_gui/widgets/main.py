__description__ = \
"""
"""
__author__ = "Hiranmyai Duvvuri"
__date__ = "2017-01-06"

from .plot_box import PlotBox
from .message_box import MessageBox
from .experiment_box import ExperimentBox
from .parameter_box import ParameterBox

import pytc

from PyQt5 import QtCore as QC
from PyQt5 import QtWidgets as QW

import inspect

class MainWidgets(QW.QWidget):
    """
    Main class that holds all of the fitter sub-widgets.
    """

    def __init__(self, parent, fit):

        super().__init__()

        self._parent = parent
        self._fit = fit

        # Create a dictionary of GlobalFitOptions
        fit_args = inspect.getargspec(pytc.global_fit.GlobalFit().fit)
        self._global_fit_options = {arg: param for arg, param
                                    in zip(fit_args.args[1:],fit_args.defaults)}

        # Lay out the widget.
        self.layout()

    def layout(self):
        """
        Create the widget layout.
        """

        # ------------ Plot widget ----------------------- 
        self._plot_box = PlotBox(self,self._fit)

        # ------------ Message box -----------------------
        self._message_box = MessageBox(self,self._fit)

        # ------------ Experiments widget ----------------
        self._exp_box = ExperimentBox(self,self._fit)
   
        # ------------ Parameters widget -----------------
        self._param_box = ParameterBox(self,self._fit)

        self._core_widgets = [self._plot_box,
                              self._message_box,
                              self._exp_box,
                              self._param_box]

        # ------------ "Do fit" button -------------------
        self._do_fit_button = QW.QPushButton("Do fit", self)
        self._do_fit_button.clicked.connect(self.do_fit_callback)

        # Split up the main window in a useful way

        # Left column
        left_column = QW.QSplitter(QC.Qt.Vertical)
        left_column.addWidget(self._plot_box)
        left_column.addWidget(self._exp_box)
        left_column.setSizes([200, 50])

        # right column
        right_column = QW.QSplitter(QC.Qt.Vertical)
        right_column.addWidget(self._message_box)
        right_column.addWidget(self._param_box)
        right_column.setSizes([200, 200])

        # Right and left columns next to each other
        h_splitter = QW.QSplitter(QC.Qt.Horizontal)
        h_splitter.addWidget(left_column)
        h_splitter.addWidget(right_column)
        h_splitter.setSizes([200, 200])

        # Now add the split up window.
        main_layout = QW.QVBoxLayout(self)
        main_layout.addWidget(h_splitter)
        main_layout.addWidget(self._do_fit_button)

    def update(self):
        """
        Update all widgets.
        """
        for w in self._core_widgets:
            w.update()

    def clear(self):
        """
        Clear all widgets.
        """
        for w in self._core_widgets:
            w.clear()

    def delete(self):
        """
        Delete this widget.
        """
    
        for w in self._core_widgets:
            w.delete()
        self.setParent(None)

    def do_fit_callback(self):
        """
        Do the fit.
        """

        # Make sure experiments are loaded
        if len(self._fit.experiments) == 0:
            warn = "Load experiments before fitting."
            error_message = QW.QMessageBox.warning(self, "warning", warn, QW.QMessageBox.Ok)
            return

        self._do_fit_button.setText("Fit running...")
        self._do_fit_button.setDisabled(True)
        self._do_fit_button.repaint()
        self._do_fit_button.update()

        self._fit.do_fit()
            
        self._do_fit_button.setText("Do fit")
        self._do_fit_button.setDisabled(False)
        self._do_fit_button.repaint()
        self._do_fit_button.update()

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
    def message_box(self):
        """
        Main message box.
        """
        return self._message_box

    @property
    def exp_box(self):
        """
        Main experiment box.
        """
        return self._exp_box

    @property
    def param_box(self):
        """
        Table with parameters.
        """
        return self._param_box

