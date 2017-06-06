__description__ = \
"""
"""
__author__ = "Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtWidgets as QW
from PyQt5 import QtGui as QG

import sys

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

class ExperimentParamWrapper:
    """
    """

    def __init__(self,parent,fit,experiment):
        """
        """

        self._parent = parent
        self._fit = fit

        

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
        self.horizontalGroupBox = QW.QGroupBox() 

        self._layout = QW.QGridLayout()
 
        self._layout.addWidget(QW.QLabel("param"), 0,0) 
        self._layout.addWidget(QW.QLabel("guess"), 0,1) 
        self._layout.addWidget(QW.QLabel("global"),0,2) 
        self._layout.addWidget(QW.QLabel("fixed"), 0,3) 
        self._layout.addWidget(QW.QLabel("upper"), 0,4) 
        self._layout.addWidget(QW.QLabel("lower"), 0,5) 

        self._param_widgets = []           
        for i, k in enumerate(model_params):

            self._param_widgets.append(FitParamWrapper(self,self._fit,self._model_info[k]))
 
            self._layout.addWidget(QW.QLabel(k),                        i+1,0)
            self._layout.addWidget(self._param_widgets[-1].guess_widget,i+1,1)
            self._layout.addWidget(self._param_widgets[-1].alias_widget,i+1,2)
            self._layout.addWidget(self._param_widgets[-1].fixed_widget,i+1,3)
            self._layout.addWidget(self._param_widgets[-1].lower_widget,i+1,4)
            self._layout.addWidget(self._param_widgets[-1].upper_widget,i+1,5)

        self.horizontalGroupBox.setLayout(self._layout)
        self._main_layout.addWidget(self.horizontalGroupBox)

        # ---------- Horizontal line -----------------
        hline = QW.QFrame()
        hline.setFrameShape(QW.QFrame.HLine)
        self._main_layout.addWidget(hline)

        # ---------- Experiment information ------------      

        expt_keys = list(self._expt_info.keys())
        expt_keys.sort()
 
        self._expt_widgets = []       
        for k in expt_keys:

            start_value    = self._expt_info[k][0]
            value_type     = self._expt_info[k][1]
            default_value  = self._expt_info[k][2] 
             
            #if value_type == "multi":
  

            print(k,self._expt_info[k])

"""
class ExpOptions(QDialog):
 
    def __init__(self, parent,experiment):
        super().__init__()
      
        self._parent = parent  
        self._experiment = experiment

        self.layout()

    def layout(self):
        main_layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()
        self._get_info()

        update_button = QPushButton("Update", self)
        update_button.clicked.connect(self._update_val)

        main_layout.addLayout(self._form_layout)
        main_layout.addWidget(update_button)

        self.setWindowTitle('Experiment Options')

    def _get_info(self):
        self._option_widgets = {}

        classes = inspect.getmembers(self._experiment, inspect.isclass)
        properties = inspect.getmembers(classes[0][1], lambda o: isinstance(o, property))

        setters = [p[0] for p in properties if p[1].fset != None]

        for i, s in enumerate(setters):

            # Skip heats (which has setter we need to ignore)
            if s in ["heats","heats_stdev"]:
                continue

            if s == "units":
                units_names = list(self._experiment.AVAIL_UNITS)
                units_names.sort()

                starting_index = 0
                self._option_widgets[s] = QComboBox(self)
                for j, k in enumerate(units_names):
                    self._option_widgets[s].addItem(k)
                    if k == self._experiment.units:
                        starting_index = j
                self._option_widgets[s].setCurrentIndex(starting_index)        

                name = str(s).replace("_", " ") + ": "
                self._experiment.units = str(self._option_widgets[s].currentText())
                self._option_widgets[s].activated[str].connect(self._units_select)
                self._form_layout.addRow(QLabel(name), self._option_widgets[s])

            else:
                self._option_widgets[s] = QLineEdit(self)
                self._option_widgets[s].setText(str(getattr(self._experiment,s)))

                name = str(s).replace("_", " ") + ": "
                self._form_layout.addRow(QLabel(name.title()), self._option_widgets[s])

    def _update_val(self):

        for k, v in self._option_widgets.items():
   
            try: 
                if type(v) == QComboBox:
                    val = str(v.currentText())
                else:
                    val = ast.literal_eval(str(v.text()))

                setattr(self._experiment, k, val)

            except ValueError:

                if type(v) == QComboBox:
                    val = str(v.currentText())
                else:
                    val = str(v.text())
                
                error_message = QMessageBox.warning(self,
                                                    "warning",
                                                    "Value {} is invalid".format(val),
                                                    QMessageBox.Ok) 
                return

        self._update.update()
        self.hide()
               
    def _units_select(self,units):
        self._experiment.units = units
"""
