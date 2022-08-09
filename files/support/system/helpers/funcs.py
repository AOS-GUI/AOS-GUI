from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def msgBox(text, title, icon, buttons):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
    msg.setStandardButtons(buttons)
    retval = msg.exec_()

    return retval