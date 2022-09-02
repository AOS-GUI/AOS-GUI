from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import listdir,path,getcwd
from files.support.system.helpers.funcs import *
import importlib

class launcher(QWidget):
    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        super(launcher, self).__init__()

        self.resize(400, 300)
        self.setWindowTitle(u"appLauncher")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.appList = QListWidget(self)
        self.appList.setObjectName(u"appList")
        self.appList.setGeometry(QRect(0, 0, 401, 261))
        self.launchButton = QPushButton(self)
        self.launchButton.setObjectName(u"launchButton")
        self.launchButton.setGeometry(QRect(100, 270, 81, 23))
        self.launchButton.setText(u"Launch App")
        self.launchButton.clicked.connect(self.launchExtApp)
        self.refreshButton = QPushButton(self)
        self.refreshButton.setObjectName(u"refreshButton")
        self.refreshButton.setGeometry(QRect(220, 270, 75, 23))
        self.refreshButton.setText(u"Refresh")
        self.refreshButton.clicked.connect(self.grabExtApps)

        self.grabExtApps()

    def launchExtApp(self):
        prgm = self.appList.currentItem().text().split(".py")[0]
        try:
            modulePrgm = importlib.import_module("files.apps."+prgm)
            importlib.reload(modulePrgm)
        except ModuleNotFoundError:
                msgBox(f"No app called \"{prgm}\" found in files/apps","ERROR!",QMessageBox.Critical,QMessageBox.Ok)
        except Exception as err:
                msgBox(f"Critical error in app \"{prgm}\": {err}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)

    def grabExtApps(self):
        self.appList.clear()
        for file in listdir("files/apps/"):
            if path.isfile(path.join("files/apps/", file)):
                self.appList.addItem(QListWidgetItem(file))