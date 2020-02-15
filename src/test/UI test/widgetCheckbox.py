from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import *
from PyQt5.QtCore import *


class Window(QtWidgets.QWidget):
    def __int__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )


        # def sizeHint(self):
        #     return QtCore.QSize(40, 120)

