from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc
import inspect

class ExpOptions(QDialog):
    
    def __init__(self, parent):
        """
        """
        super().__init__()
        
        self._exp = parent._exp
        self._update = parent._update

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

        classes = inspect.getmembers(self._exp, inspect.isclass)
        properties = inspect.getmembers(classes[0][1], lambda o: isinstance(o, property))

        setters = [p[0] for p in properties if p[1].fset != None]

        for s in setters:
            if "heats" not in s:
                self._option_widgets[s] = QLineEdit(self)
                name = str(s).replace("_", " ") + ": "
                self._form_layout.addRow(QLabel(name.title()), self._option_widgets[s])
        
    def _update_val(self):
        """
        """

        for k, v in self._option_widgets.items():
            try:
                val = int(v.text())
                setattr(self._exp, k, val)
                self._update()
                name = str(k).replace("_", " ") + ": "
                print(name + " updated to " + v.text() + "\n")
            except:
                print("out of bounds")
                