__description__ = \
"""
Class for holding on to the global fit object and associated experiments.  
Instance of class is passed to all gui objects and used to manipulate fit in
a coherent fashion.  This also stores session preferences and coordinates widget
updates by emitting a signal when the fit changes.
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
    event_logger = QC.pyqtSignal(str,str)

    def __init__(self,default_units="cal/mol",
                      default_model="Single Site",
                      default_shot_start=1,
                      default_fitter="ML",
                      continuous_update=True,
                      verbose=True):
        """
        default_units: default units for heats
        default_model: default model for fits
        default_shot_start: default start for shots
        continuous_update: whether or not to update graph and params as
                           parameters are modified
        verbose: how much output to write out
        """

        super().__init__()

        self._default_units = default_units
        self._default_model = default_model
        self._default_shot_start = default_shot_start
        self._default_fitter = default_fitter
        self._continuous_update = continuous_update
        self._verbose = verbose

        # This is the main fitting object used throughout the session
        self._fitter = pytc.GlobalFit()
        self._fit_engine = None

        # This holds all experiments
        self._experiments = []
        self._experiment_labels = {}
    
        # This holds all connectors
        self._connectors = []
        self._connector_labels = {}

        # ---------------------------------------------------------------------
        # now use some cleaver inspect calls to figure out what is available in
        # the underlying pytc api.

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

    def do_fit(self):
        """
        Actually do the global fit.
        """

        self.event_logger.emit("","")
        self.event_logger.emit("Attempting fit","fit_start")

        try:
            if self._fit_engine is None:
                self._fitter.fit()
            else:
                self._fitter.fit(fitter=self._fit_engine)

        except Exception as ex:
            s = "Fit failed. pytc threw <br/>\"\"\"{0} Args: {1!r}\"\"\""
            err = s.format(type(ex).__name__,ex.args)
            self.event_logger.emit(err,"warning")

        self.emit_changed()

        self.event_logger.emit("","")
        if self._fitter.fit_success:
            self.event_logger.emit("Fit successful.","happy")
        else:
            self.event_logger.emit("Fit failed.","warning")

    def add_experiment(self,name,*args,**kwargs):
        """
        Add an experiment to the FitContainer. 
        """
 
        # Add the experiment 
        self._experiments.append(pytc.ITCExperiment(*args,**kwargs))

        self._fitter.add_experiment(self._experiments[-1])
        self._experiment_labels[self._experiments[-1]] = name 

        # Record the unit of this experiment if it is the only experiment
        if len(self._experiments) == 1:
            self._fit_units = self._experiments[0].units

        self.event_logger.emit("Loaded experiment {} as {}".format(args[0],name),"info")

        # Indicate the fit changed
        self.emit_changed()

    def remove_experiment(self,experiment):
        """
        Remove an experiment from the FitContainer.
        """

        try:
            name = self._experiment_labels.pop(experiment)
        except KeyError:
            pass

        try:
            index = self._experiments.index(experiment)
            to_remove = self._experiments.pop(index)
            self._fitter.remove_experiment(experiment)
            self.event_logger.emit("Removed experiment {}".format(name),"info")
            self.emit_changed()
        except ValueError:
            pass
            #err = "experiment {} not found\n".format(experiment)
            #raise ValueError(err) 
 
        # We no longer have a fixed set of units if there is no experiment
        # left.
        if len(self._experiments) == 0:

            try:
                del self._fit_units
            except AttributeError:
                pass

    def add_connector(self,name,connector):
        """
        Add a connector.
        """

        self._connectors.append(connector)
        self._connector_labels[self._connectors[-1]] = name
        self.event_logger.emit("Connector {} created".format(name),"info")
        self.emit_changed()

    def remove_connector(self,c):
        """
        Remove a connector.
        """

        try:
            name = self._connector_labels.pop(c)

            index = self._connnectors.index(c)
            to_remove = self._connectors.pop(index)

            # Remove all links to experiments
            for k in c.params.keys():
                self._fitter.remove_global(k)

            self.event_logger.emit("Connector {} remove".format(name),"info")
            self.emit_changed()

        except IndexError:
            err = "No connector with index {} found\n".format(c)
            raise IndexError(err) 

    def link_to_global(self,e,param_name,global_param):
        """
        link parameter (param_name) from experiment (e) to the global_param.
        """

        # Remove link, if present
        try:
            self._fitter.unlink_from_global(e,param_name)
        except KeyError:
            pass

        # Update fit
        self._fitter.link_to_global(e,param_name,global_param)
        self.emit_changed()

    def unlink_from_global(self,e,param_name):
        """
        Unlink paramter from global.
        
        e: ITCExperiment instance
        param_name: local param name
        """
    
        try:
            self._fitter.unlink_from_global(e,param_name)
            self.emit_changed()
        except KeyError:
            pass
        
    def set_experiment_attr(self,e,attr,value,purge_fit=False):
        """
        Set an experimental attribute.
        
        e: ITCExperiment instance
        attr: attribute
        value: value to set attribute to.

        purge_fit: whether or not to delete existing fit in the GlobalFit 
                   instance
        """

        setattr(e,attr,value)
        if purge_fit:
            self._fitter.delete_current_fit()

        self.emit_changed()

    def set_fix_parameter(self,e,param_name,param_value):

        self._fitter.delete_current_fit()
        self._fitter.update_fixed(param_name,param_value,e) 
        self.emit_changed()

    def get_experiment_param(self,e):
        """
        Return the fittable parameters of an experiment.
        """

        # Make sure the experiment is loaded
        if e not in self._experiments:
            err = "experiment {} not loaded".format(e)
            raise ValueError(err)

        # Grab model parameters
        param = {}
        param["model_name"] = e.model
        for key in e.model.parameters.keys():
            param[key] = e.model.parameters[key]

        return param

    def get_experiment_settable(self,e):
        """
        Return meta data that can be set for a given experiment.  This is a list
        of tuples of the form:

        [(value,value_type,possible_values) ... ]

        where value is the current value, value_type is the type ("multi" or a 
        stanard python type), and possible values is list-like (for "multi") or
        None for everything else.  
        """

        # Make sure the experiment is loaded
        if e not in self._experiments:
            err = "experiment {} not loaded".format(e)
            raise ValueError(err)

        # Get all setters for the fit pytc.ITCExperiment instance
        classes = inspect.getmembers(e, inspect.isclass)
        properties = inspect.getmembers(classes[0][1], lambda o: isinstance(o, property))
        setters = [p[0] for p in properties if p[1].fset != None]

        meta = {}
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

    def get_experiment_connector(self,e):
        """
        Figure out the connector fit parameters and required meta data
        associated with this experiment given its associated connectors.
        """

        # Make sure the experiment is loaded
        if e not in self._experiments:
            return {}, {}
            #err = "experiment {} not loaded".format(e)
            #raise ValueError(err)

        # Look through parameter aliases, searching for connector classes
        required_data = []
        final_fit_param = {}
        for a in e.model.param_aliases:

            this_alias = e.model.param_aliases[a]
            try: 
                # This will throw an AttributeError unless this is a connector
                # method
                connector_class = this_alias.__self__ 

                fit_parameters = connector_class.params
                for p in fit_parameters:
                    final_fit_param[p] = connector_class.params[p]

                required_data.extend(connector_class.required_data)  
 
            except AttributeError:
                continue

        # Make sure these are attributes of the experiment class
        final_required = {}
        for r in set(required_data):
            try:
                value = getattr(e,r)
            except AttributeError:
                setattr(e,r,None)
                value = getattr(e,r) 
     
            final_required[r] = value 
             
        return final_required, final_fit_param

    def get_experiment_aliases(self,e):
        """
        Return aliases associated with this experiment.
        """      
 
        try:
            index = self._experiments.index(e)
            return self._fitter.param_aliases[1][index]
        except ValueError:
            self.remove_experiment(e)
            #err = "experiment {} not loaded".format(e)
            #raise ValueError(err)
            
        return None

    def get_connector_param(self,avail_name):
        """
        Look up parameters for a initializing a connector.
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
        Clear the FitContainer object.
        """

        self.__init__(self._default_units,
                      self._default_model,
                      self._default_shot_start,
                      self._default_fitter,
                      self._continuous_update,
                      self._verbose)

    @property
    def connector_methods(self):

        out = {}        
        for c in self._connectors:
            for k in c.local_methods:
                out[k] = c.local_methods[k]

        return out

    @property
    def global_param(self):
        """
        Dictionary of all global fit parameters (as pytc.FitParam instances)
        """

        return self._fitter.global_param

    @property
    def fit_units(self):
        """
        Units for the fit.  All experiments must have the same units.  This helps
        enforce this.
        """
        return self._fit_units

    @property
    def fitter(self):
        """
        Main pytc GlobalFit instance.  
        """
        return self._fitter

    @property
    def experiments(self):
        """
        All loaded experiments (list).
        """
        return self._experiments

    @property
    def experiment_labels(self):
        """
        Dictionary keying experiments to their string labels
        """
        return self._experiment_labels

    @property
    def connectors(self):
        """
        All loaded connectors (list).
        """
        return self._connectors
    
    @property
    def connector_labels(self):
        """
        Dictionary keying connectors to their string labels.
        """
        return self._connector_labels
    

    @property
    def avail_models(self):
        """
        Available models for fitting.
        """
        return self._avail_models

    @property
    def avail_connectors(self):
        """
        Available connectors.
        """
        return self._avail_connectors

    @property
    def defaults(self):
        """
        Sundry defaults (dictionary).
        """

        tmp = {"model":self._default_model,
               "units":self._default_units,
               "shot_start":self._default_shot_start,
               "default_fitter":self._default_fitter}

        return tmp

    @property
    def continuous_update(self):
        """
        Whether or not to update widgets whenever a change is made.
        """

        return self._continuous_update

    @property
    def verbose(self):
        """
        How verbose to be in output.
        """
        return self._verbose

    @property
    def fit_engine(self):
        """
        Fitting engine (ML, Baysian, etc.).  This is an instance of pytc.Fitter
        class.
        """
        return self._fit_engine

    @fit_engine.setter
    def fit_engine(self,value):
        """
        Fitting engine (ML, Baysian, etc.).  This is an instance of pytc.Fitter
        class.
        """
        self._fit_engine = value
