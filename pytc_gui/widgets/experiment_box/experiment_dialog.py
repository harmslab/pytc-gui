__description__ = \
"""
"""
__author__ = "Michael J. Harms"
__date__ = "2017-06-01"

from .connector_dialog import AddConnectorDialog

from PyQt5 import QtWidgets as QW
from PyQt5 import QtGui as QG
from PyQt5 import QtCore as QC

import sys, copy

class FitParamWrapper(QW.QWidget):
    """
    This class wraps a single fit parameter with a gui. 
    """

    def __init__(self,parent,fit,experiment,fit_param,float_view_cutoff=100000.):
        """
        Initialize the class.

        parent: parent widget
        fit: FitContainer object
        experiment: pytc.ITCExperiment instance
        fit_param: pytc.FitParameter instance to wrap
        float_view_cutoff: how to show floats in QLineEdit boxes
        """

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment
        self._p = fit_param
        self._float_view_cutoff = float_view_cutoff       

        self._fit.fit_changed_signal.connect(self.fit_has_changed_slot)

        # This is the index for the experiment in the global fit object
        self._expt_index = self._fit.experiments.index(self._experiment)
 
        self.layout()


    def layout(self):

        # --------------- Guess -----------------       
        self._guess = QW.QLineEdit()
        if self._p.guess < 1/self._float_view_cutoff or self._p.guess > self._float_view_cutoff:
            guess_str = "{:.8e}".format(self._p.guess)
        else:
            guess_str = "{:.8f}".format(self._p.guess)
        self._guess.setText(guess_str)

        self._guess.textChanged.connect(self._guess_check_handler)
        self._guess.editingFinished.connect(self._guess_final_handler)

        # --------------- Lower -----------------       
        self._lower = QW.QLineEdit()
        if  self._p.bounds[0] < 1/self._float_view_cutoff or self._p.bounds[0] > self._float_view_cutoff:
            lower_str = "{:.8e}".format(self._p.bounds[0])
        else:
            lower_str = "{:.8f}".format(self._p.bounds[0])
        self._lower.setText(lower_str)

        self._lower.textChanged.connect(self._lower_check_handler)
        self._lower.editingFinished.connect(self._lower_final_handler)
               
        # --------------- Upper -----------------       
        self._upper = QW.QLineEdit()
        if  self._p.bounds[1] < 1/self._float_view_cutoff or self._p.bounds[1] > self._float_view_cutoff:
            upper_str = "{:.8e}".format(self._p.bounds[1])
        else:
            upper_str = "{:.8f}".format(self._p.bounds[1])
        self._upper.setText(upper_str)

        self._upper.textChanged.connect(self._upper_check_handler)
        self._upper.editingFinished.connect(self._upper_final_handler)

        # --------------- Fixed -----------------
        self._fixed = QW.QCheckBox()
        self._fixed.setChecked(self._p.fixed)
        self._fixed.stateChanged.connect(self._fixed_handler)
       
        # --------------- Alias -----------------
        self._alias = QW.QComboBox()
        self._alias.addItem("Unlink")
        self._alias.addItem("Add global")
        self._alias.addItem("Add connector")

        self._alias.currentIndexChanged.connect(self._alias_handler)

    def _guess_check_handler(self,set_value=False):
        """
        Handle guess entries.  Turn pink of the value is bad.  

        set_value: whether to set the underlying value.
        """

        success = True 
        try:
            value = float(self._guess.text())
            if value < self._p.bounds[0] or value > self._p.bounds[1]:
                raise ValueError
        except ValueError:
            success = False    
 
        if success:
            color = "#FFFFFF"
        else:
            color = "#FFB6C1"

        self._guess.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))

        if success and set_value:
            self._p.guess = value
            if self._fit.continuous_update:
                self._fit.emit_changed()

        # Record instance-wide value indiciating whether the current guess is 
        # valid or not. 
        if success:
            self._current_guess_is_good = True
        else:
            self._current_guess_is_good = False

    def _guess_final_handler(self):
        """
        Run check, then set value.
        """

        self._guess_check_handler(set_value=True) 
        
    def _lower_check_handler(self,set_value=False):
        """
        Handle lower bound entries.  Turn pink of the value is bad.  

        set_value: whether to set the underlying value.
        """

        success = True 
        try:
            value = float(self._lower.text())
            if value > self._p.guess:
                raise ValueError
        except ValueError:
            success = False    
 
        if success:
            color = "#FFFFFF"
        else:
            color = "#FFB6C1"

        self._lower.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))

        if success and set_value:
            self._p.bounds = [value,self._p.bounds[1]]
            if self._fit.continuous_update:
                self._fit.emit_changed()

    def _lower_final_handler(self):
        """
        Run check, then set value.
        """
        self._lower_check_handler(set_value=True)

    def _upper_check_handler(self,set_value=False):
        """
        Handle upper bound entries.  Turn pink of the value is bad.  

        set_value: whether to set the underlying value.
        """

        success = True 
        try:
            value = float(self._upper.text())
            if value < self._p.guess:
                raise ValueError
        except ValueError:
            success = False    
 
        if success:
            color = "#FFFFFF"
        else:
            color = "#FFB6C1"

        self._upper.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
     
        if success and set_value:
            self._p.bounds = [self._p.bounds[0],value] 
            if self._fit.continuous_update:
                self._fit.emit_changed()
    
    def _upper_final_handler(self):
        """
        Run check, then set value.
        """
        self._upper_check_handler(set_value=True)
 
    def _fixed_handler(self):
        """
        Handle fixing parameters.
        """
   
        value = self._fixed.checkState()
 
        # If false, immediately record    
        if not value:
            self._p.fixed = value
    
        else:
            
            # Make sure the guess is okay before setting to true
            self._guess_check_handler()
            if self._current_guess_is_good:
                fixed_value = float(self._guess.text()) 
            
                self._p.fixed = True
                self._p.guess = fixed_value
                self._p.value = fixed_value

            else:
                err = "Fixing variable requires valid guess. (Guess will become fixed value).\n"
                error_message = QW.QMessageBox.warning(self._parent,"warning",err,QW.QMessageBox.Ok)
                self._fixed.setCheckState(False)

    def _alias_handler(self,value):
        """
        """
        value = self._alias.currentText()
        if value == "Unlink":

            # Remove current global link, if present
            try:
                self._fit.fitter.unlink_from_global(self._experiment,self._p.name)
            except KeyError:
                pass

            self._fit.emit_changed()

        elif value == "Add global":
            param_name, ok = QW.QInputDialog.getText(self,
                                                     "Global param",
                                                     "New global param name:")
            if ok:

                # Remove current global link if present
                try:
                    self._fit.fitter.unlink_from_global(self._experiment,self._p.name)
                except KeyError:
                    pass

                self._fit.fitter.link_to_global(self._experiment,self._p.name,param_name)
                self._fit.emit_changed()
            
        elif value == "Add connector":
            self._tmp = AddConnectorDialog(self,self._fit,self._experiment,self._p)
            self._tmp.show()

        else:
            
            # Remove current global link, if present
            try:
                self._fit.fitter.unlink_from_global(self._experiment,self._p.name)
            except KeyError:
                pass
            self._fit.fitter.link_to_global(self._experiment,self._p.name,value) 
            self._fit.emit_changed()
       
    @QC.pyqtSlot(bool)
    def fit_has_changed_slot(self):

        # Make sure all of the global parameters are in the dropdown
        global_param = list(self._fit.global_param.keys())
        for k in global_param:
            if self._alias.findText(k) == -1:
                self._alias.addItem(k)

        # These guys should always be kept
        global_param.append("Unlink")
        global_param.append("Add global")
        global_param.append("Add connector")
        global_param.extend(self._fit.connector_labels.values())
   
        # parameters 
        indexes = list(range(self._alias.count()))
        indexes.reverse() 
        for i in indexes:
            item_text = self._alias.itemText(i)
            if item_text not in global_param:
                self._alias.removeItem(i)

        # Now grab the current alias for this parameter
        param_aliases = self._fit.fitter.param_aliases[1][self._expt_index]   
        try:
            current_alias = param_aliases[self._p.name]
        except KeyError:
            current_alias = "Unlink"

        # Update the dropdown so it points to the correct parameter
        alias_index = self._alias.findText(current_alias) 
        self._alias.setCurrentIndex(alias_index)


    @property
    def guess_widget(self):
        return self._guess

    @property
    def lower_widget(self):
        return self._lower

    @property
    def upper_widget(self):
        return self._upper

    @property
    def fixed_widget(self):
        return self._fixed

    @property
    def alias_widget(self):
        return self._alias 


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
 
class ExperimentOptionsDialog(QW.QDialog):
    """
    Dialog used to create options for experiment.  This includes fit parameters
    and some experiment metadata.
    """

    def __init__(self,parent,fit,experiment):
        """
        parent: parent widget
        fit: FitContainer instance
        experiment: pytc.ITCExperimentInstance
        """

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment

        # Use the FitContainer instance to get the fittable parameteres and the
        # expeirment properties that can be set.
        self._fit_param_info = self._fit.get_experiment_param(self._experiment)
        self._experiment_settable = self._fit.get_experiment_settable(self._experiment)

        self.layout()

    def layout(self):
        """
        Construct the widget.
        """
    
        model_params = list(self._fit_param_info.keys())
        model_name = model_params.remove("model_name")
        model_params.sort()

        self._main_layout = QW.QVBoxLayout(self)
       
        # ------------ Fit parameters --------------- 
        self._fit_param_box = QW.QGroupBox("Fit Parameters") 
        self._fit_param_layout = QW.QGridLayout()

        # Table header 
        self._fit_param_layout.addWidget(QW.QLabel("param"), 0,0) 
        self._fit_param_layout.addWidget(QW.QLabel("guess"), 0,1) 
        self._fit_param_layout.addWidget(QW.QLabel("global"),0,2) 
        self._fit_param_layout.addWidget(QW.QLabel("fixed"), 0,3) 
        self._fit_param_layout.addWidget(QW.QLabel("lower"), 0,4) 
        self._fit_param_layout.addWidget(QW.QLabel("upper"), 0,5) 

        # Build widgets for each fittable parameter
        self._param_widgets = []           
        for i, k in enumerate(model_params):

            self._param_widgets.append(FitParamWrapper(self,self._fit,
                                                       self._experiment,
                                                       self._fit_param_info[k]))
 
            self._fit_param_layout.addWidget(QW.QLabel(k),                        i+1,0)
            self._fit_param_layout.addWidget(self._param_widgets[-1].guess_widget,i+1,1)
            self._fit_param_layout.addWidget(self._param_widgets[-1].alias_widget,i+1,2)
            self._fit_param_layout.addWidget(self._param_widgets[-1].fixed_widget,i+1,3)
            self._fit_param_layout.addWidget(self._param_widgets[-1].lower_widget,i+1,4)
            self._fit_param_layout.addWidget(self._param_widgets[-1].upper_widget,i+1,5)

        self._fit_param_box.setLayout(self._fit_param_layout)
        self._main_layout.addWidget(self._fit_param_box)

        # ---------- Horizontal line -----------------
        hline = QW.QFrame()
        hline.setFrameShape(QW.QFrame.HLine)
        self._main_layout.addWidget(hline)

        # ---------- Experiment information ------------      

        expt_keys = list(self._experiment_settable.keys())
        expt_keys.sort()
 
        self._expt_widgets = []       
        for settable_name in expt_keys:

            start_value      = self._experiment_settable[settable_name][0]
            value_type       = self._experiment_settable[settable_name][1]
            allowable_values = self._experiment_settable[settable_name][2] 

            self._expt_widgets.append(ExperimentSettableWrapper(self,
                                                                self._fit,
                                                                self._experiment,
                                                                settable_name,
                                                                start_value,
                                                                value_type,
                                                                allowable_values))
 
        self._experiment_settable_box = QW.QGroupBox("Experiment information") 
        self._experiment_settable_layout = QW.QGridLayout()

        # Layout the experimental widgets in rows of 3.
        while len(self._expt_widgets) % 3 != 0:
            self._expt_widgets.append(QW.QLabel(" "))

        counter = 0
        num_rows = int(round((len(self._expt_widgets)+1)/3))
        for i in range(num_rows):
            for j in range(3):
                self._experiment_settable_layout.addWidget(self._expt_widgets[counter],i,j)
                counter += 1

        self._experiment_settable_box.setLayout(self._experiment_settable_layout)
        self._main_layout.addWidget(self._experiment_settable_box)


