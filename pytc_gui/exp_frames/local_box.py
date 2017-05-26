from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc
import inspect

from .base import Experiments
from .. import slider_popup
from .. import sliders

class LocalBox(Experiments):
    """
    hold local parameters/sliders
    """

    def __init__(self, exp, name, parent):

        self._exp = exp
        self._required_fields = {}
        self._experiments = parent._experiments
        self._exp_box = parent._exp_box
        self._update = parent._update
        self._main_box = parent

        super().__init__(name, parent)

    def exp_widgets(self):
        """
        create sliders for experiment
        """
        parameters = self._exp.param_values

        for p, v in parameters.items():
            s = sliders.LocalSliders(p, v, self)
            self._slider_list["Local"][self._exp].append(s)

    def shots(self):
        """
        shots layout
        """
        # change shot start
        self._change_shots = QLineEdit(self)
        self._change_shots.setFixedWidth(120)
        self._change_shots.setPlaceholderText("Change Shot Start")
        self._change_shots.returnPressed.connect(self.update_shots)
        self._main_layout.addWidget(self._change_shots)

    def slider_popup(self):
        """
        hide and show slider window
        """
        self._slider_window = slider_popup.LocalPopUp(self)
        self._slider_window.show()

    def update_shots(self):
        """
        change the shot start
        """
        text = self._change_shots.text()

        if text.isdigit():
            try:
                new_start = int(text)
                setattr(self._exp, 'shot_start', new_start)
                self._update()
                print("shot start updated to " + text + "\n")
            except:
                print("shots out of bounds")
        else:
            error_message = QMessageBox.warning(self, "warning", "field only takes integers", QMessageBox.Ok)
                
    def update_req(self):
        """
        checks if any global connectors are connected and updates to add fields for any required data
        """
        exp_connectors = self._connectors_seen[self._exp]

        for c in exp_connectors:
            required = c.required_data
            for i in required:
                if i not in self._required_fields:
                    label_name = str(i).replace("_", " ") + ": "
                    label = QLabel(label_name.title(), self)
                    field = QLineEdit(self)
                    field.setMinimumWidth(150)
                    field.setPlaceholderText("values in kcal/mol or C°")
                    self._required_fields[i] = field

                    stretch = QHBoxLayout()
                    stretch.addWidget(label)
                    stretch.addWidget(field)
                    stretch.addStretch(1)

                    self._req_layout.addLayout(stretch)
                else:
                    pass
                    
    def set_attr(self):
        """
        update data from global connector fields
        """
        for n, v in self._required_fields.items():
            if v.text():
                try:
                    val = float(v.text())
                except:
                    val = v.text()

                setattr(self._exp, n, val)
            else:
                error_message = QMessageBox.warning(self, "Fit Unsuccessful!", "Empty required data fields present", QMessageBox.Ok)

    def remove(self):
        """
        """
        self._fitter.remove_experiment(self._exp)
        self._slider_list["Local"].pop(self._exp, None)
        self.close()
