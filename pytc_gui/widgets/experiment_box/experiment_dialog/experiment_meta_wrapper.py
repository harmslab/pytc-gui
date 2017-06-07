__description__ = \
"""
Create GUI elements wrapping a single piece of fit meta data.
"""
__author__ = "Michael J. Harms"
__date__ = "2017-06-01"

from PyQt5 import QtWidgets as QW
from PyQt5 import QtCore as QC

class ExperimentMetaWrapper(QW.QWidget):
    """
    This class wraps a single piece of fit meta data with a gui.
    """

    def __init__(self,parent,fit,experiment,meta_name,float_view_cutoff=100000.):
        """
        Initialize the class.

        parent: parent widget
        fit: FitContainer object
        experiment: pytc.ITCExperiment instance
        meta_name: name of meta data (string)
        float_view_cutoff: how to show floats in QLineEdit boxes
        """

        super().__init__()

        self._parent = parent
        self._fit = fit
        self._experiment = experiment
        self._meta_name = meta_name
        self._float_view_cutoff = float_view_cutoff       

        self._fit.fit_changed_signal.connect(self.fit_has_changed_slot)

        self.layout()


    def layout(self):
        """
        Create layout.
        """

        self._main_layout = QW.QHBoxLayout(self)

        self._label = QW.QLabel(self._meta_name)
        self._meta = QW.QLineEdit()
        self._meta.textChanged.connect(self._meta_handler)
        self._meta.editingFinished.connect(self._meta_handler)
   
        self._main_layout.addWidget(self._label)
        self._main_layout.addWidget(self._meta)

        # Load in parameters from FitParameter object
        self.update()
        

    def _meta_check_handler(self):
        """
        Handle meta entries.  Turn pink of the value is bad.  
        """

        success = True 
        try:
            value = float(self._meta.text())
            setattr(self._experiment,self._meta_name,value)
            color = "#FFFFFF"
        except ValueError:
            color = "#FFB6C1"

        self._guess.setStyleSheet("QLineEdit {{ background-color: {} }}".format(color))

    @QC.pyqtSlot(bool)
    def fit_has_changed_slot(self):
        self.update()

    def update(self):
        """
        Update the widgets.
        """

        # Pause updates while all of these widgets update
        self._fit.pause_updates(True)

        value = getattr(self._experiment,self._meta_name)
        if value < 1/self._float_view_cutoff or value > self._float_view_cutoff:
            value_str = "{:.8e}".format(value)
        else:
            value_str = "{:.8f}".format(value)
        self._guess.setText(value_str)

