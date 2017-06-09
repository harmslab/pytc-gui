__description__ = \
"""
Dialog for adding an experiment to a pytc fitting session.
"""
__author__ = "Hiranmayi Duvvuri"
__date__ = "2017-06-01"

import pytc

from PyQt5 import QtWidgets as QW

import inspect, re, collections, os

class AddExperiment(QW.QDialog):
    """
    Dialog for adding an experiment to a pytc fitting session.
    """

    def __init__(self, fit):

        super().__init__()

        subclasses = pytc.indiv_models.ITCModel.__subclasses__()
        self._models = {re.sub(r"(\w)([A-Z])", r"\1 \2", i.__name__): i for i in subclasses}

        self._exp_file = None
        self._fit = fit

        self.layout()

    def layout(self):
        """
        """
        # exp text, model dropdown, shots select
        main_layout = QW.QVBoxLayout(self)
        self._form_layout = QW.QFormLayout()
        self._button_layout = QW.QHBoxLayout()

        model_select = QW.QComboBox(self)
        model_names = list(self._models.keys())
        model_names.sort()
        try:
            model_names_index = model_names.index(self._fit.defaults["model"])
        except ValueError:
            model_names_index = 0

        for k in model_names:
            model_select.addItem(k)
        model_select.setCurrentIndex(model_names_index)

        # set up model select
        self._exp_model = self._models[str(model_select.currentText())]
        model_select.activated[str].connect(self.model_select)

        # set up load file
        load_exp = QW.QPushButton("Select file", self)
        load_exp.clicked.connect(self.add_file)

        self._exp_label = QW.QLabel("...", self)

        gen_exp = QW.QPushButton("OK", self)
        gen_exp.clicked.connect(self._ok_handler)

        # add to layout
        self._form_layout.addRow(load_exp, self._exp_label)
        self._form_layout.addRow(self._button_layout)

        # Experiment name
        self._enter_exp_label = QW.QLineEdit(self)
        self._form_layout.addRow(QW.QLabel("Label:", self),
                                 self._enter_exp_label)
        self._form_layout.addRow(QW.QLabel("Select Model:"), model_select)


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
            radio_button = QW.QRadioButton(type_name)
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
            units_default_index = units.index(self._fit.defaults["units"])
        except ValueError:
            units_default_index = 0

        units.sort()               

        # add exp args + defaults to widgets
        for n, v in args.items():

            if n == "units":
                self._exp_widgets[n] = QW.QComboBox(self)
                for u in units:
                    self._exp_widgets[n].addItem(u)
                units_default = self._exp_widgets[n].findText(self._fit.defaults["units"])
                self._exp_widgets[n].setCurrentIndex(units_default)
           
                # If a unit is already specified, disable the ability to set it
                # when other experiments are loaded 
                try:
                    required_units = self._fit.fit_units
                    req_index = self._exp_widgets[n].findText(required_units)
                    self._exp_widgets[n].setCurrentIndex(req_index)
                    self._exp_widgets[n].setDisabled(True)
                except AttributeError:
                    pass


            else:
                self._exp_widgets[n] = QW.QLineEdit(self)
                self._exp_widgets[n].setText(str(v))

        # sort dictionary
        sorted_names = collections.OrderedDict(sorted(self._exp_widgets.items()))

        # add to layout
        for name, entry in sorted_names.items():
            label_name = str(name).replace("_", " ") + ": "
            label = QW.QLabel(label_name.title(), self)

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
            self._gen_widgets[i] = QW.QLineEdit(self)
            self._gen_widgets[i].setText(str(args[i]))

        # add widgets to the pop-up box
        for name, entry in self._gen_widgets.items():
            label_name = str(name).replace("_", " ") + ": "
            label = QW.QLabel(label_name.title(), self)

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
            file_name = QW.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QW.QFileDialog.ShowDirsOnly)
        else:
            file_name, _ = QW.QFileDialog.getOpenFileName(self, "Select a file...", "", filter="DH Files (*.DH)")

        self._exp_file = str(file_name)
        self._exp_label.setText(os.path.relpath(self._exp_file))

        if self._enter_exp_label.text().strip() == "":
            exp_name = os.path.split(file_name)[-1]
            exp_name = ".".join(exp_name.split(".")[:-1])
            self._enter_exp_label.setText(exp_name)


    def _ok_handler(self):
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

            exp_label = self._enter_exp_label.text()
            self._fit.add_experiment(exp_label,self._exp_file,self._exp_model,**exp_param,**model_param)


            self.close()
        else:
            error_message = QW.QMessageBox.warning(self, "warning", "No heat file provided", QW.QMessageBox.Ok)
            
