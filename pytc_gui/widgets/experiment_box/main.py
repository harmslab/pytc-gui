__description__ = \
"""
message box visual element for pytc gui.
"""
__author__ = "Hiranmayi Duvvuri, Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtCore as QC
from PyQt5 import QtWidgets as QW

from .experiment_widget import ExperimentWidget

class ExperimentBox(QW.QWidget):
    """
    Widget for holding experiments.
    """

    def __init__(self,parent,fit):
    
        super().__init__()

        self._parent = parent
        self._fit = fit

        self._experiments_shown = {}

        self.layout()
        self.update()

    def layout(self):

        self._exp_content = QW.QWidget()

        # scroll box for experiments
        self._scroll = QW.QScrollArea(self)
        self._scroll.setWidget(self._exp_content)
        self._scroll.setWidgetResizable(True)

        self._experiment_box = QW.QVBoxLayout(self._exp_content)
        self._experiment_box.setAlignment(QC.Qt.AlignTop)

        self._main_layout = QW.QVBoxLayout(self)
        self._main_layout.addWidget(self._scroll)


    def update(self):
        """
        """

        # Make sure that all experiments in the FitContainer are shown
        for i, e in enumerate(self._fit.experiments):
            try:
                self._experiments_shown[e]
            except KeyError:
                self._experiments_shown[e] = ExperimentWidget(self,self._fit,e)
                self._experiment_box.addWidget(self._experiments_shown[e])

        # Delete widgets for experiments in that aren't in the FitContainer
        all_exp = list(self._experiments_shown.keys())
        for e in all_exp:
            if e not in self._fit.experiments:
                self._experiments_shown[e].deleteLater()
                self._experiments_shown.pop(e)
             
    def clear(self):
        """
        Clear the widget.
        """

        for i in reversed(range(self._experiment_box.count())): 
            try:
                self._main_layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
    
