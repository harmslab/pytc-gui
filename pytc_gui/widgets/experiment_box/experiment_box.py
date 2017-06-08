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

        self._main_layout = QW.QGridLayout(self)

        #self._exp_content = QW.QWidget()

        # scroll box for experiments
        #self._scroll = QW.QScrollArea(self)
        #self._scroll.setWidget(self._exp_content)
        #self._scroll.setWidgetResizable(True)

        #self._experiment_box = QW.QVBoxLayout(self._exp_content)
        #self._experiment_box.setAlignment(QC.Qt.AlignTop)

        #self._main_layout = QW.QVBoxLayout(self)
        #self._main_layout.addWidget(self._scroll)


    def update(self):
        """
        """

        # Delete widgets for experiments in that aren't in the FitContainer
        all_exp = list(self._experiments_shown.keys())
        for e in all_exp:
            if e not in self._fit.experiments:
                self._experiments_shown[e].deleteLater()
                self._experiments_shown.pop(e)


        # Make sure that all experiments in the FitContainer are shown
        to_layout = []
        for e in self._fit.experiments:
            try:
                to_layout.append(self._experiments_shown[e])
            except KeyError:
                self._experiments_shown[e] = ExperimentWidget(self,self._fit,e)
                to_layout.append(self._experiments_shown[e])

        # Add dummy widgets to fill out grid 
        hider = QW.QSizePolicy()
        hider.setRetainSizeWhenHidden(True)
        while len(to_layout) % 3 != 0:
            tmp = ExperimentWidget(self,self._fit,None)
            tmp.setSizePolicy(hider)
            tmp.hide()
            to_layout.append(tmp)

        # Lay out the connector widgets in rows of 3.
        counter = 0
        num_rows = int(round((len(to_layout)+1)/3))
        for i in range(num_rows):
            for j in range(3):
                self._main_layout.addWidget(to_layout[counter],i,j)
                counter += 1
        
          
    def clear(self):
        """
        Clear the widget.
        """

        for i in reversed(range(self._experiment_box.count())): 
            try:
                self._main_layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
    
