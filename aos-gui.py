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

from files.support.system import fs,editor,settings,AOShelp,aterm,splash
from files.support.system import cinstall
from files.support.system.setup import setupAOS
from files.support.system.helpers.funcs import *

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
          
          buttonsShown = content[8].split("|")

          f.close()

          self.setWindowTitle("AOS-GUI")
          # remove title bar
          self.setWindowFlag(Qt.FramelessWindowHint)
          self.setGeometry(0,0,700,500)
          self.setStyleSheet(f"background-color: {bgcolor}; color: {textcolor};")
          self.setupButtons()
          self.setupMenuBar()
          self.setupShortcuts()

     def setupButtons(self):
          global buttonX
          global buttonY

          self.settingsWindow = settings.settingsWidget()
          self.fsWindow = fs.FsWindow()
          self.cInstWindow = cinstall.camelInstall()
          self.editWindow = editor.editApp()
          self.helpWindow = AOShelp.aoshelp()
          self.atermWindow = aterm.aterm()

          btnName = 0

          for i in buttonsShown:
               if i == "True":
                    globals()[btnName] = QPushButton(self)
                    globals()[btnName].setGeometry(buttonX,buttonY,100,50)
                    globals()[btnName].setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
                    globals()[btnName].setCursor(Qt.CursorShape.PointingHandCursor)

                    if btnName == 0:
                         globals()[btnName].setText("Settings")
                         globals()[btnName].clicked.connect(self.settingsWindow.show)
                         globals()[btnName].clicked.connect(self.settingsWindow.activateWindow)
                    elif btnName == 1:
                         globals()[btnName].setText("Run .rndr")
                         globals()[btnName].clicked.connect(self.rndr)
                    elif btnName == 2:
                         globals()[btnName].setText("FileSystem")
                         globals()[btnName].clicked.connect(self.fsWindow.show)
                         globals()[btnName].clicked.connect(self.fsWindow.activateWindow)
                    elif btnName == 3:
                         globals()[btnName].setText("camelInstall")
                         globals()[btnName].clicked.connect(self.cInstWindow.show)
                         globals()[btnName].clicked.connect(self.cInstWindow.activateWindow)
                    elif btnName == 4:
                         globals()[btnName].setText("Edit")
                         globals()[btnName].clicked.connect(self.editWindow.show)
                         globals()[btnName].clicked.connect(self.editWindow.activateWindow)
                    elif btnName == 5:
                         globals()[btnName].setText("AOSHelp")
                         globals()[btnName].clicked.connect(self.helpWindow.show)
                         globals()[btnName].clicked.connect(self.helpWindow.activateWindow)
                    elif btnName == 6:
                         globals()[btnName].setText("Terminal")
                         globals()[btnName].clicked.connect(self.atermWindow.show)
                         globals()[btnName].clicked.connect(self.atermWindow.activateWindow)


                    buttonX += 120

               btnName += 1

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
                         msgBox(f"No app called \"{prgm}\" found in files/apps","ERROR!",QMessageBox.Critical,QMessageBox.Ok)
                    except Exception as err:
                         msgBox(f"Critical error in app \"{prgm}\": {err}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)

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
     QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
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
          
          if content[9] == "False" or content[9] == "":
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