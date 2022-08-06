# required imports

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# next line is the project description, format is #(tilde){name}|{desc}|{ver}
#~myapp|my app!|v0.1


# class name can be anything


class main_print(QWidget):

    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        super(main_print, self).__init__()
        self.setFixedSize(500, 400)
        self.setWindowTitle("AOS-GUI")
        self.setStyleSheet(f"background-color: {self.bgcolor}; color: {self.textcolor};")
        self.closeButton = QPushButton(self)

        self.closeButton.setText("hi")

        self.closeButton.setGeometry(QRect(170, 130, 161, 51))
        self.closeButton.setCheckable(False)
        self.closeButton.setFlat(False)

# these last two lines must be included for the app to launch.

window = main_print()
window.show()