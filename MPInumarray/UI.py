import sys

from PyQt5.QtWidgets import QAction, QLineEdit, QMessageBox, QApplication, QWidget, QPushButton, QSizePolicy, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

import shell
import numpy as np

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

        # m.move(0, 0)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        self.globalLayout = QGridLayout()
        # !!!! DO NOT CHANGE setColumStretch without purpose
        self.globalLayout.setColumnStretch(1, 4)
        self.figure = []

        self.firstGroupBox = QGroupBox("A-HA! First")
        self.globalLayout.addWidget(self.firstGroupBox, 0, 0)
        self.figure.append(PlotCanvas(self, model=shell.computeSystemOCL, width=5, height=4))
        self.globalLayout.addWidget(self.figure[0], 0, 1)

        localLayout = self.createLocalLayout(("lambda", "K", "x"), "evaluate", num=0)
        self.firstGroupBox.setLayout(localLayout)



        self.firstGroupBox = QGroupBox("Wait a second")
        self.globalLayout.addWidget(self.firstGroupBox, 1, 0)

        self.figure.append(PlotCanvas(self, model=shell.computeRLSystemOCL, width=5, height=4))
        #self.globalLayout.addWidget(figure, 1, 1)
        self.globalLayout.addWidget(self.figure[1] , 1, 1)

        localLayout = self.createLocalLayout(("Lambda min", "Lambda max", "dLambda"), "evaluate", num=1)
        self.firstGroupBox.setLayout(localLayout)

        self.horizontalGroupBox.setLayout(self.globalLayout)

    def createLocalLayout(self, args, evaluate, num):
        """
        For fast creating Local Layout
        :param num:
        :param args: TEXT TUPLE
        :return: localLayout
        """

        localLayout = QGridLayout()

        i = 0
        self.textboxList = []
        for string in args:
            self.textboxList.append(QLineEdit(self))
            self.textboxList[i].setValidator(QDoubleValidator())
            localLayout.addWidget(self.textboxList[i], i, 0)
            localLayout.addWidget(QLabel(string), i, 1)
            i += 1
        self.evButton = QPushButton(evaluate)
        localLayout.addWidget(self.evButton, i, 1)

        # connect button to function on_click. To make it clickable.
        self.evButton.clicked.connect(lambda: self.on_click(num))

        return localLayout

    @pyqtSlot()
    def on_click(self, num):
        figure = self.figure[num].plot()
        self.globalLayout.addWidget(figure, 0, 1)
        textboxValue = self.textboxList[0].text()
        self.textboxList[0].setText("")



class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, model=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.model = model
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self, **kwargs):
        ax = self.figure.add_subplot(111)
        ax.cla()
        output_array = self.model(**kwargs)


        print("len(output_array) "+str(len(output_array)))
        print("shape " + str(output_array.shape))
        print("shape len " + str(len(output_array.shape)))

        if len(output_array.shape) == 1:
            ln = len(output_array)
            ax.plot(np.linspace(0, ln, ln), output_array)
        else:
            ln = len(output_array[0])
            for pendulum in output_array:
                ax.plot(np.linspace(0, ln, ln), pendulum)

        ax.set_title('PyQt Matplotlib Example')
        self.draw()


def initUI():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == '__main__':
    initUI()
    ...





    # TODO import shell.py  functions in UI.py. Run them, if button clicked.