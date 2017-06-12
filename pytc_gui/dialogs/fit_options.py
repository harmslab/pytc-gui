__description__ = \
"""
Fit options dialog for pytc-gui.
"""
__author__ = "Hiranmayi Duvvuri"
__date__ = "2017-06-01"

from PyQt5.QtCore import pyqtSignal 
from PyQt5 import QtWidgets as QW

import pytc

import inspect, ast


class InputWidget(QW.QWidget):
    """
    This class wraps a single piece of input intelligently in a gui.
    """

    def __init__(self,initial_value):
        """
        Initialize the class.

        initial_value: initial value (used to figure out how to display)
        """

        super().__init__()

        self._initial_value = initial_value

        self._input_type = type(self._initial_value)
        self._current_value = self._initial_value
        self._valid = True

        self._layout()

    def _layout(self):
        """
        Create layout.
        """

        self._main_layout = QW.QHBoxLayout(self)

        if self._input_type is bool:
            self._select_widget = QW.QCheckBox()
            self._select_widget.stateChanged.connect(self._bool_handler)
            self._select_widget.setChecked(self._initial_value)
        elif self._input_type is str:
            self._select_widget = QW.QLineEdit()
            self._select_widget.editingFinished.connect(self._str_handler)
            self._select_widget.setText(self._initial_value)
        elif self._input_type is int:
            self._select_widget = QW.QLineEdit()
            self._select_widget.editingFinished.connect(self._int_handler)
            self._select_widget.setText(str(self._initial_value))
        else:
            self._select_widget = QW.QLineEdit()
            self._select_widget.editingFinished.connect(self._general_handler)
            self._select_widget.setText(str(self._initial_value))

        self._main_layout.addWidget(self._select_widget)
        
    def _bool_handler(self,value):
        """
        Handler for bool values.  Parses QCheckBox.
        """
             
        value = self._select_widget.checkState() 
        self._current_value = value
        self._valid = True

    def _str_handler(self):
        """
        Handler for string values. Parses QLineEdit.
        """

        current = self._select_widget.text()
        try:
            new_value = current.strip()
            if new_value == "":
                raise ValueError
            color = "#FFFFFF"
            self._current_value = new_value
            self._valid = True
        except ValueError:
            color = "#FFB6C1"
            self._valid = False
        
        self._select_widget.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))

    def _int_handler(self):
        """
        Handler for int values.  Parses QLineEdit.
        """
        current = self._select_widget.text()
        try:

            # Make sure this scans as a string 
            if type(ast.literal_eval(current)) != int:
                raise ValueError   

            new_value = int(current)
            color = "#FFFFFF"
            self._current_value = new_value
            self._valid = True
        except ValueError:
            color = "#FFB6C1"
            self._valid = False
        
        self._select_widget.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
      
    def _general_handler(self):
        """
        Handler for general values.  Parses QLineEdit.
        """
        current = self._select_widget.text()
        try:
            new_value = self._input_type(current)
            color = "#FFFFFF"
            self._current_value = new_value
            self._valid = True
        except ValueError:
            color = "#FFB6C1"
            self._valid = False
        
        self._select_widget.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
    
    @property
    def current_value(self):
        """
        Current parsed value of widget.
        """

        if not self._valid:
            raise ValueError("invalid value")

        return self._current_value
 

class FitOptions(QW.QDialog):
    """
    Fit options dialog for pytc-gui.
    """

    def __init__(self, parent, fit):
        """
        """
        super().__init__()

        self._parent = parent
        self._fit = fit

        self.layout()

    def _load_fitter_info(self):
        """
        Load fitter info from pytc.
        """

        # get list of Fitter subclasses, sorted by name
        objects = []
        for name, obj in inspect.getmembers(pytc.fitters):
            if inspect.isclass(obj):
                objects.append((name,obj))
        objects.sort() 

        self._fitter_classes = []
        self._fitter_vars = []
        self._fitter_widgets = []   
        self._fitter_options = []
        self._fitter_names = []
        self._fitter_radio_buttons = []
        self._fitter_defaults = []

        # For every Fitter subclass...
        for name, obj in objects:

            self._fitter_classes.append(obj)

            # Make new widget
            self._fitter_widgets.append(QW.QFrame())
            self._fitter_options.append(QW.QFormLayout(self._fitter_widgets[-1]))
          
            # Add name and radio button to widget 
            self._fitter_names.append(name.replace("Fitter",""))
            self._fitter_radio_buttons.append(QW.QRadioButton(self._fitter_names[-1]))
            self._fitter_radio_buttons[-1].toggled.connect(self._select_fit)
   
            # Figure out arguments for this Fitter subclass 
            args = inspect.getargspec(obj)
            if len(args.args) == 1 and args.defaults is None:
                self._fitter_defaults.append({})
            else:
                self._fitter_defaults.append({arg: param for arg, param in
                                              zip(args.args[1:], args.defaults)})

            fitter_keys = list(self._fitter_defaults[-1].keys())
            fitter_keys.sort()

            # Append fit option
            self._fitter_vars.append({})    
            for n in fitter_keys:

                label_name = str(n).replace("_", " ") + ": "
                label = QW.QLabel(label_name.title(), self)
                entry = InputWidget(self._fitter_defaults[-1][n])
        
                self._fitter_vars[-1][n] = entry
                self._fitter_options[-1].addRow(label,entry)

        # map from name back to index in lists above                                
        self._fitter_name_to_index = dict([(v,i) for i, v in enumerate(self._fitter_names)])   

 
    def layout(self):
        """
        Create widget layout.
        """
    
        # Load possible fitters
        self._load_fitter_info()
       
        # Create the window 
        self.setWindowTitle("Fit Options")
        main_layout = QW.QVBoxLayout(self)

        # Header name
        fit_header = QW.QLabel("Choose fit type: ")
        main_layout.addWidget(fit_header)

        # Create radio group for selecting fit types
        radio_group = QW.QHBoxLayout()
        for b in self._fitter_radio_buttons:
            radio_group.addWidget(b)
        main_layout.addLayout(radio_group)

        # Select the default fitter
        try:
            default_index = self._fitter_name_to_index[self._fit.defaults["default_fitter"]]
        except KeyError:
            default_index = 0
        self._current_selection = default_index 
        self._fitter_radio_buttons[default_index].setChecked(True) 
        
        # Add fitting widgets
        for w in self._fitter_widgets:
            main_layout.addWidget(w)
      
        # Add OK button 
        OK_button = QW.QPushButton("OK", self)
        OK_button.clicked.connect(self._ok_handler)
        main_layout.addWidget(OK_button)

    def _select_fit(self):
        """
        Choose which fitter option widget to display.
        """
        b = self.sender()
        for k in self._fitter_name_to_index.keys():

            f_index = self._fitter_name_to_index[k]
            if k == b.text() and b.isChecked():
                self._fitter_widgets[f_index].show()
                self._current_selection = f_index
            else:
                self._fitter_widgets[f_index].hide()         

        self.adjustSize()

    def _ok_handler(self):
        """
        Handle okay, updating self._fit with new fitter.
        """

        kwargs = {}
        for k, v in self._fitter_vars[self._current_selection].items():
            try:
                kwargs[k] = v.current_value
            except ValueError:
                error_message = QW.QMessageBox.warning(self, "warning", "Not all fit options are valid", QW.QMessageBox.Ok)
                return

        self._fit.fit_engine = self._fitter_classes[self._current_selection](**kwargs)

        self.hide()
