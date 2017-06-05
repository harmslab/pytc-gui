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

class FitContainer:
    """
    """

    def __init__(self,default_units="cal/mol",
                      default_model="Single Site",
                      default_shot_start=1):
        """
        """

        self._default_units = default_units
        self._default_model = default_model
        self._default_shot_start = default_shot_start

        self._fitter = pytc.GlobalFit()

        self._experiment_labels = []
        self._experiments = []
        self._connectors = []

        # Available model types
        self._avail_models = {re.sub(r"(\w)([A-Z])", r"\1 \2", i.__name__):i
                              for i in pytc.indiv_models.ITCModel.__subclasses__()}
        self._avail_model_keys = list(self._avail_models.keys())        
        self._avail_model_keys.sort()

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

    @property
    def experiments(self):
        """
        """

        return self._experiments

    @property
    def experiment_meta(self):
        """
        """

        meta = []

        for e in self._experiments:

            classes = inspect.getmembers(e, inspect.isclass)
            properties = inspect.getmembers(classes[0][1], lambda o: isinstance(o, property))

            setters = [p[0] for p in properties if p[1].fset != None]

            meta.append([{},{}])
            meta[-1][0]["model"] = e.model

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

                meta[-1][1][s] = (current_value,value_type,avail_values)

        return meta

    def add_experiment(self,name,*args,**kwargs):
        """
        """
  
        self._experiment_labels.append(name) 
        self._experiments.append(pytc.ITCExperiment(*args,**kwargs))
        self._fitter.add_experiment(self._experiments[-1])
   
    def replace_experiment(self,index,*args,**kwargs):
        
        try:
            old_expt = self._experiments[index]
            self._fitter.remove_experiment[old_expt]
            self._experiments[index] = pytc.ITCExperiment(*args,**kwargs)
            self._fitter.add_experiment(self._experiments[index])
        except IndexError:
            err = "No experiment with index {} found\n".format(index)
            raise IndexError(err) 

    def remove_experiment(self,index):
        """
        """

        try:
            self._experiment_labels.pop(index)
            to_remove = self._experiments.pop(index)
            self._fitter.remove_experiment(to_remove)
        except IndexError:
            err = "No experiment with index {} found\n".format(index)
            raise IndexError(err) 
           
    @property
    def connectors(self):
        """
        """

        return self._connectors

    @property
    def connector_meta(self):

        meta = []
        for c in self._connectors:
            meta.append(c)
        return meta

    def add_connector(self,connector,*args,**kwargs):
        """
        """

        self._connectors.append(connector(*args,**kwargs))

    def replace_connector(self,index,connector,*args,**kwargs):
        
        try:
            self._connectors[index] = connector(*args,**kwargs)
        except IndexError:
            err = "No connector with index {} found\n".format(index)
            raise IndexError(err) 

    def remove_connector(self,index):

        try:
            to_remove = self._connectors.pop(index)
        except IndexError:
            err = "No connector with index {} found\n".format(index)
            raise IndexError(err) 

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

    @property
    def defaults(self):

        tmp = {"model":self._default_model,
               "units":self._default_units,
               "shot_start":self._default_shot_start}

        return tmp
