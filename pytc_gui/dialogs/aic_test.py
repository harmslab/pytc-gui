__description__ = \
"""
AIC test dialog for pytc-gui.
"""
__author__ = "Hiranmayi Duvvuri"
__date__ = "2017-06-01"

from pytc import util

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets as QW

import copy, re

class AICTest(QW.QDialog):
    """
    AIC test dialog for pytc-gui.
    """

    def __init__(self, parent, fit):
        """
        Initialize class.
        """
        super().__init__()

        self._parent = parent
        self._fit = fit

        self._fit_snapshot_dict = {}

        self.layout()

    def layout(self):
        """
        Lay out the dialog.
        """

        main_layout = QW.QVBoxLayout(self)
        test_layout = QW.QHBoxLayout()
        button_layout = QW.QVBoxLayout()

        self._fitter_select = QW.QListWidget()
        self._fitter_select.setSelectionMode(QW.QAbstractItemView.ExtendedSelection)

        for k,v in self._fit_snapshot_dict.items():
            self._fitter_select.addItem(k)

        self._fitter_select.setFixedSize(150, 100)

        ftest_button = QW.QPushButton("Perform AIC Test", self)
        ftest_button.clicked.connect(self.perform_test)

        add_fit_button = QW.QPushButton("Append New Fit", self)
        add_fit_button.clicked.connect(self.add_fitter)

        self._data_out = QW.QTextEdit()
        self._data_out.setReadOnly(True)
        self._data_out.setMinimumWidth(400)

        # add buttons to layout
        button_layout.addWidget(ftest_button)
        button_layout.addWidget(add_fit_button)

        # add widgets to layout
        test_layout.addWidget(self._fitter_select)
        test_layout.addLayout(button_layout)
        main_layout.addLayout(test_layout)
        main_layout.addWidget(self._data_out)

        self.setWindowTitle('AIC Test')

    def add_fitter(self):
        """
        Add current fitter to list for testing
        """
        text, ok = QW.QInputDialog.getText(self, 'Save Fitter', 'Enter Name:')

        # save deepcopy of fitter
        if ok:
            self._fit_snapshot_dict[text] = copy.deepcopy(self._fit.fitter)
            self._fitter_select.addItem(text)
            self._fit.event_logger.emit("Fitter {} saved to list.".format(text),"info")

    def perform_test(self):
        """
        Take selected objects and use them in AIC test.
        """

        selected_names = [i.text() for i in self._fitter_select.selectedItems()] 
        selected = [self._fit_snapshot_dict[n] for n in selected_names]

        if len(selected) < 2:
            err = "You must select at least two fits to compare.\n"
            QW.QMessageBox.warning(self, "warning", err, QW.QMessageBox.Ok)
            return 

        output, plots = util.compare_models(*selected)

        test = []
        best_model = []
        weights = []
        for o, v in output.items():
            test.append(o)
            best_model.append(v[0])
            weights.append(v[1]) 

        # Figure out if there is a best model by consensus
        best_overall = [(best_model.count(a),a) for a in set(best_model)] 
        best_overall.sort(reverse=True)

        # If one guy one all the time or the best model is found better more times,
        # it's the best
        if len(best_overall) == 1 or best_overall[0][0] > best_overall[1][0]:
            final_best = best_overall[0][1]
        else:
            final_best = -1

        # Write out header
        s_head = "<span style=\"font-family:courier; font-weight:bold\">{}</span>"

        tmp = "{:10s}".format("fit")
        tmp = re.sub(" ","&#160;",tmp)
        line = [s_head.format(tmp)] 
        for j in range(len(test)):
            tmp = "{:7s}".format(test[j])
            tmp = re.sub(" ","&#160;",tmp)
            line.append(s_head.format(tmp)) 

        out = "".join(line)
        self._data_out.insertHtml(out)
        self._data_out.insertPlainText("\n") 
        self._data_out.verticalScrollBar().setValue(self._data_out.verticalScrollBar().maximum())

        # Write out result
        s = "<span style=\"font-family:courier;\">{}</span>"
        s_bold = "<span style=\"font-family:courier; font-weight:bold; color:blue\">{}</span>"

        for i in range(len(selected)):
            tmp = "{:10s}".format(selected_names[i])
            tmp = re.sub(" ","&#160;",tmp)
            if i == final_best:
                line = [s_bold.format(tmp)]
            else:
                line = [s.format(tmp)]
            for j in range(len(test)):
                tmp = "{:7.3f}".format(weights[j][i])
                tmp = re.sub(" ","&#160;",tmp)

                if best_model[j] == i:
                    line.append(s_bold.format(tmp))
                else:
                    line.append(s.format(tmp))

            out = "".join(line)
           
            self._data_out.insertHtml(out)
            self._data_out.insertPlainText("\n") 
            self._data_out.verticalScrollBar().setValue(self._data_out.verticalScrollBar().maximum())

