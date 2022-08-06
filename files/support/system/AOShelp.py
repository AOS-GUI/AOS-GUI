from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class aoshelp(QWidget):
    def __init__(self):
        super(aoshelp, self).__init__()
        self.setFixedSize(1000, 1000)
        self.move(0, 0)
        self.setWindowTitle("AOS-GUI/help")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)