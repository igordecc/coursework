import addict
x = addict.Dict()
x.a.b.c.d = 1
print(x.a.b.c.d)


from PyQt5.QtWidgets import QWidget


class myClass(QWidget):
    def __init__(self, x, y):
        super(QWidget).__init__()
        self.sum = x + y


x = myClass(5,6)
print(x.sum)