from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from random import choice

splashTexts = ["That's cool and all, but let me in!","Cool!","Oh, alrighty then.","I've got nonexistent work to do!"]


class splashScreen(QWidget):

    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        global splashTexts
        super(splashScreen, self).__init__()

        self.setFixedSize(460, 310)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setWindowTitle(u"AOS-GUI")
        self.aosgui = QLabel(self)
        self.aosgui.setObjectName(u"aosgui")
        self.aosgui.setGeometry(QRect(70, 10, 321, 91))
        self.aosgui.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:48pt;\">AOS-GUI</span></p></body></html>")
        self.aosgui.setTextFormat(Qt.RichText)
        self.aidensos = QLabel(self)
        self.aidensos.setObjectName(u"aidensos")
        self.aidensos.setGeometry(QRect(40, 100, 391, 21))
        self.aidensos.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Aiden's Operating System - Graphical User Interface</span></p></body></html>")
        self.button = QPushButton(self)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(50, 230, 361, 41))
        font = QFont()
        font.setFamily(u"MS Shell Dlg 2")
        font.setPointSize(12)
        self.button.setFont(font)

        self.button.setText(choice(splashTexts))

        self.button.clicked.connect(self.letsgo)
        self.version = QLabel(self)
        self.version.setObjectName(u"version")
        self.version.setGeometry(QRect(130, 130, 211, 20))
        self.version.setText(u"<html><head/><body><p align=\"center\">version 1.0 <span style=\" color:#ff0000;\">alpha</span></p></body></html>")
        self.createdby = QLabel(self)
        self.createdby.setObjectName(u"createdby")
        self.createdby.setGeometry(QRect(130, 170, 211, 20))
        self.createdby.setText(u"<html><head/><body><p align=\"center\"><a href=\"https://github.com/nanobot567/\"><span style=\" text-decoration: underline; color:#0000ff;\">created by nanobot567</span></a></p></body></html>")
        self.createdby.setOpenExternalLinks(True)
        self.dontshowagain = QCheckBox(self)
        self.dontshowagain.setObjectName(u"dontshowagain")
        self.dontshowagain.setGeometry(QRect(160, 280, 151, 20))
        self.dontshowagain.setText(u"Don't show this again")

        QMetaObject.connectSlotsByName(self)

        
    
    def letsgo(self):
        f = open("files/support/data/user/data.aos","r")
        content = f.read()
        content = content.split()
        f.close()
        f = open("files/support/data/user/data.aos","w")
        content[15] = ""
        for i in content:
            if i != "":
                f.write(i+"\n")
        f.write(str(self.dontshowagain.isChecked()))
        f.close()
        self.close()