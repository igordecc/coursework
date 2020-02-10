# TODO plot lables
# TODO plot grid
import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
# PyQt5 UI stuff. Widjets, midjets etc.
from PyQt5.QtWidgets import QLineEdit, QApplication, QPushButton, QSizePolicy, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel

# matplot libraries need to do plotting stuff
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# project modules used in this one
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
        print("INIT UI!")
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        # m.move(0, 0)
        print("INIT UI!")
        self.show()
        print("INIT UI!")

    def createGridLayout(self):
        # Grid layout is pretty useful.
        # It allows to scale every window item with the window itself.
        self.horizontalGroupBox = QGroupBox("Grid")
        self.globalLayout = QGridLayout()
        # !!!! DO NOT CHANGE setColumStretch without purpose. Or size proportions of plots and textboxes will broke!
        self.globalLayout.setColumnStretch(1, 4)
        self.figure = []
        self.gRowIndex = 0

        self.oscGroupBox = QGroupBox("oscillators")
        self.globalLayout.addWidget(self.oscGroupBox, self.gRowIndex, 0)
        model = shell.compute_system_ocl
        self.figure.append(PlotCanvas(self, model=model, width=5, height=4))
        self.globalLayout.addWidget(self.figure[self.gRowIndex], self.gRowIndex, 1)

        localLayout = LocalLayout(("osc_min", "osc_max", "osc_step"), "evaluate", num=self.gRowIndex, figure=self.figure, globalLayout=self.globalLayout, default_values=model.__defaults__)
        self.oscGroupBox.setLayout(localLayout.localLayout)

        self.gRowIndex += 1
        self.rFromLambdaGroupBox = QGroupBox("r from lambda")
        self.globalLayout.addWidget(self.rFromLambdaGroupBox, self.gRowIndex, 0)
        model = shell.compute_r_for_multiple_lambda_ocl
        self.figure.append(PlotCanvas(self, model=model, width=5, height=4))
        self.globalLayout.addWidget(self.figure[self.gRowIndex] , self.gRowIndex, 1)

        localLayout = LocalLayout(("lmb_min", "lmb_max", "lmb_step", "oscillators_number"), "evaluate", num=self.gRowIndex, figure=self.figure, globalLayout=self.globalLayout, default_values=model.__defaults__)
        self.rFromLambdaGroupBox.setLayout(localLayout.localLayout)

        self.gRowIndex += 1

        # self.graphGroupBox = QGroupBox("graph properties")
        # self.globalLayout.addWidget(self.graphGroupBox, self.gRowIndex, 0)
        #
        self.figure.append(PlotCanvas(self, model=model, width=5, height=4, lables=("xlable","ylable")))
        self.globalLayout.addWidget(self.figure[self.gRowIndex], self.gRowIndex, 1)
        localLayout = QGridLayout()
        localLayout.addWidget(self.figure[self.gRowIndex])
        self.globalLayout = self.createNestedGrid(self.globalLayout, self.gRowIndex, 1, localLayout)

        model = shell.compute_graph_properties_for_system
        localLayout = LocalLayout(("oscillators_number",
                                   "topology",
                                   "reconnectionProbability",
                                   "neighbours"),
                                  "evaluate",
                                  num=self.gRowIndex, figure=self.figure, globalLayout=self.globalLayout, default_values=model.__defaults__
                                  )
        # self.graphGroupBox.setLayout(localLayout.localLayout)
        self.globalLayout = self.createNestedGrid(self.globalLayout, self.gRowIndex, 0, localLayout.localLayout, "graph properties NEW")

        self.horizontalGroupBox.setLayout(self.globalLayout)

    def createNestedGrid(self, parentGrid, row, column, filler, name="Gride View title", ):
        """
        Add Nested Grid into Parend Grid. Addition will be in row and column, filled with filler.
        :param parentGrid:
        :param row:
        :param column:
        :param filler:
        :param name:
        :return:
        """
        graphGroupBox = QGroupBox(name)
        print(filler)
        parentGrid.addWidget(graphGroupBox, row, column)


        graphGroupBox.setLayout(filler)
        return parentGrid



class LocalLayout:

    def __init__(self, args, evaluate, num, figure, globalLayout, default_values=None):

        self.localLayout = QGridLayout()
        self.figure = figure
        self.globalLayout = globalLayout

        i = 0
        self.textboxList = {}
        for string in args:     # so many labels, so many textboxes
            self.textboxList[string] = QLineEdit()
            if default_values:
                self.textboxList[string].insert(str(default_values[i]))
            # self.textboxList[string].text()
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
    """
    # we need to create plot object. To Do that, we use FigureCanvas-like class.
    """
    def __init__(self, parent=None, model=None, width=5, height=4, dpi=100, lables = None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.model = model
        self.axes = fig.add_subplot(111)

        if lables:
            self.xlable, self.ylable = lables
        else:
            self.xlable = None

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self, **kwargs):
        # is plot function, that plot a plot, then you call the plot()
        ax = self.figure.add_subplot(self.axes)
        # ax.set_xlable("sdfsdf")
        ax.cla()
        output_array = self.model(**kwargs)

        # we need to plot lambda and usual graphics by the same plot() method
        if type(output_array) is tuple:
            ax.plot(*output_array)
        else:
            ln = len(output_array[0])
            for pendulum in output_array:
                ax.plot(np.linspace(0, ln, ln), pendulum)

        if self.xlable:
            ax.set_xlable = self.xlable
            ax.set_ylable = self.ylable

        self.draw()



def init_app():
    # one additional layer to compact __main__
    app = QApplication(sys.argv)
    print('i m here')
    ex = App()
    print('i m here')
    sys.exit(app.exec_())
    print('i m here')


if __name__ == '__main__':
    init_app()