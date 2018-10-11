import sys

from PyQt5.QtWidgets import QAction, QLineEdit, QMessageBox, QApplication, QWidget, QPushButton, QSizePolicy, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)


        #m.move(0, 0)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        globalLayout = QGridLayout()
        #!!!! DO NOT CHANGE setColumStretch without purpose
        #globalLayout.setColumnStretch(0, 4)
        globalLayout.setColumnStretch(1, 4)
        #========
        #globalLayout.setSizeConstraint(10)



        #--- first plot
        self.firstGroupBox = QGroupBox("A-HA! First")
        globalLayout.addWidget(self.firstGroupBox, 0, 0)
        globalLayout.addWidget(PlotCanvas(self, width=5, height=4), 0, 1)
        localLayout = QGridLayout()
        
        localLayout.addWidget(QLineEdit(self), 0, 0)
        localLayout.addWidget(QPushButton('1'), 0, 1)

        self.firstGroupBox.setLayout(localLayout)

        # globalLayout.addWidget(QPushButton('4'), 1, 0)
        # globalLayout.addWidget(QPushButton('5'), 1, 1)
        # globalLayout.addWidget(QPushButton('7'), 2, 0)
        self.horizontalGroupBox.setLayout(globalLayout)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())