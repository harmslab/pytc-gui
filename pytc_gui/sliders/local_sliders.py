from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc
import inspect, math

from .add_global_connector import AddGlobalConnectorWindow
from .base import Sliders
from .. import exp_frames

class LocalSliders(Sliders):
    """
    create sliders for a local exp object
    """

    def __init__(self, param_name, value, parent):
        """
        """
        self._value = value
        self._global_var = parent._global_var
        self._slider_list = parent._slider_list
        self._connectors_seen = parent._connectors_seen
        self._global_connectors = parent._global_connectors
        self._global_tracker = parent._global_tracker
        self._exp_box = parent._exp_box
        self._main_box = parent._main_box
        self._if_connected = None

        super().__init__(param_name, parent)

    def bounds(self):
        """
        update the min max for the slider
        """
        exp_range = self._exp.model.param_guess_ranges[self._param_name]

        self._min = exp_range[0]
        self._max = exp_range[1]

        super().bounds()

        self._link = QComboBox(self)
        self._link.addItem("Unlink")
        self._link.addItem("Add Global Var")
        self._link.addItem("Add Connector")

        # update lists of variables for each new slider, check if var is a string or a connector object
        for i in self._global_var:
            if isinstance(i, str):
                self._link.addItem(i)
            else: 
                for p, v in i.local_methods.items():
                    self._link.addItem(p)

        self._link.activated[str].connect(self.link_unlink)
        self._main_layout.addWidget(self._link, 1, 3)

        self._main_box.fit_signal.connect(self.set_fit_true)

    def link_unlink(self, status):
        """
        add global variable, update if parameter is linked or not to a global paremeter
        """
        if status == "Unlink":
            try:
                self._fitter.unlink_from_global(self._exp, self._param_name)
                self.reset()
                self._global_tracker[self._if_connected].unlinked(self)
            except:
                pass

        elif status == "Add Global Var":
            text, ok = QInputDialog.getText(self, "Add Global Variable", "Var Name: ")
            if ok: 
                self._global_var.append(text)
                for e in self._slider_list["Local"].values():
                    for i in e:
                        i.update_global(text)

                index = self._link.findText(text)
                self._link.setCurrentIndex(index)
                self.global_link(text)
            else:
                i = self._link.findText("Unlink")
                self._link.setCurrentIndex(i)

        elif status == "Add Connector":
    
            def connector_handler(connector,var_names,curr_var):
        
                self._global_var.append(connector)
                for v in var_names:
                    self._global_connectors[v] = [connector.local_methods[v], connector]

                # Append connector methods to dropbdown lists
                for p, v in connector.local_methods.items():
                    for e in self._slider_list["Local"].values():
                        for i in e:
                            i.update_global(p)

                index = self._link.findText(curr_var)
                self._link.setCurrentIndex(index)
                self.connector_link(curr_var)
            
            self.diag = AddGlobalConnectorWindow(connector_handler)
            self.diag.show()

        elif status not in self._global_connectors:
            # connect to a simple global variable
            self.global_link(status)
        else:
            # connect to global connector
            self.connector_link(status)

    def global_link(self,var):
        """
        """
        # connect to a simple global variable
        self._fitter.link_to_global(self._exp, self._param_name, var)
        self._slider.hide()
        self._param_guess_label.hide()
        self._fix.hide()
        self._update_min_label.hide()
        self._update_min.hide()
        self._update_max_label.hide()
        self._update_max.hide()

        # set current connected name
        self._if_connected = var

        # add global exp to experiments widget
        if var not in self._slider_list["Global"]:
            # create global exp object and add to layout
            param_obj = self._fitter.global_param[var]
            global_e = exp_frames.GlobalBox(var, param_obj, self)
            self._global_tracker[var] = global_e
            self._exp_box.addWidget(global_e)

            print("global added")

        self._global_tracker[var].linked(self)

    def connector_link(self,var):
        """
        """
        # connect to global connector
        self._slider.hide()
        self._param_guess_label.hide()
        self._fix.hide()
        self._update_min_label.hide()
        self._update_min.hide()
        self._update_max_label.hide()
        self._update_max.hide()

        curr_connector = self._global_connectors[var][1]
        name = curr_connector.name
        self._connectors_seen[self._exp].append(curr_connector)
        self._fitter.link_to_global(self._exp, self._param_name, self._global_connectors[var][0])

        # add connector to experiments widget
        if name not in self._slider_list["Global"]:
            self._slider_list["Global"][name] = []

            # create a connector holder and add to layout
            connector_e = exp_frames.ConnectorsBox(name, curr_connector, self)
            self._exp_box.addWidget(connector_e)
            self._global_tracker[name] = connector_e

        self._global_tracker[name].linked(self)

        # set current connected name
        self._if_connected = name

        # check for instances of LocalBox and update
        for loc_obj in self._exp_box.parentWidget().findChildren(exp_frames.LocalBox):
            loc_obj.update_req()

    def update_global(self, value):
        """
        update the list of global parameters in combobox
        """
        self._link.addItem(value)

    def reset(self):
        """
        if global exp object deleted, return local slider object to unlinked state
        """
        self._slider.show()
        self._param_guess_label.show()
        self._fix.show()
        self._update_min_label.show()
        self._update_min.show()
        self._update_max_label.show()
        self._update_max.show()

        unlink_index = self._link.findText("Unlink", Qt.MatchFixedString)
        self._link.setCurrentIndex(unlink_index)
        
    def update_bounds(self):
        """
        update min/max bounds and check if range needs to be updated as well
        """
        bounds = [self._min, self._max]
        self._fitter.update_bounds(self._param_name, bounds, self._exp)

        # check if bounds are smaller than range, then update.
        curr_range = self._exp.model.param_guess_ranges[self._param_name]
        curr_bounds = self._exp.model.bounds[self._param_name]

        if curr_range[0] < curr_bounds[0] or curr_range[1] > curr_bounds[1]:
            self._fitter.update_range(self._param_name, bounds, self._exp)

