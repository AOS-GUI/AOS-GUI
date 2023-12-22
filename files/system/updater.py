from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
import json
import webbrowser

from files.apps.sdk.sdk import *

class updater(QWidget):
    def __init__(self):
        super(updater, self).__init__()
        self.setFixedSize(500, 500)
        self.setWindowTitle("updater")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        with open(getAOSdir()+"/system/data/version","r") as f:
            try:
                r = requests.get("https://raw.githubusercontent.com/AOS-GUI/AOS-GUI/main/files/system/data/version")
                if compareVersion(f.read(),r.text) == -1:
                    resp = msgBox("Your version of AOS is outdated! Would you like to update now (this will open a browser tab with the AOS-GUI install page)?\n\n(Hint: if you don't want to be told that your version is outdated, remove 'updater' in autorun.aos!)","AOS-GUI/updater",buttons=QMessageBox.Yes|QMessageBox.No)
                    if resp == QMessageBox.Yes:
                        webbrowser.open("https://github.com/aos-gui/aos-gui/releases/latest")
                        raise SystemExit
            except Exception as e:
                pass
