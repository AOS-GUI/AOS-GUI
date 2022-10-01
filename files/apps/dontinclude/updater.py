from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests

from files.system.sdk.sdk import *
version = aosVersion()

class updater(QWidget):
    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        super(updater, self).__init__()
        self.setFixedSize(500, 400)
        self.setWindowTitle("AOS-GUI")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.btn = QPushButton("Check for updates", self)
        self.btn.setGeometry(30,30,125,100)
        self.btn.clicked.connect(self.checkForUpdates)
        
    def checkForUpdates(self):
        # txt = requests.get("https://raw.githubusercontent.com/Nanobot567/AOS-GUI/main/files/support/data/version?token=GHSAT0AAAAAABXWSMDCGIVCYIIIBEQDG4L4YZUM3FQ").text
        txt = "0.2"
        try:
            if float(txt) > float(version):
                ret = msgBox("AOS is outdated! Would you like to update now?","Outdated AOS!",QMessageBox.Critical,QMessageBox.Yes|QMessageBox.No)
                if ret == 16384:
                    # update
                    pass
            elif float(txt) < float(version):
                msgBox("Wow! You're running a version of AOS that is so far into the future that it doesn't exist yet!","Woah!")
            else:
                msgBox("Looks like you're up to date!", "Up to date!")
        except:
            msgBox("Looks like you're either using a nonexistent version of AOS, or you're simply testing a prerelease.","Huh???")

window = updater()
window.show()