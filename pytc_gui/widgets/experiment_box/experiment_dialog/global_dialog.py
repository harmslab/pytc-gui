__description__ = \
"""
Dialog that pops up when user wants to create a new global variable.
""" 
__author__ = "Michael J. Harms"
__date__ = "2017-06-06"

from PyQt5 import QtWidgets as QW

class AddGlobalDialog(QW.QDialog):
    """
    Dialog box for adding a new global variable.
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

        # Input box holding name
        self._global_var_input = QW.QLineEdit(self)
        self._global_var_input.setText("GLOBAL")
        self._global_var_input.textChanged.connect(self._check_name)

        # Final OK button
        self._OK_button = QW.QPushButton("OK", self)
        self._OK_button.clicked.connect(self._ok_button_handler)

        # Add to form
        self._form_layout.addRow(QW.QLabel("New Global Variable:"), self._global_var_input)

        # add to main layout
        self._main_layout.addLayout(self._form_layout)
        self._main_layout.addWidget(self._OK_button)

        self.setWindowTitle("Add new global variable")

    
    def _check_name(self):
        """
        Turn bad name pink.
        """
    
        value = self._global_var_input.text()
        value = value.strip()
       
        color = "#FFFFFF"
        if value.strip() == "":
            color = "#FFB6C1"
        if value in self._fit.global_param.keys():
            color = "#FFB6C1"

        self._global_var_input.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))
 
    def _ok_button_handler(self):
        """
        Handle OK button.
        """

        self._check_name()

        value = self._global_var_input.text()
        value = value.strip()
       
        if value.strip() == "":
            return
        if value in self._fit.global_param.keys():
            warn = "{} already defined.".format(value)
            err = QW.QMessageBox.warning(self, "warning", warn, QW.QMessageBox.Ok)
            return 

        # Remove link, if present
        try:
            self._fit.fitter.unlink_from_global(self._experiment,self._p.name)
        except KeyError:
            pass

        # Update fit
        self._fit.fitter.link_to_global(self._experiment,self._p.name,value)
        self._fit.emit_changed()

        self.close()
   
    def reject(self):
        """
        Update widgets with the rejection. (e.g. user hit "X" in top corner)
        """

        self._fit.emit_changed()
        super().reject() 
