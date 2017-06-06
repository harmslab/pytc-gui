__description__ = \
"""
"""
__author__ = "Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtWidgets as QW
from PyQt5 import QtGui as QG

import sys, copy

class FitParamWrapper:
    """
    This class wraps a single fit parameter with a gui. 
    """

    def __init__(self,parent,fit,fit_param,cutoff=100000.):
        """
        """

        self._parent = parent
        self._fit = fit
        self._p = fit_param

        # --------------- Guess -----------------       
        self._guess = QW.QLineEdit()
        if self._p.guess < 1/cutoff or self._p.guess > cutoff:
            guess_str = "{:.8e}".format(self._p.guess)
        else:
            guess_str = "{:.8f}".format(self._p.guess)
        self._guess.setText(guess_str)

        self._guess_validator = QG.QDoubleValidator(self._p.bounds[0],
                                                    self._p.bounds[1],
                                                    100)
        self._guess.setValidator(self._guess_validator)
        self._guess.textChanged.connect(self._guess_err_handler)
        self._guess.editingFinished.connect(self._guess_handler)

        # --------------- Lower -----------------       
        self._lower = QW.QLineEdit()
        if  self._p.bounds[0] < 1/cutoff or self._p.bounds[0] > cutoff:
            lower_str = "{:.8e}".format(self._p.bounds[0])
        else:
            lower_str = "{:.8f}".format(self._p.bounds[0])
        self._lower.setText(lower_str)

        self._lower_validator = QG.QDoubleValidator(-sys.float_info.max,
                                                    self._p.guess,
                                                    100)
        self._lower.setValidator(self._lower_validator)
        self._lower.textChanged.connect(self._lower_err_handler)
        self._lower.editingFinished.connect(self._lower_handler)
               
        # --------------- Upper -----------------       
        self._upper = QW.QLineEdit()
        if  self._p.bounds[1] < 1/cutoff or self._p.bounds[1] > cutoff:
            upper_str = "{:.8e}".format(self._p.bounds[1])
        else:
            upper_str = "{:.8f}".format(self._p.bounds[1])
        self._upper.setText(upper_str)

        self._upper_validator = QG.QDoubleValidator(self._p.guess,
                                                    sys.float_info.max,
                                                    100)
        self._upper.setValidator(self._upper_validator)
        self._upper.textChanged.connect(self._upper_err_handler)
        self._upper.editingFinished.connect(self._upper_handler)

        # --------------- Fixed -----------------
        self._fixed = QW.QCheckBox()
        self._fixed.setChecked(self._p.fixed)
        self._fixed.stateChanged.connect(self._fixed_handler)
       
        # --------------- Alias -----------------
        self._alias = QW.QComboBox()

      
    def _guess_handler(self):
        """
        Set guess.
        """
       
        value = float(self._guess.text()) 
        self._p.guess = value

    def _guess_err_handler(self):
        """
        Visual cue showing guess error.
        """
      
        state = self._guess_validator.validate(self._guess.text(),0)[0]
        if state == QG.QValidator.Acceptable:
            color = "#FFFFFF"
        else:
            color = "#FFB6C1"
        self._guess.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
        
    def _lower_handler(self):
        """
        Set lower bound.
        """
       
        value = float(self._lower.text()) 
        self._p.bounds = [value,self._p.bounds[1]]

    def _lower_err_handler(self):
        """
        Visual cue showing lower error.
        """
      
        state = self._lower_validator.validate(self._lower.text(),0)[0]
        if state == QG.QValidator.Acceptable:
            color = "#FFFFFF"
        else:
            color = "#FFB6C1"
        self._lower.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))

    def _upper_handler(self):
        """
        Set upper bound.
        """
      
        value = float(self._upper.text())  
        self._p.bounds = [self._p.bounds[0],value]

    def _upper_err_handler(self):
        """
        Visual cue showing upper error.
        """
      
        state = self._upper_validator.validate(self._upper.text(),0)[0]
        if state == QG.QValidator.Acceptable:
            color = "#FFFFFF"
        else:
            color = "#FFB6C1"
        self._upper.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
     
    def _fixed_handler(self):
        """
        Handle fixing variable.
        """
   
        value = self._fixed.checkState()
     
        if not value:
            self._p.fixed = value
    
        else:
            
            # Make sure the guess is okay 
            state = self._guess_validator.validate(self._guess.text(),0)[0]
            if state == QG.QValidator.Acceptable:
                fixed_value = float(self._guess.text()) 
            
                self._p.fixed = True
                self._p.guess = fixed_value
                self._p.value = fixed_value

            else:
                self._guess_err_handler()

                err = "Fixing variable requires valid starting value.\n"
                error_message = QW.QMessageBox.warning(self._parent,"warning",err,QW.QMessageBox.Ok)
                self._fixed.setCheckState(False)

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


class ExperimentParamWrapper(QW.QWidget):
    """
    """

    def __init__(self,parent,fit,experiment,param_name,start_value,value_type,
                 allowable_values,cutoff=100000):
        """
        """

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment
        self._param_name = param_name
        self._start_value = start_value
        self._value_type = value_type
        self._allowable_values = allowable_values
        self._cutoff = cutoff

        self.layout()

    def layout(self):

        self._main_layout = QW.QHBoxLayout(self)

        self._label = QW.QLabel(self._param_name)
        self._main_layout.addWidget(self._label)       

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
            self._select_widget.currentIndexChanged.connect(self._update_multi_param)

        elif self._value_type == bool:

            self._select_widget = QW.QCheckBox()
            self._select_widget.setChecked(self._start_value)
            self._select_widget.stateChanged.connect(self._start_value)

        else:
            self._select_widget = QW.QLineEdit(self)

            if self._value_type == float:
                if self._start_value < 1/self._cutoff or self._start_value > self._cutoff:
                    val_str = "{:.8e}".format(self._start_value)
                else:
                    val_str = "{:.8f}".format(self._start_value)
            else:
                val_str = "{}".format(self._start_value)

            self._select_widget.setText(val_str)

            self._select_widget.textChanged.connect(self._update_other_param)

        self._main_layout.addWidget(self._select_widget)
           
    def _update_multi_param(self,value):

        new_value = self._select_widget.currentText()

        setattr(self._experiment, self._param_name, new_value)
        if self._fit.continuous_update:
            self._fit.emit_changed()

    def _update_bool_param(self):
              
        setattr(self._experiment,self._param_name, self._select_wiget.checkState())
        if self._fit.continuous_update:
            self._fit.emit_changed() 

    def _update_other_param(self):

        current = self._select_widget.text()
        try:
            new_value = self._value_type(current)
            color = "#FFFFFF"
        except ValueError:
            new_value = None
            color = "#FFB6C1"
        
        self._select_widget.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
        if new_value is not None:
        
            setattr(self._experiment,self._param_name, new_value)
            if self._fit.continuous_update:
                self._fit.emit_changed() 
 
class ExperimentOptionsDialog(QW.QDialog):
    """
    """

    def __init__(self,parent,fit,experiment):
        """
        """

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment
            
        current_exp_data = self._fit.get_experiment_meta(self._experiment)
        self._model_info = current_exp_data[0]
        self._expt_info = current_exp_data[1] 

        self.layout()

    def layout(self):
    
        model_params = list(self._model_info.keys())
        model_name = model_params.remove("model_name")
        model_params.sort()

        self._main_layout = QW.QVBoxLayout(self)
       
        # ------------ Fit parameters --------------- 
        self._fit_param_box = QW.QGroupBox() 

        self._fit_param_layout = QW.QGridLayout()
 
        self._fit_param_layout.addWidget(QW.QLabel("param"), 0,0) 
        self._fit_param_layout.addWidget(QW.QLabel("guess"), 0,1) 
        self._fit_param_layout.addWidget(QW.QLabel("global"),0,2) 
        self._fit_param_layout.addWidget(QW.QLabel("fixed"), 0,3) 
        self._fit_param_layout.addWidget(QW.QLabel("upper"), 0,4) 
        self._fit_param_layout.addWidget(QW.QLabel("lower"), 0,5) 

        self._param_widgets = []           
        for i, k in enumerate(model_params):

            self._param_widgets.append(FitParamWrapper(self,self._fit,self._model_info[k]))
 
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

        expt_keys = list(self._expt_info.keys())
        expt_keys.sort()
 
        self._expt_widgets = []       
        for param_name in expt_keys:

            start_value      = self._expt_info[param_name][0]
            value_type       = self._expt_info[param_name][1]
            allowable_values = self._expt_info[param_name][2] 

            self._expt_widgets.append(ExperimentParamWrapper(self,
                                                             self._fit,
                                                             self._experiment,
                                                             param_name,
                                                             start_value,
                                                             value_type,
                                                             allowable_values))
 
        self._experiment_param_box = QW.QGroupBox() 
        self._experiment_param_layout = QW.QGridLayout()

        counter = 0
        num_rows = int(round(len(self._expt_widgets)/2))
        for i in range(num_rows):
            for j in range(2):
                self._experiment_param_layout.addWidget(self._expt_widgets[counter],i,j)
                counter += 1

        self._experiment_param_box.setLayout(self._experiment_param_layout)
        self._main_layout.addWidget(self._experiment_param_box)


