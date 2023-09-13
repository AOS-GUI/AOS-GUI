from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from files.apps.sdk.sdk import *

import configparser

config = configparser.ConfigParser()
config.read("files/system/data/user/data.aos")

class splashScreen(QWidget):
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
        self.aosgui.setGeometry(QRect(-2, 10, 450, 91))
        self.aosgui.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:48pt;\">AOS-GUI</span></p></body></html>")
        #self.aosgui.setText(u"<html><head/><body><p align=\"center\"><img src='docs/resources/images/aosgui-black.png' style='width: 10px;height: auto;'></img></p></body></html>")
        self.aosgui.setTextFormat(Qt.RichText)
        self.aidensos = QLabel(self)
        self.aidensos.setObjectName(u"aidensos")
        self.aidensos.setGeometry(QRect(0, 100, 451, 21))
        self.aidensos.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Aiden's Operating System - Graphical User Interface</span></p></body></html>")
        self.button = QPushButton(self)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(46, 230, 370, 41))
        font = QFont()
        font.setFamily(u"MS Shell Dlg 2")
        font.setPointSize(12)
        self.button.setFont(font)
        self.button.setText(u"Let me in!")
        self.button.clicked.connect(self.letsgo)
        self.version = QLabel(self)
        self.version.setObjectName(u"version")
        self.version.setGeometry(QRect(-78, 290, 211, 20))
        self.version.setText(u"<html><head/><body><p align=\"center\">"+getVersion()+" <span style=\" color:#ff0000;\">beta</span></p></body></html>")
        self.createdby = QLabel(self)
        self.createdby.setObjectName(u"createdby")
        self.createdby.setGeometry(QRect(126, 120, 211, 20))
        self.createdby.setText(u"<html><head/><body><p align=\"center\"><a href=\"https://github.com/nanobot567/\"><span style=\" text-decoration: underline; color:#0000ff;\">created by nanobot567</span></a></p></body></html>")
        self.createdby.setOpenExternalLinks(True)
        self.dontshowagain = QCheckBox(self)
        self.dontshowagain.setObjectName(u"dontshowagain")
        self.dontshowagain.setGeometry(QRect(155, 280, 150, 20))
        self.dontshowagain.setText(u"Don't show this again")
        self.splashTextLabel = QLabel(self)
        self.splashTextLabel.setObjectName(u"splashTextLabel")
        self.splashTextLabel.setGeometry(QRect(0, 160, 462, 41))
        self.splashTextLabel.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">"+getSplashText(True)+"</span></p></body></html>")

        QMetaObject.connectSlotsByName(self)

    def letsgo(self):
        chked = self.dontshowagain.isChecked()
        if chked == True:
            config["splash"]["show"] = "True"
            with open('files/system/data/user/data.aos', 'w') as configfile:
                config.write(configfile)
        self.hide()