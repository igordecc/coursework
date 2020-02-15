from PyQt5 import QtCore, QtGui, QtWidgets
from power_bar import PowerBar
from widgetCheckbox import Window

app = QtWidgets.QApplication([])
volume = Window()
volume.show()
app.exec_()