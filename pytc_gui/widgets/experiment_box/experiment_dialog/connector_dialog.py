__description__ = \
"""
Dialog that pops up when user connects a global_connector variable to an
existing experiment.
""" 
__author__ = "Michael J. Harms"
__date__ = "2017-06-06"

from PyQt5 import QtWidgets as QW

import inspect

class AddConnectorDialog(QW.QDialog):
    """
    Dialog box for adding a new global connector to the fit.
    """

    def __init__(self,parent,fit,experiment,fit_param):
        """
        parent: parent widget instance
        fit: FitContainer instance
        experiment: pytc.ITCExperiment instance holding fit parameter
        fit_param: pytc.FitParam instance holding fittable parameter
        """

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment
        self._p = fit_param

        self.layout()

    def layout(self):
        """
        Populate the window.
        """

        self._main_layout = QW.QVBoxLayout(self)
        self._form_layout = QW.QFormLayout()

        # Combobox widget holding possible connectors
        self._connector_select_widget = QW.QComboBox(self)

        connector_names = list(self._fit.avail_connectors.keys())
        connector_names.sort()
        for n in connector_names:
            self._connector_select_widget.addItem(n)

        self._connector_select_widget.setCurrentIndex(0)
        self._connector_select_widget.activated.connect(self._update_dialog)

        # Input box holding name
        self._connector_name_input = QW.QLineEdit(self)
        self._connector_name_input.setText("connector")
        self._connector_name_input.textChanged.connect(self._update_connector_name)

        # Final OK button
        self._OK_button = QW.QPushButton("OK", self)
        self._OK_button.clicked.connect(self._ok_button_handler)

        # Add to form
        self._form_layout.addRow(QW.QLabel("Select Model:"), self._connector_select_widget)
        self._form_layout.addRow(QW.QLabel("Name:"), self._connector_name_input)

        # Populate widgets
        self._arg_widgets = {}
        self._update_dialog()

        # add to main layout
        self._main_layout.addLayout(self._form_layout)
        self._main_layout.addWidget(self._OK_button)

        self.setWindowTitle('Add new global connector')

    def _update_dialog(self):
        """
        Resize and repopulate dialog according to the connector in question.
        """

        self.adjustSize()

        # remove args from form layout
        for l in self._arg_widgets.values():
            widget_labeled = self._form_layout.labelForField(l)
            if widget_labeled is not None:
                widget_labeled.deleteLater()
            l.deleteLater()

        # check if parameter label even there
        try:
            param_label = self._form_layout.labelForField(self._parameter_name_box)
            if param_label is not None:
                param_label.deleteLater()
            self._parameter_name_box.deleteLater()
        except:
            pass

        # Grab connector and name
        self._selected_connector_key = self._connector_select_widget.currentText()
        self._connector_name = self._connector_name_input.text()

        # Connector class   
        connector = self._fit.avail_connectors[self._selected_connector_key]

        # Create instance of connector class
        self._selected_connector = connector(name=self._connector_name)

        # Figure out the args that are specific to this connector
        new_fields = {}
        connector_args = inspect.getargspec(connector.__init__)
        try:
            offset = len(connector_args.args) - len(connector_args.defaults)
            for i in range(len(connector_args.defaults)):
                new_fields[connector_args.args[i + offset]] = connector_args.defaults[i]

        # TypeError indicates no args...
        except TypeError:
            pass

        # Add the newly selected args back into the connector
        self._arg_types = {}
        self._arg_widgets = {}
        for k, v in new_fields.items():

            self._arg_types[k] = type(v)

            label = QW.QLabel(k,self)
            if type(v) == bool:
                chooser = QW.QCheckBox(self)
                chooser.setChecked(v)
                self._arg_widgets[k] = chooser
            else:
                box = QW.QLineEdit(self)
                box.setText("{}".format(v))
                box.textChanged.connect(self._widget_checker)
                self._arg_widgets[k] = box

            self._form_layout.addRow(label, box)

        # Create dropdown box for the parameter name to select
        label = QW.QLabel("Select parameter",self)
        self._parameter_name_box = QW.QComboBox(self)

        # Add the dropdown box to the list
        self._form_layout.addRow(label, self._parameter_name_box)

        # Update the list of parameters that can be selected
        self._update_param_box()

    def _update_connector_name(self):
        """
        If the user alters the name of the connector, update the parameters.
        """

        # Change inside of connector and update dropdown box with parameters to select
        self._selected_connector.name = self._connector_name_input.text()
        self._update_param_box()

    def _update_param_box(self):
        """
        Update the parameter box.
        """
        
        # Clear existing entries in the dropbox
        self._parameter_name_box.clear()

        # Update the names of the parameters
        self._param_names = list(self._selected_connector.local_methods.keys())
        self._param_names.sort()
        for k in self._param_names:
            self._parameter_name_box.addItem(k)
    
    def _widget_checker(self):
        """
        Make sure widgets are good, turning bad widgets pink.
        """
   
        for k in self._arg_widgets.keys():

            caster = self._arg_types[k]
            if caster == bool:
                continue

            try:
                value = caster(self._arg_widgets[k].text())
                if type(value) is str and value.strip() == "":
                    raise ValueError 
                color = "#FFFFFF"
            except ValueError:
                color = "#FFB6C1"

            self._arg_widgets[k].setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
 
    def _ok_button_handler(self):
        """
        Handle OK button.
        """

        # Grab connector and name
        self._selected_connector_key = self._connector_select_widget.currentText()
        self._connector_name = self._connector_name_input.text()
    
        # Connector class   
        connector = self._fit.avail_connectors[self._selected_connector_key]

        # Create kwargs to initialize the connector
        kwargs = {} 
        for k, widget in self._arg_widgets.items():

            caster = self._arg_types[k]

            # Grab boolean
            if caster == bool:
                final_value = widget.checkState()
            else:
 
                # Parse the non-boolean value.
                value = widget.text()
                try:
                    final_value = caster(value)
                    if type(final_value) is str and final_value.strip() == "":
                        raise ValueError
                except ValueError:
                    self._widget_checker()
                    return
                          
            kwargs[k] = final_value

        # Create connector
        self._selected_connector = connector(name=self._connector_name,
                                             **kwargs)

        # Get currently selected parameter name
        var_name = self._parameter_name_box.currentText()

        # Create connector
        self._fit.add_connector(self._connector_name,self._selected_connector)

        self._fit.link_to_global(self._experiment,
                                 self._p.name,
                                 self._selected_connector.local_methods[var_name])

        self._parent.set_as_connected(True)

        self.accept()
