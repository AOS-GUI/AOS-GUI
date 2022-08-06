from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep
from os import getcwd

filePath = ""
currentlyOpenFile = "Untitled"
currentlyOpenFileName = "Untitled"

class editApp(QWidget):
     def __init__(self):
          super(editApp, self).__init__()
          self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFile}")
          self.setFixedSize(640, 480)
          self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

          self.textEdit = QTextEdit(self)
          self.textEdit.setObjectName(u"textEdit")
          self.textEdit.setGeometry(QRect(10, 40, 621, 431))
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

     def newFile(self):
          global currentlyOpenFile,currentlyOpenFileName
          file,check = QFileDialog.getSaveFileName(None, "New File", getcwd().replace("\\","/")+"/files/")
          if check:
               text = open(file,"w")
               text.close()
               currentlyOpenFile = file
               currentlyOpenFileName = currentlyOpenFile.split("/")
               currentlyOpenFileName = currentlyOpenFileName[-1]
               self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")


     def openFile(self):
          file,check = QFileDialog.getOpenFileName(None, "Open a file", "", "All Files (*)")
          if check:
               text = open(file,"r")
               self.textEdit.setText(text.read())
               text.close()

               global currentlyOpenFile,currentlyOpenFileName
               currentlyOpenFile = file
               currentlyOpenFileName = currentlyOpenFile.split("/")
               currentlyOpenFileName = currentlyOpenFileName[-1]
               self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")
     
     def saveFile(self):
          global currentlyOpenFile,currentlyOpenFileName

          if currentlyOpenFileName == "Untitled":
               self.saveAsFile()
          else:
               text = open(currentlyOpenFile,"w")
               text.write(self.textEdit.toPlainText())
               text.close()
     
     def saveAsFile(self):
          global currentlyOpenFile,currentlyOpenFileName

          file,check = QFileDialog.getSaveFileName(None, "Save", getcwd().replace("\\","/")+"/files/")
          if check:
               text = open(file,"w")
               text.write(self.textEdit.toPlainText())
               text.close()
               currentlyOpenFile = file
               currentlyOpenFileName = currentlyOpenFile.split("/")
               currentlyOpenFileName = currentlyOpenFileName[-1]
               self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")
               
# maybe later :D

# def openFileAtPath(file=""):
#      global filePath
#      filePath = file

#      editApp().__init__()
#      print("inited")