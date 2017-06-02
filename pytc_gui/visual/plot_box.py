from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import seaborn

class PlotBox(QWidget):
    """
    hold plot widget and update plot
    """

    def __init__(self, parent):
        """
        """
        super().__init__()

        self._fitter = parent._fitter

        self.layout()

    def layout(self):
        """
        """
        self._main_layout = QVBoxLayout(self)

    def update(self):
        """
        clear main layout and add new graph to layout
        """

        self.clear()
        tabs = QTabWidget()

        self._figure, self._ax = self._fitter.plot()

        plot_figure = FigureCanvas(self._figure)
        tabs.addTab(plot_figure, "Main")

        try: 
            self._corner_fig = self._fitter.corner_plot()
        except:
            self._corner_fig = Figure()
            corner_ax = self._corner_fig.add_subplot(111)

        corner_plot = FigureCanvas(self._corner_fig)
        tabs.addTab(corner_plot, "Corner Plots")

        self._main_layout.addWidget(tabs)

    def clear(self):
        """
        clear table
        """
        for i in range(self._main_layout.count()): 
            self._main_layout.itemAt(i).widget().deleteLater()

