from PyQt5 import QtWidgets as QW

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import seaborn

class PlotBox(QW.QWidget):
    """
    Hold the plot widget.
    """

    def __init__(self, parent, fit):
        """
        """
        super().__init__()

        self._parent = parent
        self._fit = fit
        self.layout()

    def layout(self):
        """
        Create layout for plot.
        """
        self._main_layout = QW.QVBoxLayout(self)

    def update(self):
        """
        clear main layout and add new graph to layout
        """

        self.clear()
    
        tabs = QW.QTabWidget()

        try:
            self._figure, self._ax = self._fit.fitter.plot()
        except AttributeError:
            err = "Warning: Could not update plot."
            print(err)
            return

        plot_figure = FigureCanvas(self._figure)
        tabs.addTab(plot_figure, "Main")

        try: 
            self._corner_fig = self._fit.fitter.corner_plot()
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
