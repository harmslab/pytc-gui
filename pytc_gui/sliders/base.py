from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc
import inspect, math

class Sliders(QWidget):
    """
    create sliders for an experiment
    """

    def __init__(self, param_name, parent):
        super().__init__()

        self._exp = parent._exp
        self._param_name = param_name
        self._fitter = parent._fitter
        self._fit_run = False
        self._main_box = parent._main_box
        self._plot_frame = parent._plot_frame

        self.layout()

    @property
    def name(self):
        """
        """
        return self._param_name

    def layout(self):
        """
        """
        self._main_layout = QGridLayout(self)
        self._main_layout.setVerticalSpacing(40)

        self._name_label = QLabel(self._param_name, self)
        self._main_layout.addWidget(self._name_label, 0, 0, 0, 2)

        self._fix = QCheckBox("Fix?", self)
        self._fix.toggle()
        self._fix.setChecked(False)
        self._fix.stateChanged.connect(self.fix_layout)
        self._main_layout.addWidget(self._fix, 1, 0)

        self._slider = QSlider(Qt.Horizontal)
        self._slider.sliderReleased.connect(self.update_val)
        self._main_layout.addWidget(self._slider, 1, 1)
        self._slider.setMinimumWidth(100)

        self._param_guess_label = QLabel("", self)
        self._main_layout.addWidget(self._param_guess_label, 1, 2)

        self.bounds()

        self._fix_int = QLineEdit(self)
        self._main_layout.addWidget(self._fix_int, 1, 3)
        self._fix_int.setText(str(1))
        self._fix_int.returnPressed.connect(self.fix)
        self._fix_int.hide()

        self._update_min_label = QLabel("min: ", self)
        self._main_layout.addWidget(self._update_min_label, 1, 4)

        self._update_min = QLineEdit(self)
        self._main_layout.addWidget(self._update_min, 1, 5)
        self._update_min.returnPressed.connect(self.min_bounds)
        self._update_min.setFixedWidth(60)

        self._update_max_label = QLabel("max: ", self)
        self._main_layout.addWidget(self._update_max_label, 1, 6)

        self._update_max = QLineEdit(self)
        self._main_layout.addWidget(self._update_max, 1, 7)
        self._update_max.returnPressed.connect(self.max_bounds)
        self._update_max.setFixedWidth(60)

    @pyqtSlot()
    def set_fit_true(self):
        """
        """
        self._fit_run = True

    def check_if_fit(self):
        """
        if a fit has been run, and a slider is changed, change all parameters back to guesses in slider widgets
        """
        if self._fit_run:
            self._fitter.guess_to_value()
            self._fit_run = False

        self._plot_frame.update()

    def fix_layout(self, state):
        """
        initial parameter fix and updating whether slider/fixed int is hidden or shown
        """
        if state == Qt.Checked:
            # change widget views
            self._fix_int.show()
            self._slider.hide()
            self._param_guess_label.hide()
            self._fitter.update_fixed(self._param_name, int(self._fix_int.text()), self._exp)
            self.check_if_fit()
        else:
            #change widget views
            self._fix_int.hide()
            self._slider.show()
            self._param_guess_label.show()

            self._fitter.update_fixed(self._param_name, None, self._exp)

    def fix(self):
        """
        update fixed value when enter/return key pressed
        """
        try:
            self._fitter.update_fixed(self._param_name, int(self._fix_int.text()), self._exp)
            self.check_if_fit()
        except:
            pass

    def update_val(self):
        """
        update value for parameter based on slider value
        """

        value = int(self._slider.value())

        # transform values back
        if self._range_diff < 10:
            value /= 10
        elif self._range_diff < 100000:
            value *= 100
        elif self._range_diff < 100000000:
            value = 10 ** value

        if value != 0:
            # if guess update, update parameter as well for plot
            self._fitter.update_guess(self._param_name, value, self._exp)
            self._fitter.update_value(self._param_name, value, self._exp)
            self._param_guess_label.setText(str(value))
        else:
            pass

        self.check_if_fit()

    def transform_init(self, val):
        """
        transform values for use in slider
        """
        if self._range_diff < 10:
            new_val = val * 10
        elif self._range_diff < 100000:
            new_val = val / 100
        elif self._range_diff < 100000000:
            new_val = math.log10(val)

        return new_val

    def min_bounds(self):
        """
        update the minimum bounds when enter/return key pressed
        """
        try:
            self._min = int(self._update_min.text())

            # make sure K min bound isn't negative
            if "K" in self._param_name and self._min < 0:
                self._min = 1

            # set new range
            self._range_diff = self._max - self._min

            # if range has significantly changed, update value transformations
            self._slider_max = self.transform_init(self._max)
            self._slider_min = self.transform_init(self._min)

            # set slider min
            self._slider.setMinimum(self._slider_min)
            self.update_bounds()
        except:
            pass

    def max_bounds(self):
        """
        update maximum bounds when enter/return key pressed
        """
        try:
            self._max = int(self._update_max.text())

            # set new range
            self._range_diff = self._max - self._min

            # if range has significantly changed, update the value transformations
            self._slider_max = self.transform_init(self._max)
            self._slider_min = self.transform_init(self._min)

            # set slider max
            self._slider.setMaximum(self._slider_max)
            self.update_bounds()
        except:
            pass

    def bounds(self):
        """
        for anything specific to child class
        """
        # transform values based on parameter to allow floats to pass to fitter and 
        # make sliders easier to use, QtSlider only allows integers
        self._range_diff = self._max - self._min

        min_range = self.transform_init(self._min)
        max_range = self.transform_init(self._max)

        self._slider.setMinimum(min_range)
        self._slider.setMaximum(max_range)

    def update_bounds(self):
        """
        update min/max bounds and check if range needs to be updated as well
        """
        pass
