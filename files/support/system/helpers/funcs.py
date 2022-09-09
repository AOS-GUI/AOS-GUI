from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def msgBox(text, title, icon=QMessageBox.Information, buttons=QMessageBox.Ok):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
    msg.setStandardButtons(buttons)
    retval = msg.exec_()

    return retval

def userSettings():
    f = open("files/support/data/user/data.aos","r")
    content = f.read()
    content = content.split("\n")

    print("Setting up main window...")

    try:
        themeText = open("files/support/data/user/themes/"+content[2]+".theme","r")
    except FileNotFoundError:
        print("!! WARNING: Theme "+content[2]+" not found, going to default-dark...")
        themeText = open("files/support/data/user/themes/default-dark.theme","r")

    themeText = themeText.read()
    themeColors = themeText.split("\n")


    return content,themeColors