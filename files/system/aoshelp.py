from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class aoshelp(QWidget):
    def __init__(self):
        super(aoshelp, self).__init__()
        self.resize(350, 400)
        self.setWindowTitle("AOS-GUI/help")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.helpText = QTextBrowser(self)
        self.helpText.setReadOnly(True)

        self.reset()

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.Resize):
            self.helpText.setGeometry(0,0,self.frameGeometry().width(),self.frameGeometry().height()-30)
        return super().eventFilter(obj, event)
    
    def reset(self):
        self.resize(350, 400)
        f = open("MDs/help.md")
        text = f.read()
        f.close()

        self.helpText.setMarkdown(text)
        self.helpText.setGeometry(QRect(0, 0, 350, 400))