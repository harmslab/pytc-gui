__description__ = \
"""
Wrap all settable attributes of an experiment in a GUI.
"""
__author__ = "Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtWidgets as QW

import copy

class ExperimentSettableWrapper(QW.QWidget):
    """
    Wrap a single experiment settable as a widget.
    """

    def __init__(self,parent,fit,experiment,settable_name,start_value,value_type,
                 allowable_values,float_view_cutoff=100000):
        """
        parent: parent widget
        fit: FitContainer object
        experiment: pytc.ITCExperiment object containing settable
        settable_name: name of settable (string) in experiment object
        start_value: starting value of settable when widget opens
        value_type: value type. 
            bool -> QCheckBox
            str,float,int -> QLineEdit, parsed appropriately
            multi -> QDropDown, using allowable_values to populate
        allowable_value: list of available values for multi, None otherwise
        float_view_cutoff: how to show floats in QLineEdit boxes
        """

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment
        self._settable_name = settable_name
        self._start_value = start_value
        self._value_type = value_type
        self._allowable_values = allowable_values
        self._float_view_cutoff = float_view_cutoff


        self.layout()

    def layout(self):
        """
        Create widget layout.
        """

        self._main_layout = QW.QHBoxLayout(self)

        self._label = QW.QLabel(self._settable_name)
        self._main_layout.addWidget(self._label)       

        # --------- multi value ----------
        if self._value_type == "multi":

            self._select_widget = QW.QComboBox(self)

            try:
                len(self._allowable_values)
            except TypeError:
                err = "allowable types must be a list-like object for a multi value.\n"
                raise ValueError(err) 

            self._allowable_values = copy.copy(self._allowable_values)
            self._allowable_values.sort()
            self._select_widget.addItems(self._allowable_values)

            current_index = self._select_widget.findText(self._start_value)
            if current_index == -1:
                err = "current value is not in the allowable values\n"
                raise ValueError(err)

            self._select_widget.setCurrentIndex(current_index)
            self._select_widget.currentIndexChanged.connect(self._update_multi_settable)

        # --------- bool value --------------
        elif self._value_type == bool:

            self._select_widget = QW.QCheckBox()
            self._select_widget.setChecked(self._start_value)
            self._select_widget.stateChanged.connect(self._start_value)

        # -------- other values --------------
        else:
            self._select_widget = QW.QLineEdit(self)

            if self._value_type == float:
                if self._start_value < 1/self._float_view_cutoff or self._start_value > self._float_view_cutoff:
                    val_str = "{:.8e}".format(self._start_value)
                else:
                    val_str = "{:.8f}".format(self._start_value)
            else:
                val_str = "{}".format(self._start_value)

            self._select_widget.setText(val_str)

            self._select_widget.textChanged.connect(self._update_other_settable)

        self._main_layout.addWidget(self._select_widget)
           
    def _update_multi_settable(self,value):
        """
        Handler for "multi" values.  Parses QDropDown.
        """

        new_value = self._select_widget.currentText()

        setattr(self._experiment, self._settable_name, new_value)
        if self._fit.continuous_update:
            self._fit.emit_changed()

    def _update_bool_settable(self):
        """
        Handler for bool values.  Parses QCheckBox
        """
              
        setattr(self._experiment,self._settable_name, self._select_wiget.checkState())
        if self._fit.continuous_update:
            self._fit.emit_changed() 

    def _update_other_settable(self):
        """
        Handler for other values (str, float, int most likely).  Parses
        QLineEdit.
        """

        current = self._select_widget.text()
        try:
            new_value = self._value_type(current)
            color = "#FFFFFF"
        except ValueError:
            new_value = None
            color = "#FFB6C1"
        
        self._select_widget.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
        if new_value is not None:
        
            setattr(self._experiment,self._settable_name, new_value)
            if self._fit.continuous_update:
                self._fit.emit_changed() 
 
