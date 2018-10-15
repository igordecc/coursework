import sys

from PyQt5.QtWidgets import QAction, QLineEdit, QMessageBox, QApplication, QWidget, QPushButton, QSizePolicy, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator
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

        # m.move(0, 0)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        globalLayout = QGridLayout()
        # !!!! DO NOT CHANGE setColumStretch without purpose
        globalLayout.setColumnStretch(1, 4)

        # --- first plot
        self.firstGroupBox = QGroupBox("A-HA! First")
        globalLayout.addWidget(self.firstGroupBox, 0, 0)

        globalLayout.addWidget(PlotCanvas(self, width=5, height=4), 0, 1)

        localLayout = self.createLocalLayout(("lambda", "K", "x"), "evaluate")
        self.firstGroupBox.setLayout(localLayout)

        # --- end
        self.horizontalGroupBox.setLayout(globalLayout)

    def createLocalLayout(self, args, evaluate):
        """
        For fast creating Local Layout
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
        self.evButton.clicked.connect(self.on_click)

        return localLayout

    @pyqtSlot()
    def on_click(self):

        textboxValue = self.textboxList[0].text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textboxList[0].setText("")

        import shell
        shell.computeSystemOCL(osc_min=1000, osc_max=1001, osc_step=20)


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


def initUI():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == '__main__':
    initUI()

    import shell
    shell.computeSdystemOCL(osc_min=1000, osc_max=1001, osc_step=20)


    # TODO import shell.py  functions in UI.py. Run them, if button clicked.