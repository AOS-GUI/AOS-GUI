from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

f = open("MDs/manual.md")
text = f.read()
f.close()

class aoshelp(QWidget):
    def __init__(self):
        super(aoshelp, self).__init__()
        self.setFixedSize(500, 500)
        self.setWindowTitle("AOS-GUI/help")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.helpText = QTextEdit(self)
        self.helpText.setGeometry(QRect(0, 0, 500, 500))
        self.helpText.setReadOnly(True)
        self.helpText.setMarkdown(text)