# TODO plot lables
# TODO plot grid
import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
# PyQt5 UI stuff. Widjets, midjets etc.
from PyQt5.QtWidgets import QLineEdit, QApplication, QPushButton, QSizePolicy, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel, QWidget
from PyQt5 import QtWidgets, QtCore
# matplot libraries need to do plotting stuff
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# project modules used in this one
import shell


class _CheckBar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        barLayout = QGridLayout()
        barLayout.setColumnStretch(4,1)

        name_list = [
            "show default parameters",
            "show first plot",
            "show second plot",
            "show third plot"
        ]

        self.checkbox = []
        for i in range(4):
            self.checkbox.append(QtWidgets.QCheckBox())
            self.checkbox[i].setText(name_list[i])
            self.trigger = QtCore.pyqtSignal()

            self.checkbox[i].isChecked()
            barLayout.addWidget(self.checkbox[i], i, 0)

        self.setLayout(barLayout)


    def changeEvent(self, e):
        pass

    def sizeHint(self):
        return QtCore.QSize(40,120)

    def _trigger_refresh(self):
        self.update()

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.Qt import pyqtSignal as Signal
class Foo(QWidget):
    trigger = Signal()

    def __init__(self):
        super().__init__()
        # Define a new signal called 'trigger' that has no arguments.
        self.checkbox = QtWidgets.QCheckBox()

    def connect_and_emit_trigger(self):
        # Connect the trigger signal to a slot.
        self.trigger.connect(self.handle_trigger)

        # Emit the signal.
        self.trigger.emit()

    def handle_trigger(self):
        # Show that the slot has been called.

        print("trigger signal received")



class App(QWidget):

    def __init__(self, parent=None):
        super(QWidget , self).__init__(parent)
        self.title = 'PyQt5 layout'
        self.left = 400
        self.top = 200
        self.width = 800
        self.height = 600
        Foo()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        windowLayout = QVBoxLayout()
        self._CheckBar = _CheckBar()
        self.checkbox = self._CheckBar.checkbox
        windowLayout.addWidget(self._CheckBar)

        self.createGridLayout()

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

        "----------------------------------------------------------------"
        """
        compute one oscillators system to see phases behavior.
        """

        self.gRowIndex = 0

        self.oscGroupBox = QGroupBox("oscillators")
        self.globalLayout.addWidget(self.oscGroupBox, self.gRowIndex, 0)
        model = shell.compute_system_ocl
        self.figure.append(PlotCanvas(self, model=model, width=5, height=4))
        self.globalLayout.addWidget(self.figure[self.gRowIndex], self.gRowIndex, 1)

        localLayout = LocalLayout(("osc_min", "osc_max", "osc_step"), "evaluate", num=self.gRowIndex, figure=self.figure, globalLayout=self.globalLayout, default_values=model.__kwdefaults__)
        self.oscGroupBox.setLayout(localLayout.localLayout)
        "-----------------------------------------------------------------"
        """
        compute system set for lambdas in range. plot order parametr.   
        """
        self.gRowIndex += 1
        self.rFromLambdaGroupBox = QGroupBox("r from lambda")
        self.globalLayout.addWidget(self.rFromLambdaGroupBox, self.gRowIndex, 0)
        model = shell.compute_r_for_multiple_lambda_ocl
        self.figure.append(PlotCanvas(self, model=model, width=5, height=4))
        self.globalLayout.addWidget(self.figure[self.gRowIndex] , self.gRowIndex, 1)

        localLayout = LocalLayout(("lmb_min", "lmb_max", "lmb_step", "oscillators_number", "topology"),
                                  "evaluate",
                                  num=self.gRowIndex,
                                  figure=self.figure,
                                  globalLayout=self.globalLayout,
                                  default_values=model.__kwdefaults__)
        self.rFromLambdaGroupBox.setLayout(localLayout.localLayout)
        """-------------------------------------------------------------"""
        if self._CheckBar.checkbox[3].isChecked():

            self.gRowIndex += 1

            # self.graphGroupBox = QGroupBox("graph properties")
            # self.globalLayout.addWidget(self.graphGroupBox, self.gRowIndex, 0)
            #
            model = shell.compute_graph_properties_for_system
            self.figure.append(PlotCanvas(self, model=model, width=5, height=4, lables=("xlable","ylable")))
            self.globalLayout.addWidget(self.figure[self.gRowIndex], self.gRowIndex, 1)
            localLayout = QGridLayout()
            localLayout.addWidget(self.figure[self.gRowIndex])
            self.globalLayout = self.createNestedGrid(self.globalLayout,
                                                      self.gRowIndex,
                                                      1,
                                                      localLayout,
                                                      "plot")

            localLayout = LocalLayout(("oscillators_number", "topology", "reconnectionProbability","neighbours"),
                                      "evaluate",
                                      num=self.gRowIndex,
                                      figure=self.figure,
                                      globalLayout=self.globalLayout,
                                      default_values=model.__kwdefaults__
                                      )
            # self.graphGroupBox.setLayout(localLayout.localLayout)
            self.globalLayout = self.createNestedGrid(self.globalLayout,
                                                      self.gRowIndex,
                                                      0,
                                                      localLayout.localLayout,
                                                      "graph properties NEW")
            "-----------------------------------------------------------"
        self.horizontalGroupBox.setLayout(self.globalLayout)

    def createNestedGrid(self, parentGrid, row, column, fillerGrid, name="Gride View title", ):
        """
        Add Nested Grid into Parend Grid. Addition will be in row and column, filled with filler grid (with content).
        :param parentGrid:
        :param row:
        :param column:
        :param fillerGrid:
        :param name:
        :return:
        """
        graphGroupBox = QGroupBox(name)
        parentGrid.addWidget(graphGroupBox, row, column)


        graphGroupBox.setLayout(fillerGrid)
        return parentGrid


class randomclass(QWidget):
    def __init__(self):
        super.__init__()


class LocalLayout:

    def __init__(self, args, evaluate, num, figure, globalLayout, default_values=None):

        self.localLayout = QGridLayout()
        self.figure = figure
        self.globalLayout = globalLayout

        i = 0
        self.textboxList = {}
        for _string in args:     # so many labels, so many textboxes
            self.textboxList[_string] = QLineEdit()
            if default_values:
                self.textboxList[_string].insert(str(default_values[_string]))
            # self.textboxList[string].text()
            #self.textboxList[string].setValidator(QDoubleValidator()) #DON'T allow type "." charackter. Work wrong!
            self.localLayout.addWidget(self.textboxList[_string], i, 0)
            self.localLayout.addWidget(QLabel(_string), i, 1)
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
    ex = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    init_app()