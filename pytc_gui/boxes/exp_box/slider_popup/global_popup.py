from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc
import inspect

from .. import sliders
from .base import SliderPopUp

class GlobalPopUp(SliderPopUp):
    """
    pop-up window for slider widgets
    """

    def __init__(self, parent):
        """
        """
        super().__init__(parent)

    def populate(self):
        """
        """
        sliders = self._slider_list["Global"][self._name]

        # add sliders to layout
        self._main_layout.addWidget(sliders)