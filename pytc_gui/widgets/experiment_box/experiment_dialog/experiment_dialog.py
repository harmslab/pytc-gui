__description__ = \
"""
Dialog box holding all experiment fit parameters and settable attributes
in a simple GUI.
"""
__author__ = "Michael J. Harms"
__date__ = "2017-06-01"

from .fit_param_wrapper import FitParamWrapper
from .experiment_settable import ExperimentSettableWrapper

from PyQt5 import QtWidgets as QW

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

        # Lay out the experimental widgets in rows of 3.
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
    
    def show(self):
        """
        When the dialog box is shown, update all of the widgets with whatever
        values are currently in the fitter.
        """

        for p in self._param_widgets:
            p.update()

        for e in self._expt_widgets:
            e.update()

        super().show() 
        
