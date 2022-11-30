from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from os import getcwd

from files.system.sdk.sdk import msgBox

filePath = ""
currentlyOpenFile = "Untitled"
currentlyOpenFileName = "Untitled"
originalText = ""

class editApp(QWidget):
    def __init__(self):
        super(editApp, self).__init__()
        global textEdit
        self.originalText = ""
        self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFile}")
        self.setFixedSize(640, 480)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        textEdit = QTextEdit(self)
        textEdit.setObjectName(u"textEdit")
        textEdit.setGeometry(QRect(10, 40, 621, 431))
        textEdit.textChanged.connect(self.updateStatus)
        self.open = QPushButton(self)
        self.open.setObjectName(u"open")
        self.open.setGeometry(QRect(60, 10, 51, 28))
        self.open.setText(u"Open")
        self.open.clicked.connect(self.openFile)
        self.save = QPushButton(self)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(120, 10, 51, 28))
        self.save.setText(u"Save")
        self.save.clicked.connect(self.saveFile)
        self.saveAs = QPushButton(self)
        self.saveAs.setObjectName(u"saveAs")
        self.saveAs.setGeometry(QRect(180, 10, 71, 28))
        self.saveAs.setText(u"Save As")
        self.saveAs.clicked.connect(self.saveAsFile)
        self.newFileBtn = QPushButton(self)
        self.newFileBtn.setObjectName(u"newFile")
        self.newFileBtn.setGeometry(QRect(10, 10, 41, 28))
        self.newFileBtn.setText("New")
        self.newFileBtn.clicked.connect(self.newFile)
        self.formatBox = QComboBox(self)
        self.formatBox.addItem(u"Plaintext")
        self.formatBox.addItem(u"Markdown")
        self.formatBox.addItem(u"HTML")
        self.formatBox.setObjectName(u"formatBox")
        self.formatBox.setGeometry(QRect(490, 10, 141, 21))
        self.formatBox.activated.connect(self.updateText)
        
    def updateStatus(self):
        self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}*")

    def updateText(self):
        if self.formatBox.currentText() == "Plaintext":
            if self.originalText != "":
                textEdit.setText(self.originalText)
            else:
                textEdit.setText(textEdit.toPlainText())
        elif self.formatBox.currentText() == "Markdown":
            self.originalText = textEdit.toPlainText()
            textEdit.setMarkdown(textEdit.toMarkdown())
        elif self.formatBox.currentText() == "HTML":
            self.originalText = textEdit.toPlainText()
            textEdit.setHtml(textEdit.toHtml())

    def newFile(self):
        ret = msgBox("Would you like to save your current file?", "Save?", QMessageBox.Information, QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.saveAsFile()

        textEdit.setText("")
        self.formatBox.setCurrentText("Plaintext")

        # global currentlyOpenFile,currentlyOpenFileName
        # file,check = QFileDialog.getSaveFileName(None, "New File", directory=getcwd().replace("\\","/")+"/files/")
        # if check:
        #     text = open(file,"w")
        #     text.close()
        #     currentlyOpenFile = file
        #     currentlyOpenFileName = currentlyOpenFile.split("/")
        #     currentlyOpenFileName = currentlyOpenFileName[-1]
        #     self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")


    def openFile(self):
        file,check = QFileDialog.getOpenFileName(None, "Open a file", getcwd().replace("\\","/")+"/files/", "All Files (*)")
        if check:
            text = open(file,"r")
            textEdit.setText(text.read())
            text.close()

            global currentlyOpenFile,currentlyOpenFileName
            currentlyOpenFile = file
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
            self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
    
    def saveFile(self):
        global currentlyOpenFile,currentlyOpenFileName

        if currentlyOpenFileName == "Untitled":
            self.saveAsFile()
        else:
            text = open(currentlyOpenFile,"w")
            text.write(textEdit.toPlainText())
            text.close()
            self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
    
    def saveAsFile(self):
        global currentlyOpenFile,currentlyOpenFileName

        file,check = QFileDialog.getSaveFileName(None, "Save", directory=getcwd().replace("\\","/")+"/files/")
        if check:
            text = open(file,"w")
            text.write(textEdit.toPlainText())
            text.close()
            currentlyOpenFile = file
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
        else:
            self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")

    def openViaOutsideSource(self, path):
        if self == None:
            self = super(editApp, self).__init__
            print("self none")
        text = open(path,"r")
        textEdit.setText(text.read())
        text.close()

        global currentlyOpenFile,currentlyOpenFileName
        currentlyOpenFile = path
        currentlyOpenFileName = currentlyOpenFile.split("/")
        currentlyOpenFileName = currentlyOpenFileName[-1]
        editApp().setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
        editApp().show()