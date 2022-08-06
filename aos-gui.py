try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

try:
     from PyQt5.QtGui import *
     from PyQt5.QtWidgets import *
     from PyQt5.QtCore import *
     from PyQt5.QtPrintSupport import *
except:
     print("Installing AOS-GUI requirements...")
     pipmain(["install","PyQt5"])
     # pipmain(["install","PyQtWebEngine"])
     print("Done! Starting up...")

     from PyQt5.QtGui import *
     from PyQt5.QtWidgets import *
     from PyQt5.QtCore import *
     from PyQt5.QtPrintSupport import *

from files.support.system import fs,editor,startupWindow,settings,AOShelp,aterm,splash
from files.support.system import cinstall
from files.support.system.setup import setupAOS

from time import sleep
import importlib
import sys
import os

fontSize = 11
buttonFontSize = f"font-size:{fontSize}px"
buttonX = 20
buttonY = 40
buttonsShown = []

kSeqs = []

class AOS(QMainWindow):
     def __init__(self):
          size = app.primaryScreen().size()
          super(AOS, self).__init__()
          global textcolor,bgcolor,ttextcolor,tbgcolor,btextcolor,bbgcolor,buttonsShown,theme,username,password,kSeqs,fontSize,buttonFontSize

          # apply settings

          f = open("files/support/data/user/data.aos","r")
          content = f.read()
          content = content.split("\n")

          themeText = open("files/support/data/user/themes/"+content[2]+".theme","r")
          themeText = themeText.read()
          themeColors = themeText.split("\n")
          username = content[0]
          password = content[1]
          fontSize = content[3]
          buttonFontSize = f"font-size:{fontSize}px"
          for i in range(4,8):
               kSeqs.append(content[i])
          textcolor = themeColors[0]
          bgcolor = themeColors[1]
          ttextcolor = themeColors[3]
          tbgcolor = themeColors[2]
          btextcolor = themeColors[5]
          bbgcolor = themeColors[4]
          for i in range(8,len(content)):
               buttonsShown.append(content[i])

          f.close()

          self.setWindowTitle("AOS-GUI")
          # remove title bar
          self.setWindowFlag(Qt.FramelessWindowHint)
          self.setGeometry(0,0,700,500)
          self.setStyleSheet(f"background-color: {bgcolor}; color: {textcolor};")
          self.setupButtons()
          self.setupMenuBar()
          self.setupShortcuts()
          # self.openStartupWindow()

     def setupButtons(self):
          global buttonX
          global buttonY

          self.settingsWindow = settings.settingsWidget()
          self.fsWindow = fs.FsWindow()
          self.cInstWindow = cinstall.camelInstall()
          self.editWindow = editor.editApp()
          self.helpWindow = AOShelp.aoshelp()
          self.atermWindow = aterm.aterm()

          if buttonsShown[0] == "True":
               self.settings = QPushButton(self)
               self.settings.setGeometry(buttonX, buttonY, 100,50)
               self.settings.setText('Settings')
               self.settings.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.settings.setCursor(Qt.CursorShape.PointingHandCursor)
               self.settings.clicked.connect(self.settingsWindow.show)
               self.settings.clicked.connect(self.settingsWindow.activateWindow)
               buttonX += 120
               

          if buttonsShown[1] == "True":
               self.rndrButton = QPushButton(self)
               self.rndrButton.setGeometry(buttonX, buttonY, 100,50)
               self.rndrButton.setText('Run .rndr')
               self.rndrButton.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.rndrButton.setCursor(Qt.CursorShape.PointingHandCursor)
               self.rndrButton.clicked.connect(self.rndr)
               buttonX += 120
          
          if buttonsShown[2] == "True":
               self.fs = QPushButton(self)
               self.fs.setGeometry(buttonX, buttonY, 100,50)
               self.fs.setText('FileSystem')
               self.fs.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.fs.setCursor(Qt.CursorShape.PointingHandCursor)
               self.fs.clicked.connect(self.fsWindow.show)
               self.fs.clicked.connect(self.fsWindow.activateWindow)
               buttonX += 120

          if buttonsShown[3] == "True":
               self.cInst = QPushButton(self)
               self.cInst.setGeometry(buttonX, buttonY, 100,50)
               self.cInst.setText('camelInstall')
               self.cInst.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.cInst.setCursor(Qt.CursorShape.PointingHandCursor)
               self.cInst.clicked.connect(self.cInstWindow.show)
               self.cInst.clicked.connect(self.cInstWindow.activateWindow)
               buttonX += 120

          if buttonsShown[4] == "True":
               self.edit = QPushButton(self)
               self.edit.setGeometry(buttonX, buttonY, 100,50)
               self.edit.setText('Edit')
               self.edit.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.edit.setCursor(Qt.CursorShape.PointingHandCursor)
               self.edit.clicked.connect(self.editWindow.show)
               self.edit.clicked.connect(self.editWindow.activateWindow)
               buttonX += 120

          if buttonsShown[5] == "True":
               self.help = QPushButton(self)
               self.help.setGeometry(buttonX, buttonY, 100,50)
               self.help.setText('AOSHelp')
               self.help.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.help.setCursor(Qt.CursorShape.PointingHandCursor)
               self.help.clicked.connect(self.helpWindow.show)
               self.help.clicked.connect(self.helpWindow.activateWindow)
               buttonX += 120
          
          if buttonsShown[6] == "True":
               self.aterm = QPushButton(self)
               self.aterm.setGeometry(buttonX, buttonY, 100,50)
               self.aterm.setText('Terminal')
               self.aterm.setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               self.aterm.setCursor(Qt.CursorShape.PointingHandCursor)
               self.aterm.clicked.connect(self.atermWindow.show)
               self.aterm.clicked.connect(self.atermWindow.activateWindow)
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
                    self.fsWindow.show()
               elif prgm.lower() == "editor":
                    self.editWindow.show()
               elif prgm.lower() == "settings":
                    self.settings.show()
               elif prgm.lower() == "render":
                    self.rndr()
               elif prgm.lower() == "aoshelp":
                    self.helpWindow.show()
               elif prgm.lower() == "cinstall":
                    self.cInstWindow.show()
               elif prgm.lower() == "aterm":
                    self.atermWindow.show()
               else:
                    try:
                         modulePrgm = importlib.import_module("files.apps."+prgm)
                         importlib.reload(modulePrgm)
                    except ModuleNotFoundError:
                         msg = QMessageBox()
                         msg.setIcon(QMessageBox.Critical)
                         msg.setText(f"No app called \"{prgm}\" found in files/apps")
                         msg.setWindowTitle("ERROR!")
                         msg.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
                         msg.setStandardButtons(QMessageBox.Ok)
                         retval = msg.exec_()
                    except Exception as err:
                         msg = QMessageBox()
                         msg.setIcon(QMessageBox.Critical)
                         msg.setText(f"Critical error in app \"{prgm}\": {err}")
                         msg.setWindowTitle("ERROR!")
                         msg.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
                         msg.setStandardButtons(QMessageBox.Ok)
                         retval = msg.exec_()

               self.setStyleSheet(f"background-color: {bgcolor}; color: {textcolor};")

     def setupShortcuts(self):
          self.runSC = QShortcut(QKeySequence(kSeqs[0]), self)
          self.termSC = QShortcut(QKeySequence(kSeqs[1]), self)
          self.setSC = QShortcut(QKeySequence(kSeqs[2]), self)
          self.helpSC = QShortcut(QKeySequence(kSeqs[3]), self)
          self.runSC.activated.connect(self.run)
          self.termSC.activated.connect(self.atermWindow.show)
          self.setSC.activated.connect(self.settings.show)
          self.helpSC.activated.connect(self.helpWindow.show)
     # setupUi

     # def openStartupWindow(self):
     #      self.startupWin = startupWindow.startupWindow()
     #      self.startupWin.show()
     #      self.startupWin.raise_()
# +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


if __name__ == '__main__':
     app = QApplication([])

     try:
          f = open("files/support/data/user/data.aos", "r")
          window = AOS()
          window.showFullScreen()

          content = f.read()
          content = content.split("\n")
          if content[1] != "":
               passwordInput = ""
               while passwordInput != content[1]:
                    passwordInput, z = QInputDialog.getText(window, "Password","Please enter your password:", QLineEdit.Normal, "")
          if content[15] == "False" or content[15] == "":
               splashscreen = splash.splashScreen()
               splashscreen.show()

          f.close()
     except Exception as e:
          if not str(e).startswith("[Errno 2]"):
               print(e)
          window = setupAOS.installform()
          window.show()

     # window = MainWindow()
     exit(app.exec_())