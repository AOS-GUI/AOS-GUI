from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class aoshelp(QWidget):
    def __init__(self):
        super(aoshelp, self).__init__()
        self.setFixedSize(400, 400)
        self.move(0, 0)
        self.setWindowTitle("AOS-GUI")

        self.closeButton = QPushButton(self)
        self.closeButton.setText("hi")
        self.closeButton.setGeometry(QRect(170, 130, 161, 51))
        self.closeButton.setCheckable(False)
        self.closeButton.setFlat(False)