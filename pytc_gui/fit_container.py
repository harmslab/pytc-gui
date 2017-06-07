__description__ = \
"""
Class for holding on to the global fit object and associated experiments.  
Instance of class is passed to all gui objects and used to manipulate fit in
a coherent fashion.
"""
__author__ = "Michael J. Harms"
__date__ = "2017-06-03"

import pytc
import re, inspect

from PyQt5 import QtWidgets as QW
from PyQt5 import QtCore as QC

class FitContainer(QW.QWidget):
    """
    Virtual widget holding onto the whole fit.  It is never displayed, but 
    holds on to all of the information necessary for the GlobalFit.  Any 
    time it is changed, it emits on self.fit_changed_signal.  This can be
    forced by other objects via self.emit_changed().
    """

    fit_changed_signal = QC.pyqtSignal(bool)

    def __init__(self,default_units="cal/mol",
                      default_model="Single Site",
                      default_shot_start=1,
                      continuous_update=True):
        """
        """

        super().__init__()

        self._default_units = default_units
        self._default_model = default_model
        self._default_shot_start = default_shot_start
        self._continuous_update = continuous_update

        self._fitter = pytc.GlobalFit()

        self._experiments = []
        self._experiment_labels = {}

        self._connectors = []
        self._connector_labels = {}

        # Available model types
        self._avail_models = {re.sub(r"(\w)([A-Z])", r"\1 \2", i.__name__):i
                              for i in pytc.indiv_models.ITCModel.__subclasses__()}

        # Available experiment file types
        self._avail_file_types = []
        for name, obj in inspect.getmembers(pytc.experiments):
            if inspect.isclass(obj):
                new_name = re.sub(r"(\w)([A-Z])", r"\1 \2",name)
                self._avail_file_types.append((new_name,obj))
        self._avail_file_types.sort()

        # Available units
        self._avail_units = getattr(pytc.experiments.base.BaseITCExperiment, 'AVAIL_UNITS')
        self._avail_units = list(self._avail_units.keys())
        self._avail_units.sort()

        # Available connectors
        conn_subclasses = pytc.global_connectors.GlobalConnector.__subclasses__()
        self._avail_connectors = dict([(s.__name__,s) for s in conn_subclasses])

    def emit_changed(self):
        """
        Emit a signal saying that the fit changed.
        """

        self.fit_changed_signal.emit(True)

    @property
    def global_param(self):
        """
        """

        return self._fitter.global_param

    @property
    def fitter(self):
        """
        """

        return self._fitter

    def add_experiment(self,name,*args,**kwargs):
        """
        Add an experiment to the FitContainer. 
        """
  
        self._experiments.append(pytc.ITCExperiment(*args,**kwargs))
        self._fitter.add_experiment(self._experiments[-1])
        self._experiment_labels[self._experiments[-1]] = name 

        self.emit_changed()

    def remove_experiment(self,experiment):
        """
        Remove an experiment from the FitContainer.
        """

        try:
            self._experiment_labels.pop(experiment)

            index = self._experiments.index(experiment)
            to_remove = self._experiments.pop(index)

            self._fitter.remove_experiment(to_remove)
        except ValueError:
            err = "experiment {} found\n".format(experiment)
            raise ValueError(err) 
   
    def get_experiment_param(self,e):
        """
        Return the fittable parameters of an experiment.
        """

        if e not in self._experiments:
            err = "experiment {} not loaded".format(e)
            raise ValueError(err)

        param = {}
        param["model_name"] = e.model
        
        for key in e.model.parameters.keys():
            param[key] = e.model.parameters[key]

        return param

    def get_experiment_settable(self,e):
        """
        Return meta data that can be set for a given experiment.
        """

        meta = {}

        if e not in self._experiments:
            err = "experiment {} not loaded".format(e)
            raise ValueError(err)

        classes = inspect.getmembers(e, inspect.isclass)
        properties = inspect.getmembers(classes[0][1], lambda o: isinstance(o, property))
        setters = [p[0] for p in properties if p[1].fset != None]

        for i, s in enumerate(setters):

            # Skip heats (which has setter we need to ignore)
            if s in ["heats","heats_stdev"]:
                continue

            # Deal with units (special multi)
            if s == "units":
                current_value = getattr(e,s) 
                value_type = "multi"
                avail_values = self._avail_units
            else:
                # For most values, no specific value is required
                current_value = getattr(e,s)
                value_type = type(current_value)
                avail_values = None

                # boolean values are treated as multis
                if value_type is bool:
                    value_type = "multi"
                    avail_values = [True,False]

            meta[s] = (current_value,value_type,avail_values)

        return meta

    @property
    def experiments(self):
        """
        """

        return self._experiments

    @property
    def experiment_labels(self):
        """
        """

        return self._experiment_labels

               
    def add_connector(self,name,connector,*args,**kwargs):
        """
        Add a connector.
        """

        self._connectors.append(connector(*args,**kwargs))
        self._connector_labels[self._connectors[-1]] = name

    def remove_connector(self,c):
        """
        Remove a connector.
        """

        try:
            self._connector_labels.pop(experiment)

            index = self._connnectors.index(experiment)
            to_remove = self._connectors.pop(index)

            # Remove all links to experiments
            for k in c.params.keys():
                self._fitter.remove_global(k)

        except IndexError:
            err = "No connector with index {} found\n".format(c)
            raise IndexError(err) 

    def get_connector_param(self,avail_name):
        """
        Look up parameters for a connector.
        """

        try:
            c = self._avail_connectors[avail_name]
        except KeyError:
            err = "connector {} not found\n".format(avail_name)
            raise ValueError(err)
        
        meta = {}
        parameters = inspect.signature(c).parameters
        for k in parameters:
            meta[k] = parameters.default
            if meta[k] == inspect._empty:
                meta[k] = None

        return meta  

    def clear(self):
        """
        """

        self.__init__(self._default_units,
                      self._default_model,
                      self._default_shot_start,
                      self._continuous_update)

    @property
    def connectors(self):
        """
        """
        return self._connectors
    
    @property
    def connector_labels(self):
        """
        """
        return self._connector_labels
    

    @property
    def avail_models(self):
        return self._avail_models

    @property
    def avail_connectors(self):
        return self._avail_connectors

    @property
    def defaults(self):

        tmp = {"model":self._default_model,
               "units":self._default_units,
               "shot_start":self._default_shot_start}

        return tmp

    @property
    def continuous_update(self):
        return self._continuous_update
