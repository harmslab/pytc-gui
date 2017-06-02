import pytc
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import inspect, re, collections

DEFAULT_UNITS = "cal/mol"
DEFAULT_MODEL = "Single Site"

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
        self._button_layout = QHBoxLayout()

        model_select = QComboBox(self)
        model_names = list(self._models.keys())
        model_names.sort()
        try:
            model_names_index = model_names.index(DEFAULT_MODEL)
        except ValueError:
            model_names_index = 0

        for k in model_names:
            model_select.addItem(k)
        model_select.setCurrentIndex(model_names_index)

        # set up model select
        self._exp_model = self._models[str(model_select.currentText())]
        model_select.activated[str].connect(self.model_select)

        # set up load file
        load_exp = QPushButton("Load File", self)
        load_exp.clicked.connect(self.add_file)

        self._exp_label = QLabel("...", self)

        gen_exp = QPushButton("OK", self)
        gen_exp.clicked.connect(self.generate)

        # add to layout
        self._form_layout.addRow(load_exp, self._exp_label)
        self._form_layout.addRow(self._button_layout)
        self._form_layout.addRow(QLabel("Select Model:"), model_select)

        self._load_exp_info()

        # keeps load_exp from being default button for return press
        load_exp.setDefault(False)
        load_exp.setAutoDefault(False)

        self._update_widgets()

        main_layout.addLayout(self._form_layout)
        main_layout.addWidget(gen_exp)

        self.setWindowTitle('Add Experiment to Fitter')

    def _load_exp_info(self):
        """
        """
        self._gen_widgets = {}
        self._exp_widgets = {}

        self._radio_buttons = []

        # get file types/choosers
        file_types = []
        for name, obj in inspect.getmembers(pytc.experiments):
            if inspect.isclass(obj):
                file_types.append((name,obj))
        file_types.sort()

        # make radio buttons + add to layout
        for name, obj in file_types:
            type_name = name.replace("Experiment", "")
            radio_button = QRadioButton(type_name)
            radio_button.toggled.connect(self.select_file_type)
            self._button_layout.addWidget(radio_button)
            self._radio_buttons.append(radio_button)
            if "Origin" in type_name:
                radio_button.setChecked(True)

        exp_def = inspect.getargspec(pytc.experiments.base.BaseITCExperiment)

        args = {arg: param for arg, param in zip(exp_def.args[3:], exp_def.defaults)}

        # get units 
        units = getattr(pytc.experiments.base.BaseITCExperiment, 'AVAIL_UNITS')
        units = list(units.keys())
        try:
            units_default_index = units.index(DEFAULT_UNITS)
        except ValueError:
            units_default_index = 0

        units.sort()               

        # add exp args + defaults to widgets
        for n, v in args.items():
            if n == "units":
                self._exp_widgets[n] = QComboBox(self)
                for u in units:
                    self._exp_widgets[n].addItem(u)
                self._exp_widgets[n].setCurrentIndex(units_default_index)
            else:
                self._exp_widgets[n] = QLineEdit(self)
                self._exp_widgets[n].setText(str(v))

        # sort dictionary
        sorted_names = collections.OrderedDict(sorted(self._exp_widgets.items()))

        # add to layout
        for name, entry in sorted_names.items():
            label_name = str(name).replace("_", " ") + ": "
            label = QLabel(label_name.title(), self)

            self._form_layout.addRow(label, entry)

    def _update_widgets(self):
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
        self._update_widgets()

    def select_file_type(self):
        """
        """
        b = self.sender()

        # change type of file dialog based on radio option
        if b.isChecked():
            self._file_type = b.text()

    def add_file(self):
        """
        """
        # do folder or file radio options
        if self._file_type == "Nitpic":
            file_name = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        else:
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

            exp_param = {}
            for k, v in self._exp_widgets.items():
                val = None
                if k != "units":
                    if "." in v.text():
                        val = float(v.text())
                    elif v.text().isdigit():
                        val = int(v.text())
                    else:
                        val = v.text()
                else:
                    val = v.currentText()

                exp_param[k] = val

            itc_exp = pytc.ITCExperiment(self._exp_file, self._exp_model, **exp_param, **model_param)
            self._fitter.add_experiment(itc_exp)

            self._on_close._plot_box.update()
            self._on_close._exp_box.update_exp()

            self.close()
        else:
            error_message = QMessageBox.warning(self, "warning", "No .DH file provided", QMessageBox.Ok)
            
