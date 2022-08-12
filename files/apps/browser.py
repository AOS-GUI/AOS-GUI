# required imports

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

from files.support.system.helpers.funcs import msgBox

# next line is the project description, format is '#(tilde){name}|{desc}|{ver}'
#~browser|browser|v1.0


# class name can be anything

url = "https://duckduckgo.com/"

class browser(QWidget):
    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        super(browser, self).__init__()
        self.setFixedSize(800, 650)
        self.setWindowTitle("AOS-GUI browser")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint) # this line is needed for the program to stay on top of desktop

        self.urlButton = QPushButton(self)
        self.urlButton.setGeometry(QRect(0, 0, 50, 20))
        self.urlButton.setText("Set URL")
        self.urlButton.clicked.connect(self.setURL)

        self.web = QWebEngineView(self)
        self.web.setGeometry(0,20,800,630)
        self.web.load(QUrl(url))
        self.web.show()

    def setURL(self):
        url, ok = QInputDialog.getText(self, "Enter URL","Please enter a URL:", QLineEdit.Normal, "")
        self.web.load(QUrl(url))

window = browser()
window.show()