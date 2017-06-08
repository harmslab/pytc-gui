__description__ = \
"""
Pretty table for fit parameters.
"""
__author__ = "Hiranmayi Duvvuri"
__date__ = "2017-06-03"

import PyQt5.QtWidgets as QW
import PyQt5.QtCore as QC
#from io import StringIO
import seaborn

class ParameterBox(QW.QTableWidget):
    """
    Take csv style param string and put into table widget
    """

    def __init__(self,parent,fit):

        super().__init__()

        self._parent = parent
        self._fit = fit

        self._header = []
        self._col_name = []
        self._data = []

        self._fit.fit_changed_signal.connect(self.fit_has_changed_slot)

        self.layout()

    def layout(self):
        """
        Create table layout.
        """

        self.setAlternatingRowColors(True)

    def _csv_to_table(self):
        """
        convert csv data file to lists to be read by qtablewidget
        """

        self._header = []
        self._col_name = []
        self._data = []

        string_file = self._fit.fitter.fit_as_csv
        #string_file = StringIO(file_data)

        # break up the file data
        for i in string_file.split("\n"):
            if i.startswith("#"):
                self._header.append(i.rstrip())
            elif i.startswith("type"):
                i = i.rstrip().split(',')
                self._col_name = i
            else:
                i = i.rstrip().split(',')
                self._data.append(i)

        self._fit.event_logger.emit("Fit stats:","normal")
        for l in self._header:
            self._fit.event_logger.emit(l[1:].strip(),"normal")

    def update(self):
        """
        update the table with updated fit parameters
        """
    
        # If the fit is not done, clear the parameters
        if not self._fit.fitter.fit_success or len(self._fit.experiments) == 0:
            self.clear()
            return

        # Grab fit results from csv
        self._csv_to_table()

        self.setRowCount(len(self._data))
        self.setColumnCount(len(self._data[0]))
        self.setHorizontalHeaderLabels(self._col_name)

        # load fit data into the table
        for i, row in enumerate(self._data):
            for j, col in enumerate(row):
                item = QW.QTableWidgetItem(col)
                self.setItem(i, j, item)

    def clear(self):
        """
        Clear the widget
        """
        super().clear()
        self._header = []
        self._col_name = []
        self._data = []
        self.layout()

    @QC.pyqtSlot(bool)
    def fit_has_changed_slot(self,val):
        """
        Slot that looks for emission from FitContainer saying that it changed
        in some way.
        """

        # Update all of the widgets
        self.update()
