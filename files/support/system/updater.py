from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class updater(QWidget):
    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        super(updater, self).__init__()
        self.setFixedSize(500, 400)
        self.setWindowTitle("AOS-GUI")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        