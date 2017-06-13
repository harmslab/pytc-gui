__description__ = \
"""
Class for holding onto an experiment, allowing deletion and access to fitting
parameters.
"""
__author__ = "Hiranmayi Duvvuri, Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtWidgets as QW
from PyQt5 import QtGui as QG
from PyQt5 import QtCore as QC

from .experiment_dialog import ExperimentOptionsDialog

import os

class ExperimentWidget(QW.QFrame):
    """
    Pointer to experiment.  Has name, settings button, and delete button.
    """

    def __init__(self,parent,fit,experiment):

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment
        
        if self._experiment is not None:
            self._expt_label = self._fit.experiment_labels[experiment]
        else:
            self._expt_label = "dummy"

        self._image_base = os.path.split(os.path.realpath(__file__))[0]

        self.layout()


    def layout(self):
        """
        Layout the row for this experiment.
        """

        self._main_layout = QW.QGridLayout(self)

        # Construct the header for the experiment
        self._main_layout.addWidget(QW.QLabel(self._expt_label),0,0)
 
        # -------------- Buttons --------------------

        # Button to show experiment options
        self._show_options_button = QW.QPushButton("", self)
        self._show_options_button.clicked.connect(self._options_callback)
        self._show_options_button.setIcon(QG.QIcon(os.path.join(self._image_base,"icons","more-info.png")))
        self._show_options_button.setIconSize(QC.QSize(21,21))
        self._show_options_button.setFixedWidth(30)
        self._main_layout.addWidget(self._show_options_button,0,1)

        # Button to remove experiment
        self._remove_button = QW.QPushButton("", self)
        self._remove_button.clicked.connect(self._remove_callback)
        self._remove_button.setIcon(QG.QIcon(os.path.join(self._image_base,"icons","delete-icon.png")))
        self._remove_button.setIconSize(QC.QSize(21,21))
        self._remove_button.setFixedWidth(30)
        self._main_layout.addWidget(self._remove_button,0,2)

        self.setFrameShape(QW.QFrame.StyledPanel)

        if self._experiment is None:
            self._show_options_button.setDisabled(True)
            self._remove_button.setDisabled(True)

    def _options_callback(self): 
        """
        Construct persistent dialog with fit options for this experiment.
        """    

        try:
            self._options_diag.show()
        except AttributeError:
            self._options_diag = ExperimentOptionsDialog(self,self._fit,self._experiment)
            self._options_diag.show()
        
        self._options_diag.raise_()           
 
    def _remove_callback(self):
        """
        Remove an experiment from the fitter.
        """

        warn = "Are you sure you want to remove experiment?"
        warning_message = QW.QMessageBox.warning(self, "Warning", warn,
                                                 QW.QMessageBox.Yes|QW.QMessageBox.No)

        if warning_message == QW.QMessageBox.Yes:
            self.delete()
           
    def delete(self):
        """
        Delete widgets.
        """

        try:
            self._options_diag.delete()
            self._options_diag.setParent(None)
        except AttributeError:
            pass

        self.setParent(None)

        # Remove experiment -- unless already removed
        try:
            self._fit.remove_experiment(self._experiment)
        except ValueError:
            pass

