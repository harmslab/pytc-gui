from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .exp_frames import LocalBox

class AddExpWorker(QObject):
    """
    create threads for experiment/fit updates
    """
    finished = pyqtSignal()
    loc_signal = pyqtSignal([list])
    #fit_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__()

        self._experiments = parent._experiments
        self._slider_list = parent._slider_list
        self._connectors_seen = parent._connectors_seen
        self._loc_parent = parent
        self._exp_box = parent._exp_box

    @pyqtSlot()
    def loop_creation(self):

        for e in self._experiments:
            if e in self._slider_list["Local"]:
                continue

            self._slider_list["Local"][e] = []
            self._connectors_seen[e] = []

            file_name = e.dh_file
            exp_name = file_name.split("/")[-1]
            
            self.loc_signal.emit([e, exp_name])

        self.finished.emit()

    def set_attr(self):

        for loc_obj in self._exp_box.parentWidget().findChildren(LocalBox):
            loc_obj.set_attr()

        for exp_obj in range(self._exp_box.count()): 
            self._exp_box.itemAt(exp_obj).widget().set_fit_true()
