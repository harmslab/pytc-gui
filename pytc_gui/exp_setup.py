import pytc
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import inspect
import re

class AddExperimentWindow(QDialog):
    """
    add experiment pop-up box
    """

    def __init__(self, fitter, on_close):

        super().__init__()

        subclasses = pytc.indiv_models.ITCModel.__subclasses__()
        self._models = {re.sub(r"(\w)([A-Z])", r"\1 \2", i.__name__): i for i in subclasses}

        self._exp_file = None
        self._shot_start = 1
        self._fitter = fitter

        self._on_close = on_close

        self.layout()

    def layout(self):
        """
        """
        # exp text, model dropdown, shots select
        main_layout = QVBoxLayout(self)
        self._form_layout = QFormLayout()

        self._gen_widgets = {}

        model_select = QComboBox(self)
        model_names = list(self._models.keys())
        model_names.sort()

        for k in model_names:
            model_select.addItem(k)

        self._exp_model = self._models[str(model_select.currentText())]
        model_select.activated[str].connect(self.model_select)

        load_exp = QPushButton("Load File", self)
        load_exp.clicked.connect(self.add_file)

        self._exp_label = QLabel("...", self)

        shot_start_text = QLineEdit(self)
        shot_start_text.setText("0")
        shot_start_text.textChanged[str].connect(self.shot_select)

        gen_exp = QPushButton("OK", self)
        gen_exp.clicked.connect(self.generate)

        self._form_layout.addRow(load_exp, self._exp_label)
        self._form_layout.addRow(QLabel("Select Model:"), model_select)
        self._form_layout.addRow(QLabel("Shot Start:"), shot_start_text)

        # keeps load_exp from being default button for return press
        load_exp.setDefault(False)
        load_exp.setAutoDefault(False)

        self.update_widgets()

        main_layout.addLayout(self._form_layout)
        main_layout.addWidget(gen_exp)

        self.setWindowTitle('Add Experiment to Fitter')

    def update_widgets(self):
        """
        """
        # check for any model specific parameters and update text fields with those values
        for l in self._gen_widgets.values():
            widget_labeled = self._form_layout.labelForField(l)
            if widget_labeled is not None:
                widget_labeled.deleteLater()
            l.deleteLater()

        self.adjustSize()
        self._gen_widgets = {}

        parent_req = pytc.indiv_models.ITCModel()

        sig_parent = inspect.getargspec(parent_req.__init__)
        sig_child = inspect.getargspec(self._exp_model.__init__)

        args = {arg: param for arg, param in zip(sig_child.args[1:], sig_child.defaults)}

        unique = list(set(sig_child.args) - set(sig_parent.args))

        for i in unique:
            self._gen_widgets[i] = QLineEdit(self)
            self._gen_widgets[i].setText(str(args[i]))

        # add widgets to the pop-up box
        for name, entry in self._gen_widgets.items():
            label_name = str(name).replace("_", " ") + ": "
            label = QLabel(label_name.title(), self)

            self._form_layout.addRow(label, entry)

    def model_select(self, model):
        """
        """
        self._exp_model = self._models[model]
        self.update_widgets()

    def shot_select(self, shot):
        """
        """
        try:
            self._shot_start = int(shot)
        except:
            pass

    def add_file(self):
        """
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a file...", "", filter="DH Files (*.DH)")
        self._exp_file = str(file_name)
        self._exp_name = file_name.split("/")[-1]
        self._exp_label.setText(self._exp_name)

    def generate(self):
        """
        """
        if self._exp_file != None:

            # set up dictionary for paramter names and their values in float or int
            model_param = {}
            for k, v in self._gen_widgets.items():
                val = None
                if "." in v.text():
                    val = float(v.text())
                else:
                    val = int(v.text())

                model_param[k] = val

            itc_exp = pytc.ITCExperiment(self._exp_file, self._exp_model, shot_start = self._shot_start, **model_param)
            self._fitter.add_experiment(itc_exp)

            self._on_close._plot_frame.update()
            self._on_close._exp_frame.add_exp()
            self.close()
        else:
            error_message = QMessageBox.warning(self, "warning", "No .DH file provided", QMessageBox.Ok)
            
