__description__ = \
"""
Pretty table for fit parameters.
"""
__author__ = "Hiranmayi Duvvuri"
__date__ = "2017-06-03"

import PyQt5.QtWidgets as QW
from io import StringIO
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

           
        file_data = self._fit.fitter.fit_as_csv
        string_file = StringIO(file_data)

        # break up the file data
        for i in string_file:
            if i.startswith("#"):
                self._header.append(i.rstrip())
            elif i.startswith("type"):
                i = i.rstrip().split(',')
                self._col_name = i
            else:
                i = i.rstrip().split(',')
                self._data.append(i)

        for l in self._header:
            print(l)
        print("\n")

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
