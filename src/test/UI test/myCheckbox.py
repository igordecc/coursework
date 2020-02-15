import PyQt5
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QMainWindow  #, QWidget, QLabel


class Object():
    def __init__(self, onClickFunction):
        self.OCF = onClickFunction
    def clickBox(self):
        self.OCF()
    pass

class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("Choose plots")
        self.setMinimumSize(QtCore.QSize(300,400))
        # self.graph = Object(lambda:None)
        self.graph = lambda: None
        self.graph.a = QCheckBox("Awesome?", self)
        self.graph.b = QCheckBox("Awesome?", self)
        self.graph.c = QCheckBox("Awesome?", self)
        self.graph.a.stateChanged.connect(self.clickBox)
        self.graph.b.stateChanged.connect(self.clickBox)
        self.graph.c.stateChanged.connect(self.clickBox)
        self.graph.a.move(20,20)
        self.graph.a.resize(320,40)
        self.graph.b.move(20, 60)
        self.graph.b.resize(320, 40)
        self.graph.c.move(20, 100)
        self.graph.c.resize(320, 40)

    def clickBox(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MyWindow()
    mainWin.show()
    sys.exit( app.exec_() )