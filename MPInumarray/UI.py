import sys
import numpy as np
import random
import pandas as pd

#PyQt5 UI stuff. Widjets, midjets etc.
from PyQt5.QtWidgets import QAction, QLineEdit, QMessageBox, QApplication, QWidget, QPushButton, QSizePolicy, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator
from PyQt5.QtCore import pyqtSlot

#matplot libraries need to do plotting stuff
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#project modules used in this one
import shell

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout'
        self.left = 400
        self.top = 200
        self.width = 800
        self.height = 600
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
        # Grid layout is pretty useful.
        # It allows to scale every window item with the window itself.
        self.horizontalGroupBox = QGroupBox("Grid")
        self.globalLayout = QGridLayout()
        # !!!! DO NOT CHANGE setColumStretch without purpose. Or size proportions of plots and textboxes will broke!
        self.globalLayout.setColumnStretch(1, 4)
        self.figure = []
        self.gRowIndex = 0

        self.firstGroupBox = QGroupBox("First")
        self.globalLayout.addWidget(self.firstGroupBox, self.gRowIndex, 0)
        self.figure.append(PlotCanvas(self, model=shell.computeSystemOCL, width=5, height=4))
        self.globalLayout.addWidget(self.figure[self.gRowIndex], self.gRowIndex, 1)

        localLayout = createLocalLayout(("osc_min", "osc_max", "osc_step"), "evaluate", num=self.gRowIndex, figure=self.figure, globalLayout=self.globalLayout)
        self.firstGroupBox.setLayout(localLayout.localLayout)

        self.gRowIndex += 1
        self.firstGroupBox = QGroupBox("Second")
        self.globalLayout.addWidget(self.firstGroupBox, self.gRowIndex, 0)
        self.figure.append(PlotCanvas(self, model=shell.computeRLSystemOCL, width=5, height=4))
        self.globalLayout.addWidget(self.figure[self.gRowIndex] , self.gRowIndex, 1)

        localLayout = createLocalLayout(("lmb_min", "lmb_max", "lmb_step", "oscillators_number"), "evaluate", num=self.gRowIndex, figure=self.figure, globalLayout=self.globalLayout)
        self.firstGroupBox.setLayout(localLayout.localLayout)

        self.gRowIndex += 1
        self.firstGroupBox = QGroupBox("Third")
        self.globalLayout.addWidget(self.firstGroupBox, self.gRowIndex, 0)
        self.figure.append(PlotCanvas(self, model=shell.KAnalis, width=5, height=4))
        self.globalLayout.addWidget(self.figure[self.gRowIndex], self.gRowIndex, 1)

        localLayout = createLocalLayout(("lambd", "oscillators_number", "topology"), "evaluate", num=self.gRowIndex, figure=self.figure, globalLayout=self.globalLayout)
        self.firstGroupBox.setLayout(localLayout.localLayout)

        self.horizontalGroupBox.setLayout(self.globalLayout)

class createLocalLayout():
    def __init__(self, args, evaluate, num, figure, globalLayout):

        self.localLayout = QGridLayout()
        self.figure = figure
        self.globalLayout = globalLayout

        i = 0
        self.textboxList = {}
        for string in args:     # so many labels, so many textboxes
            self.textboxList[string] = QLineEdit()
            #self.textboxList[string].setValidator(QDoubleValidator()) #DON'T allow type "." charackter. Work wrong!
            self.localLayout.addWidget(self.textboxList[string], i, 0)
            self.localLayout.addWidget(QLabel(string), i, 1)
            i += 1

        self.evButton = QPushButton(evaluate)
        self.localLayout.addWidget(self.evButton, i, 1)

        # connect button to function on_click. To make it clickable.
        self.evButton.clicked.connect(lambda: self.on_click(num))



    @pyqtSlot()
    def on_click(self, num):
        textboxValue = {}
        for key in self.textboxList.keys() :
            text = self.textboxList[key].text()
            text = text.replace(",", ".")
            try:
                if np.mod(np.float(text), 1) == 0:
                    textboxValue[key] = np.int(text)
                else:
                    textboxValue[key] = np.float(text)
            except:
                textboxValue[key] = text


        figure = self.figure[num].plot(**textboxValue)
        self.globalLayout.addWidget(figure, 0, 1)



class PlotCanvas(FigureCanvas):
    #we need to create plot object. To Do that, we use FigureCanvas-like class.
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
        # is plot function, that plot a plot, then you call the plot()
        ax = self.figure.add_subplot(111)
        ax.cla()
        output_array = self.model(**kwargs)

        #we need to plot lambda and usual graphics by the same plot() method
        if type(output_array) is tuple:
            ax.plot(*output_array)
        else:
            ln = len(output_array[0])
            for pendulum in output_array:
                ax.plot(np.linspace(0, ln, ln), pendulum)

        ax.set_title('PyQt Matplotlib Example')
        self.draw()


def initUI():
    # one additional layer to compact __main__
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == '__main__':
    initUI()
    ...



    #TODO make textboxes usefull

    # TODO make new coments after all