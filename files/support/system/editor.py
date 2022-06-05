from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep

filePath = ""
currentlyOpenFile = "Untitled"

class editApp(QWidget):
     def __init__(self):
          super(editApp, self).__init__()
          self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFile}")
          self.resize(600, 400)

          self.textEdit = QTextEdit()
          # self.textEdit.setText(fileText)
          # self.textEdit.resize(600,100)

          Layout = QVBoxLayout(self)
          Layout.addWidget(self.textEdit)
          # self.setLayout(Layout)

          self.open = QPushButton(self)
          self.open.setObjectName(u"install")
          self.open.setText("open")
          self.open.setGeometry(QRect(230, 380, 50, 20))
          self.open.setAutoFillBackground(False)
          self.open.setAutoDefault(False)
          self.open.clicked.connect(self.openFile)

          self.save = QPushButton(self)
          self.save.setObjectName(u"install")
          self.save.setText("save")
          self.save.setGeometry(QRect(285, 380, 50, 20))
          self.save.setAutoFillBackground(False)
          self.save.setAutoDefault(False)
          self.save.clicked.connect(self.saveFile)

          self.saveAs = QPushButton(self)
          self.saveAs.setObjectName(u"install")
          self.saveAs.setText("save as")
          self.saveAs.setGeometry(QRect(340, 380, 50, 20))
          self.saveAs.setAutoFillBackground(False)
          self.saveAs.setAutoDefault(False)
          self.saveAs.clicked.connect(self.saveAsFile)

     def openFile(self):
          file,check = QFileDialog.getOpenFileName(None, "Open a file", "", "All Files (*)")
          if check:
               print(file)
               text = open(file,"r")
               self.textEdit.setText(text.read())
               text.close()

               global currentlyOpenFile
               currentlyOpenFile = file
               self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFile}")
     
     def saveFile(self):
          global currentlyOpenFile
          print(currentlyOpenFile)

          if currentlyOpenFile == "Untitled":
               self.saveAsFile()
          else:
               text = open(currentlyOpenFile,"w")
               text.write(self.textEdit.toPlainText())
               text.close()
     
     def saveAsFile(self):
          global currentlyOpenFile

          file,check = QFileDialog.getSaveFileName(None, "Save", "")
          if check:
               text = open(file,"w")
               text.write(self.textEdit.toPlainText())
               text.close()
               currentlyOpenFile = file
               self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFile}")
               
# maybe later :D

# def openFileAtPath(file=""):
#      global filePath
#      filePath = file

#      editApp().__init__()
#      print("inited")