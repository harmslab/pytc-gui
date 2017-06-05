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

        self._fitter_list = parent._fitter_list

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

        # ------------ "Do fit" button -------------------
        do_fit_button = QW.QPushButton("Do fit", self)
        do_fit_button.clicked.connect(self.do_fit_callback)

        # Split up the main window in a useful way

        # Left column
        left_column = QW.QSplitter(QC.Qt.Vertical)
        left_column.addWidget(self._plot_box)
        left_column.addWidget(self._exp_box)
        left_column.setSizes([300, 50])

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
        main_layout.addWidget(do_fit_button)

        # MJH ??? --> what is signaling architecture?
        self._parent.fit_signal.connect(self.fit_signal_update)

    def clear(self):
        """
        Clear all widgets.
        """

        self._plot_box.clear()
        self._message_box.clear()
        self._exp_box.clear()
        self._param_box.clear()

    def update_fit_options(self, options_dict):
        """
        """
        self._global_fit_options = options_dict

    def _perform_fit(self):
        """
        XXX MJH TEMPORARY BRIDGE DURING REFACTOR XXX
        """

        self._exp_box.update_exp()

        # after doing fit, emit signal to sliders and update parameter table
        self._parent._fit.fitter.fit(**self._global_fit_options)
        self._parent.fit_signal.emit(self._fit.fitter)

    def do_fit_callback(self):
        """
        """
        self._perform_fit()
        self._plot_box.update()
        self._param_box.update()

    @QC.pyqtSlot(pytc.global_fit.GlobalFit)
    def fit_signal_update(self, obj):
        """
        """
        self._plot_box._fitter = obj
        self._exp_box._fitter = obj

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

    @property
    def fitter(self):
        """
        Main fitter object.
        """
        return self._fit.fitter


