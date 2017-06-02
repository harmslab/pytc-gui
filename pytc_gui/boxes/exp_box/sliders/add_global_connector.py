from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import string, random, inspect, ast

import pytc

class AddGlobalConnectorWindow(QDialog):
    """
    Construct a window that allows the user to build a GlobalConnector object.
    """

    def __init__(self, end_function):
        """
        :param end_function: a function to call when the "OK" button is called.  This
                             should take the connector and param_name to use.
        """
    

        super().__init__()

        self._end_function = end_function

        # Figure out the global connectors loaded
        possible_subclasses = pytc.global_connectors.GlobalConnector.__subclasses__()
        self._global_connectors = dict([(s.__name__,s) for s in possible_subclasses])

        self.layout()

    def layout(self):
        """
        Populate the window.
        """

        main_layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()

        # Combobox widget holding possible connectors
        self._connector_select_widget = QComboBox(self)
        connector_names = list(self._global_connectors.keys())
        connector_names.sort()
        for n in connector_names:
            self._connector_select_widget.addItem(n)
        self._connector_select_widget.setCurrentIndex(0)

        # Connector selection call back
        self._connector_select_widget.activated[str].connect(self._update_connector)

        # Input box holding name
        self._connector_name_input = QLineEdit(self)

        random_name = "".join([random.choice(string.ascii_letters) for i in range(3)])
        self._connector_name_input.setText(random_name)

        # Connector name call back
        self._connector_name_input.textChanged[str].connect(self._update_connector_name)

        # Final OK button
        self._OK_button = QPushButton("OK", self)
        self._OK_button.clicked.connect(self._return_final_connector)

        # add to form
        self._form_layout.addRow(QLabel("Select Model:"), self._connector_select_widget)
        self._form_layout.addRow(QLabel("Name:"), self._connector_name_input)

        # Populate widgets
        self._arg_widgets = {}
        self._update_connector()

        # add to main layout
        main_layout.addLayout(self._form_layout)
        main_layout.addWidget(self._OK_button)

        self.setWindowTitle('Add new global connector')

    def _update_connector(self):
        """
        If the user selects a new connector, repopulate the window appropriately.
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
        connector = self._global_connectors[self._selected_connector_key]

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
        self._arg_widgets = {}
        for k, v in new_fields.items():

            label = QLabel(k,self)
            box = QLineEdit(self)
            box.setText("{}".format(v))

            self._arg_widgets[k] = box

            self._form_layout.addRow(label, box)

        # Create dropdown box for the parameter name to select
        label = QLabel("Select parameter",self)
        self._parameter_name_box = QComboBox(self)

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
        
        # Clear existing entries in the dropbox (it's the last widget)
        self._parameter_name_box.clear()

        # Update the names of the parameters
        self._param_names = list(self._selected_connector.local_methods.keys())
        self._param_names.sort()
        for k in self._param_names:
            self._parameter_name_box.addItem(k)
        
    def _return_final_connector(self):
        """
        Construct the final connector, run the end_function, and close.
        """

        # Grab connector and name
        self._selected_connector_key = self._connector_select_widget.currentText()
        self._connector_name = self._connector_name_input.text()
    
        # Connector class   
        connector = self._global_connectors[self._selected_connector_key]

        # Create kwargs to initialize the connector
        kwargs = {} 
        for k, widget in self._arg_widgets.items():
        
            # Parse the value.  
            value = widget.text()

            try:
                final_value = ast.literal_eval(value)
            except ValueError:
                if value.lower() in ["true","t"]:
                    final_value = True
                elif value.lower() in ["false","f"]:
                    final_value = False
                elif value.lower() == "none":
                    final_value = None
                else:
                    final_value = str(value)

            kwargs[k] = final_value

        # Create connector
        self._selected_connector = connector(name=self._connector_name,
                                             **kwargs)

        # Get currently selected parameter name
        var_name = self._parameter_name_box.currentText()

        # Pass data back
        self._end_function(self._selected_connector,self._param_names,var_name)

        self.close()
    
