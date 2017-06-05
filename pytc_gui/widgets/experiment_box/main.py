from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import seaborn

from .exp_frames import LocalBox, GlobalBox, ConnectorsBox

class ExperimentBox(QWidget):
    """
    Experiment box widget.  
    """

    fit_signal = pyqtSignal()

    def __init__(self, parent, fit):
        """
        """
        super().__init__()

        self._parent = parent
        self._fit = fit

        self._slider_list = {"Global" : {}, "Local" : {}}
        #self._global_connectors = {}
        #self._connectors_seen = {}
        self._plot_box = parent._plot_box
        self._update = parent.do_fit_callback

        self.layout()

    def layout(self):
        """
        Create layout.
        """

        # scroll box for experiments
        self._scroll = QScrollArea(self)
        self._exp_content = QWidget()
        self._exp_box = QVBoxLayout(self._exp_content)
        self._scroll.setWidget(self._exp_content)
        self._scroll.setWidgetResizable(True)
        self._exp_box.setAlignment(Qt.AlignTop)

        self._main_layout = QVBoxLayout(self)
        self._main_layout.addWidget(self._scroll)

    def update_exp(self):
        """
        Update fit and parameters, update experiments added to fitter
        """

        # check for instances of LocalBox and set any attributes
        for loc_obj in self._exp_box.findChildren(LocalBox):
            loc_obj.set_attr()

        if len(self._fit.experiments) != 0:

            # create local holder if doesn't exist
            for e in self._fit.experiments:
                if e in self._slider_list["Local"]:
                    continue

                self._slider_list["Local"][e] = []
                self._fit.connectors_seen[e] = []

                file_name = e.dh_file
                exp_name = file_name.split("/")[-1]

                exp = LocalBox(e, exp_name, self)
                self._exp_box.addWidget(exp)

    def clear(self):
        """
        for clearing the application
        """
        try:
            # check for any global/connector vars, remove them first
            for i in range(self._exp_box.count()): 
                widget = self._exp_box.itemAt(i).widget()
                if isinstance(widget, LocalBox):
                    continue

                widget.remove()

            # finally, remove local objects
            for loc_obj in self._exp_box.parentWidget().findChildren(LocalBox):
                self._fit.fitter.remove_experiment(loc_obj._exp)
                loc_obj.deleteLater()
        except:
            pass

        # reset all lists/dictionaries
        self._slider_list = {"Global" : {}, "Local" : {}}
        self._fit.connectors_seen = {}
        #self._global_connectors = {}

