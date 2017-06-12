__description__ = \
"""
Class for generating main plots.
"""
__author__ = "Hiranmayi Duvvurii"
__date__ = "2017-06-01"

from PyQt5 import QtWidgets as QW
from PyQt5 import QtCore    as QC

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import seaborn
import sys

class PlotBox(QW.QTabWidget):
    """
    Hold the plot widget.
    """

    def __init__(self, parent, fit):
        """
        """
        super().__init__()

        self._parent = parent
        self._fit = fit
        
        self._err_template = "Could not generate plot. pytc threw <br/>\"\"\"{0} Args: {1!r}\"\"\""
        self._fit.fit_changed_signal.connect(self.fit_has_changed_slot)

    def update(self):
        """
        Clear tabs and repopulate given the current state of the fit.
        """

        self.clear()

        # Delete previous figures
        try:
            plt.close(self._main_fig)
            plt.close(self._corner_fig)
        except AttributeError:
            pass
       
        # Don't try to fit if there is no experiment loaded 
        if len(self._fit.experiments) == 0:
            return

        # Main plot
        try:
            self._main_fig, self._main_ax = self._fit.fitter.plot()
        except Exception as ex:
            err = self._err_template.format(type(ex).__name__,ex.args)
            if self._fit.verbose:
                self._fit.event_logger.emit(err,"warning")

            self._main_fig = Figure()
            self._main_ax = self._main_fig.add_subplot(111)

        self.addTab(FigureCanvas(self._main_fig), "Main")

        # Corner plot
        try: 
            self._corner_fig = self._fit.fitter.corner_plot()

        except Exception as ex:
            err = self._err_template.format(type(ex).__name__,ex.args)
            if self._fit.verbose:
                self._fit.event_logger.emit(err,"warning")

            self._corner_fig = Figure()
            self._corner_ax = self._corner_fig.add_subplot(111)

        self.addTab(FigureCanvas(self._corner_fig), "Corner Plot")
    
    @QC.pyqtSlot(bool)
    def fit_has_changed_slot(self,val):
        """
        Slot that looks for emission from FitContainer saying that it changed
        in some way.
        """

        # Update all of the widgets
        self.update()
