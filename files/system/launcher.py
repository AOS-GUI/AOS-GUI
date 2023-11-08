from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from files.apps.sdk.sdk import *

from os import listdir,path

class launcher(QWidget):
    def __init__(self):
        super(launcher, self).__init__()

        self.setFixedSize(400, 300)
        self.setWindowTitle(u"AOS-GUI/launcher")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.appList = QListWidget(self)
        self.appList.setObjectName(u"appList")
        self.appList.setGeometry(QRect(0, 0, 401, 261))
        self.launchButton = QPushButton(self)
        self.launchButton.setObjectName(u"launchButton")
        self.launchButton.setGeometry(QRect(100, 270, 81, 23))
        self.launchButton.setText(u"Launch App")
        def errRoutine():
            prgm = self.appList.currentItem().text().split(".py")[0]
            ret, err = openApplication(prgm)
            if err:
                msgBox("Error in "+prgm+": "+str(err),"AOS-GUI/execRoutine")
        self.launchButton.clicked.connect(errRoutine)
        self.refreshButton = QPushButton(self)
        self.refreshButton.setObjectName(u"refreshButton")
        self.refreshButton.setGeometry(QRect(220, 270, 75, 23))
        self.refreshButton.setText(u"Refresh")
        self.refreshButton.clicked.connect(self.grabExtApps)

        self.grabExtApps()

    def grabExtApps(self):
        self.appList.clear()
        for file in listdir("files/apps/"):
            if path.isfile(path.join("files/apps/", file)):
                self.appList.addItem(QListWidgetItem(file))
