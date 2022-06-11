from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from random import choice

textChoices = ["let me in!"]

htmlHtml = """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n
<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n
</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n
<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n
<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:600;\"><br /></p>\n
<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:600;\"><br /></p>\n
<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; m
argin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">AOS-GUI</span></p>\n
<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">v1.0 alpha </span><span style=\" font-size:8pt; font-weight:600; color:#cb0000;\">(do not distribute!)</span></p>\n
<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-weight:600; color:#cb0000;\"><br /></p>\n
<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-weight:600; color:#cb0000;\"><br /></p>\n
<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><sp
an style=\" font-size:8pt; color:#000000;\">created by nanobot567</span></p>\n
<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-weight:600; color:#cb0000;\"><br /></p></body></html>"""

class startupWindow(QWidget):
     def __init__(self):
        super(startupWindow, self).__init__()
        self.setFixedSize(500, 400)
        self.setWindowTitle("AOS-GUI")
        self.html = QTextEdit()
        self.html.setGeometry(QRect(0, 0, 500, 400))
        self.html.setFrameShape(QFrame.NoFrame)
        self.html.setFrameShadow(QFrame.Sunken)
        self.html.setUndoRedoEnabled(False)
        self.html.setReadOnly(True)
        self.html.setTextInteractionFlags(Qt.NoTextInteraction)
        self.html.setHtml(htmlHtml)
        self.closeButton = QPushButton()

        self.closeButton.setText(choice(textChoices))

        self.closeButton.setGeometry(QRect(170, 290, 161, 51))
        self.closeButton.setCheckable(False)
        self.closeButton.setFlat(False)

        Layout = QVBoxLayout(self)
        Layout.addWidget(self.html)
        Layout.addWidget(self.closeButton)


    # setupUi
    # retranslateUi