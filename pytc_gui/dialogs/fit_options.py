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
                entry = QW.QLineEdit(self)
                entry.setText(str(self._fitter_defaults[-1][n]))

                self._fitter_vars[-1][n] = entry
                self._fitter_options[-1].addRow(label, entry)

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
            kwargs[k] = ast.literal_eval(v.text())

        self._fit.fit_engine = self._fitter_classes[self._current_selection](**kwargs)

        self.hide()
