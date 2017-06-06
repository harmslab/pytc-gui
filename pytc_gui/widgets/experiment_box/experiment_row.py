
from PyQt5 import QtWidgets as QW
from PyQt5 import QtGui as QG
from PyQt5 import QtCore as QC

from .experiment_dialog import ExperimentOptionsDialog

import os

class ExperimentRow(QW.QWidget):

    def __init__(self,parent,fit,experiment):

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment

        self._need_meta_field = False
        self._meta_field_name = "Meta data:"

        self._image_base = os.path.split(os.path.realpath(__file__))[0]

        self.layout()


    def layout(self):
        """
        Layout the row for this experiment.
        """

        self._main_layout = QW.QHBoxLayout(self)

        # Construct the header for the experiment
        self._label = QW.QLabel("test") #self._label)
        self._main_layout.addWidget(self._label)

        # -------------- Buttons --------------------

        # Button to show experiment options
        self._show_options_button = QW.QPushButton("", self)
        self._show_options_button.clicked.connect(self._options_callback)
        self._show_options_button.setIcon(QG.QIcon(os.path.join(self._image_base,"icons","more-info.png")))
        self._show_options_button.setIconSize(QC.QSize(21,21))
        self._show_options_button.setFixedWidth(30)
        self._main_layout.addWidget(self._show_options_button)

        # Button to remove experiment
        self._remove_button = QW.QPushButton("", self)
        self._remove_button.clicked.connect(self._remove_callback)
        self._remove_button.setIcon(QG.QIcon(os.path.join(self._image_base,"icons","delete-icon.png")))
        self._remove_button.setIconSize(QC.QSize(21,21))
        self._remove_button.setFixedWidth(30)
        self._main_layout.addWidget(self._remove_button)

        # ------------- Meta data -------------------

        # Field for adding meta data
        self._meta_label = QW.QLabel(self._meta_field_name,self)
        self._main_layout.addWidget(self._meta_label)

        self._meta_entry = QW.QLineEdit(self)
        self._main_layout.addWidget(self._meta_entry)

        self._meta_label.hide()
        self._meta_entry.hide()

        self._main_layout.setGeometry(QC.QRect(0,0,200,30))
        self._main_layout.setSpacing(0)

    def _options_callback(self): 
        """
        Construct dialog with fit options for this experiment.
        """    

        self._tmp = ExperimentOptionsDialog(self,self._fit,self._experiment)
        self._tmp.show()
            

    def _remove_callback(self):
        """
        Remove an experiment from the fitter.
        """

        warn = "Are you sure you want to remove experiment?"
        warning_message = QW.QMessageBox.warning(self, "Warning", warn,
                                                 QW.QMessageBox.Yes|QW.QMessageBox.No)

        if warning_message == QW.QMessageBox.Yes:

            try:
                self._fit.remove_experiment(self._experiment)
            except ValueError:
                err = "Experiment already deleted.\n"
                sys.stderr.write(err)

        self._fit.emit_changed()

    @property
    def need_meta_field(self):
        
        return self._need_meta_field

    @need_meta_field.setter
    def need_meta_field(self,value):

        if type(value) is not bool:
            err = "need_meta_field must be boolean"
            raise ValueError(err)

        self._need_meta_field = value
        if self._need_meta_field:
            self._meta_label.show()
            self._meta_entry.show()
        else:
            self._meta_label.hide()
            self._meta_entry.hide()

    @property
    def meta_field_name(self):
        return self._meta_field_name

    @meta_field_name.setter
    def meta_field_name(self,value):
        self._meta_field_name = str(value)
        self._meta_label.setText(self._meta_field_name)
