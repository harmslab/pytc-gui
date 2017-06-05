from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc

import inspect, ast

class ExpOptions(QDialog):
    """
    Dialog that allows the user to set options for an experiment. 
    """   
 
    def __init__(self, parent,experiment):
        """
        """
        super().__init__()
      
        self._parent = parent  
        self._update = parent._main_box
        self._experiment = experiment

        self.layout()

    def layout(self):
        """
        """
        main_layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()
        self._get_info()

        update_button = QPushButton("Update", self)
        update_button.clicked.connect(self._update_val)

        main_layout.addLayout(self._form_layout)
        main_layout.addWidget(update_button)

        self.setWindowTitle('Experiment Options')

    def _get_info(self):
        """
        get any properties that can be change for the experiment
        """
        self._option_widgets = {}

        classes = inspect.getmembers(self._experiment, inspect.isclass)
        properties = inspect.getmembers(classes[0][1], lambda o: isinstance(o, property))

        setters = [p[0] for p in properties if p[1].fset != None]

        for i, s in enumerate(setters):

            # Skip heats (which has setter we need to ignore)
            if s in ["heats","heats_stdev"]:
                continue

            if s == "units":
                units_names = list(self._experiment.AVAIL_UNITS)
                units_names.sort()

                starting_index = 0
                self._option_widgets[s] = QComboBox(self)
                for j, k in enumerate(units_names):
                    self._option_widgets[s].addItem(k)
                    if k == self._experiment.units:
                        starting_index = j
                self._option_widgets[s].setCurrentIndex(starting_index)        

                name = str(s).replace("_", " ") + ": "
                self._experiment.units = str(self._option_widgets[s].currentText())
                self._option_widgets[s].activated[str].connect(self._units_select)
                self._form_layout.addRow(QLabel(name), self._option_widgets[s])

            else:
                self._option_widgets[s] = QLineEdit(self)
                self._option_widgets[s].setText(str(getattr(self._experiment,s)))

                name = str(s).replace("_", " ") + ": "
                self._form_layout.addRow(QLabel(name.title()), self._option_widgets[s])

    def _update_val(self):
        """
        """

        for k, v in self._option_widgets.items():
   
            try: 
                if type(v) == QComboBox:
                    val = str(v.currentText())
                else:
                    val = ast.literal_eval(str(v.text()))

                setattr(self._experiment, k, val)

            except ValueError:

                if type(v) == QComboBox:
                    val = str(v.currentText())
                else:
                    val = str(v.text())
                
                error_message = QMessageBox.warning(self,
                                                    "warning",
                                                    "Value {} is invalid".format(val),
                                                    QMessageBox.Ok) 
                return

        self._update.update()
        self.hide()
               
    def _units_select(self,units):
        self._experiment.units = units
 
