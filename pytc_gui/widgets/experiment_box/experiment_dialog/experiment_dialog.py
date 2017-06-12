__description__ = \
"""
Dialog box holding all experiment fit parameters and settable attributes
in a simple GUI.
"""
__author__ = "Michael J. Harms"
__date__ = "2017-06-01"

from .experiment_meta_wrapper import ExperimentMetaWrapper
from .fit_param_wrapper import FitParamWrapper
from .experiment_settable import ExperimentSettableWrapper

from PyQt5 import QtWidgets as QW
from PyQt5 import QtCore as QC

class ExperimentOptionsDialog(QW.QDialog):
    """
    Dialog used to create options for experiment.  This includes fit parameters
    and some experiment connectordata.
    """

    def __init__(self,parent,fit,experiment,num_exp_columns=3):
        """
        parent: parent widget
        fit: FitContainer instance
        experiment: pytc.ITCExperimentInstance
        num_exp_columns: number of columns of ExperimentSettableWidgets
        """

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment
        self._num_exp_columns = num_exp_columns
      
        # keep track of currently required metadata 
        self._current_required_meta = None
        self._current_connector_param = None
 
        self._fit.fit_changed_signal.connect(self.fit_has_changed_slot)

        self.layout()

    def layout(self):
        """
        Construct the widget.
        """

        name = self._fit.experiment_labels[self._experiment]
        self.setWindowTitle("{} fit parameters".format(name)) 

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
        self._fit_param_info = self._fit.get_experiment_param(self._experiment)

        model_params = list(self._fit_param_info.keys())
        model_name = model_params.remove("model_name")
        model_params.sort()
        self._param_widgets = []           
        for i, k in enumerate(model_params):

            self._param_widgets.append(FitParamWrapper(self,
                                                       self._fit,
                                                       self._experiment,
                                                       self._fit_param_info[k]))
 
            self._fit_param_layout.addWidget(QW.QLabel(k),                        i+1,0)
            self._fit_param_layout.addWidget(self._param_widgets[-1].guess_widget,i+1,1)
            self._fit_param_layout.addWidget(self._param_widgets[-1].alias_widget,i+1,2)
            self._fit_param_layout.addWidget(self._param_widgets[-1].fixed_widget,i+1,3)
            self._fit_param_layout.addWidget(self._param_widgets[-1].lower_widget,i+1,4)
            self._fit_param_layout.addWidget(self._param_widgets[-1].upper_widget,i+1,5)

        self._num_param_rows = len(model_params) + 1
        self._num_local_param_widgets = self._num_param_rows*6

        self._fit_param_box.setLayout(self._fit_param_layout)
        self._main_layout.addWidget(self._fit_param_box)

        # ---------- Horizontal line -----------------
        hline = QW.QFrame()
        hline.setFrameShape(QW.QFrame.HLine)
        self._main_layout.addWidget(hline)

        # ---------- Experiment information ------------      

        self._experiment_settable = self._fit.get_experiment_settable(self._experiment)

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

        # Lay out the experimental widgets in rows of self._num_exp_columns.
        to_layout = [w for w in self._expt_widgets]


        # Add dummy widgets to fill out grid 
        hider = QW.QSizePolicy()
        hider.setRetainSizeWhenHidden(True)
        dummies = []
        counter = 0
        while len(to_layout) % self._num_exp_columns != 0:
    
            # Add fake widget
            dummies.append(ExperimentSettableWrapper(self,self._fit,
                                                     self._experiment,
                                                    "dummy{}".format(counter),
                                                    "",str,None))
            dummies[-1].setSizePolicy(hider)
            to_layout.append(dummies[-1])
            to_layout[-1].hide()

            counter += 1

        counter = 0
        self._num_exp_rows = int(round((len(to_layout)+1)/self._num_exp_columns))
        for i in range(self._num_exp_rows):
            for j in range(self._num_exp_columns):
                self._experiment_settable_layout.addWidget(to_layout[counter],i,j)
                counter += 1

        self._experiment_settable_box.setLayout(self._experiment_settable_layout)
        self._main_layout.addWidget(self._experiment_settable_box)

        # Dictionaries to hold widgets for global connectors
        self._connector_widgets = {}
        self._meta_widgets = {}


    def update(self):

        # Update parameter and experimental widgets
        for p in self._param_widgets:
            p.update()
        for e in self._expt_widgets:
            e.update()

        # Grab connector fit parameters and required meta data associated with
        # this experiment 
        required_meta, connector_param = self._fit.get_experiment_connector(self._experiment)

        # ----------- connector parameters --------------
        if set(connector_param) != self._current_connector_param:

            # Build connector widgets for associated parameters  
            connector_keys = list(connector_param.keys())
            connector_keys.sort()
            to_layout = []
            for k in connector_keys:
            
                try:
                    self._connector_widgets[k].update()
                except KeyError:
                    self._connector_widgets[k] = FitParamWrapper(self,
                                                                 self._fit,
                                                                 self._experiment,
                                                                 connector_param[k])
                to_layout.append(self._connector_widgets[k])

            # Delete any existing connector fit parameter widgets from layout
            widget_indexes = list(range(self._num_local_param_widgets,
                                  self._fit_param_layout.count()))
            widget_indexes.reverse()
            for i in widget_indexes:
                self._fit_param_layout.itemAt(i).widget().setParent(None)

            # Add associated connector fit parameter widgets to layout
            for i, w in enumerate(to_layout): 
 
                r = i + self._num_param_rows

                # Lock down the ability to chose a new linkage for this parameter
                w.set_as_connector_param(True)

                self._fit_param_layout.addWidget(QW.QLabel(w.name),r,0)
                self._fit_param_layout.addWidget(w.guess_widget,r,1)
                self._fit_param_layout.addWidget(w.alias_widget,r,2)
                self._fit_param_layout.addWidget(w.fixed_widget,r,3)
                self._fit_param_layout.addWidget(w.lower_widget,r,4)
                self._fit_param_layout.addWidget(w.upper_widget,r,5)

            self._current_connector_param = set(connector_param)

        # ------------- required experiment metadata -----------------

        if set(required_meta) != self._current_required_meta:
 
            required_meta_keys = list(required_meta.keys())
            required_meta_keys.sort()
            to_layout = [] 
            for m in required_meta_keys:
                try:
                    self._meta_widgets[m].update()
                except KeyError:
                    self._meta_widgets[m] = ExperimentMetaWrapper(self,
                                                                  self._fit,
                                                                  self._experiment,
                                                                  m)
                to_layout.append(self._meta_widgets[m])       

            # Delete existing widgets from layout
            widget_indexes = list(range(self._num_exp_rows*3,
                                        self._experiment_settable_layout.count()))
            widget_indexes.reverse()
            for i in widget_indexes:
               self._experiment_settable_layout.itemAt(i).widget().setParent(None)
            
            # Add dummy widgets to fill out grid 
            hider = QW.QSizePolicy()
            hider.setRetainSizeWhenHidden(True)
            dummies = []
            counter = 0
            while len(to_layout) % self._num_exp_columns != 0:
        
                # Add fake widget
                dummies.append(ExperimentSettableWrapper(self,self._fit,
                                                         self._experiment,
                                                        "dummy{}".format(counter),
                                                        "",str,None))
                dummies[-1].setSizePolicy(hider)
                to_layout.append(dummies[-1])
                to_layout[-1].hide()

                counter += 1

            # Lay out the connector widgets in rows of num_exp_columns.
            counter = 0
            num_rows = int(round((len(to_layout)+1)/self._num_exp_columns))
            for i in range(num_rows):
                r = i + self._num_exp_rows
                for j in range(self._num_exp_columns):
                    self._experiment_settable_layout.addWidget(to_layout[counter],r,j)
                    counter += 1

            self._current_required_meta = set(required_meta)

        # For some reason this must be run twice to get correct size in all cases
        self.adjustSize()
        self.adjustSize()
 
    def show(self):
        """
        When the dialog box is shown, update all of the widgets with whatever
        values are currently in the fitter.
        """
    
        self.update()
        super().show() 
       
    @QC.pyqtSlot(bool)
    def fit_has_changed_slot(self):
        self.update()
