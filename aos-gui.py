from sys import exit
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from files.support.system import fs,render,editor,startupWindow,settings
from files.support.system import cinstall
from files.support.system.setup import setupAOS
from time import sleep
import importlib

buttonFontSize = "font-size:11px"
buttonX = 20
buttonY = 30
buttonsShown = []

class MainWindow(QMainWindow):
     def __init__(self):
          size = app.primaryScreen().size()
          super(MainWindow, self).__init__()
          global textcolor
          global bgcolor
          global ttextcolor
          global tbgcolor
          global btextcolor
          global bbgcolor
          global buttonsShown
          global username

          # apply settings

          f = open("files/support/data/user/data.aos","r")
          content = f.read()
          content = content.split("\n")
          username = content[0]
          textcolor = content[2]
          bgcolor = content[3]
          ttextcolor = content[4]
          tbgcolor = content[5]
          btextcolor = content[6]
          bbgcolor = content[7]
          for i in range(8,13):
               buttonsShown.append(content[i])

          f.close()

          self.setWindowTitle("AOS-GUI")
          # remove title bar
          self.setWindowFlag(Qt.FramelessWindowHint)
          self.setGeometry(0,0,700,500)
          self.setStyleSheet(f"background-color: {bgcolor}; color: {textcolor};")
          self.setupButtons()
          self.setupMenuBar()
          # self.openStartupWindow()

     def setupButtons(self):
          global buttonX
          if buttonsShown[0] == "True":
               self.settings = QPushButton(self)
               self.settings.setGeometry(buttonX, 30, 100,50)
               self.settings.setText('AOS-GUI Settings')
               self.settings.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.settings.setCursor(Qt.CursorShape.PointingHandCursor)
               self.settings.window = settings.settingsWidget()
               self.settings.clicked.connect(self.settings.window.show)
               self.settings.clicked.connect(self.settings.window.activateWindow)
               buttonX += 120
               

          if buttonsShown[1] == "True":
               self.rndrButton = QPushButton(self)
               self.rndrButton.setGeometry(buttonX, 30, 100,50)
               self.rndrButton.setText('Run .rndr')
               self.rndrButton.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.rndrButton.setCursor(Qt.CursorShape.PointingHandCursor)
               self.rndrButton.clicked.connect(self.rndr)
               buttonX += 120
          
          if buttonsShown[2] == "True":
               self.fs = QPushButton(self)
               self.fs.setGeometry(buttonX, 30, 100,50)
               self.fs.setText('FileSystem')
               self.fs.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.fs.setCursor(Qt.CursorShape.PointingHandCursor)
               self.fs.window = fs.FsWindow()
               self.fs.clicked.connect(self.fs.window.show)
               self.fs.clicked.connect(self.fs.window.activateWindow)
               buttonX += 120

          if buttonsShown[3] == "True":
               self.cInst = QPushButton(self)
               self.cInst.setGeometry(buttonX, 30, 100,50)
               self.cInst.setText('camelInstall')
               self.cInst.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.cInst.setCursor(Qt.CursorShape.PointingHandCursor)
               self.cInst.window = cinstall.camelInstall()
               self.cInst.clicked.connect(self.cInst.window.show)
               self.cInst.clicked.connect(self.cInst.window.activateWindow)
               buttonX += 120

          if buttonsShown[4] == "True":
               self.edit = QPushButton(self)
               self.edit.setGeometry(buttonX, 30, 100,50)
               self.edit.setText('Edit')
               self.edit.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.edit.setCursor(Qt.CursorShape.PointingHandCursor)
               self.edit.window = editor.editApp()
               self.edit.clicked.connect(self.edit.window.show)
               self.edit.clicked.connect(self.edit.window.activateWindow)
               buttonX += 120

     def setupMenuBar(self):
          menuBar = self.menuBar()

          menuBar.setStyleSheet(f"background-color: {tbgcolor}; color: {ttextcolor};")

          self.settings = settings.settingsWidget()
          # cinstall.window = cinstall.Ui_camelInstaller()

          self.runAction = QAction("&Run...", self)
          # self.cInstAction = QAction("&camelInstall", self)
          self.setAction = QAction("&Settings", self)
          self.exitAction = QAction("&Exit", self)


          aosMenu = QMenu(f"&AOS - {username}", self)
          menuBar.addMenu(aosMenu)
          aosMenu.addAction(self.runAction)
          # aosMenu.addAction(self.cInstAction)
          aosMenu.addAction(self.setAction)
          aosMenu.addAction(self.exitAction)

          self.runAction.triggered.connect(self.run)
          # self.cInstAction.triggered.connect(cinstall.window.show)
          self.setAction.triggered.connect(self.settings.show)
          self.exitAction.triggered.connect(self.close)

     def rndr(self):
          rndr,check = QFileDialog.getOpenFileName(None, "Open a .rndr", "", "Renderable file (*.rndr);;All Files (*)")
          if check:
               print(rndr)

     def run(self):
          prgm,done = QInputDialog.getText(
             self, 'Run', 'Type the program you would like to run (.py extension not needed)')
          
          if prgm.isspace() or prgm == "":
               pass
          else:
               if prgm.lower() == "fs":
                    self.fs.window.show()
               elif prgm.lower() == "editor":
                    self.edit.window.show()
               elif prgm.lower() == "settings":
                    self.settings.show()
               elif prgm.lower() == "render":
                    self.rndr()
               else:
                    try:
                         modulePrgm = importlib.import_module("files.apps."+prgm)
                         importlib.reload(modulePrgm)
                    except ModuleNotFoundError:
                         pass
               self.setStyleSheet(f"background-color: {bgcolor}; color: {textcolor};")
     # setupUi

     # def openStartupWindow(self):
     #      self.startupWin = startupWindow.startupWindow()
     #      self.startupWin.show()
     #      self.startupWin.raise_()



if __name__ == '__main__':
     app = QApplication([])
     try:
          f = open("files/support/data/user/data.aos", "r")
          window = MainWindow()
          window.showFullScreen()
          f.close()
     except FileNotFoundError:
          window = setupAOS.installform()
          window.show()
     # window = MainWindow()
     exit(app.exec_())