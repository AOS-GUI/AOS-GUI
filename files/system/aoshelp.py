from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

f = open("MDs/help.md")
text = f.read()
f.close()

class aoshelp(QWidget):
    def __init__(self):
        super(aoshelp, self).__init__()
        self.setFixedSize(600, 600)
        self.setWindowTitle("AOS-GUI/help")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.helpText = QTextBrowser(self)
        self.helpText.setGeometry(QRect(0, 0, 600, 600))
        self.helpText.setReadOnly(True)
        self.helpText.setMarkdown(text)