#  █████╗  ██████╗ ███████╗       ██████╗ ██╗   ██╗██╗
# ██╔══██╗██╔═══██╗██╔════╝      ██╔════╝ ██║   ██║██║
# ███████║██║   ██║███████╗█████╗██║  ███╗██║   ██║██║
# ██╔══██║██║   ██║╚════██║╚════╝██║   ██║██║   ██║██║
# ██║  ██║╚██████╔╝███████║      ╚██████╔╝╚██████╔╝██║
# ╚═╝  ╚═╝ ╚═════╝ ╚══════╝       ╚═════╝  ╚═════╝ ╚═╝

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

try:
     from PyQt5.QtGui import *
     from PyQt5.QtWidgets import *
     from PyQt5.QtCore import *
     from PyQt5.QtPrintSupport import *
     import requests
     from playsound import playsound
except:
     print("Installing AOS-GUI requirements...")
     pipmain(["install","PyQt5"])
     pipmain(["install","requests"])
     pipmain(["install","playsound"])
     # pipmain(["install","PyQtWebEngine"])
     print("Done! Starting up...")

     from PyQt5.QtGui import *
     from PyQt5.QtWidgets import *
     from PyQt5.QtCore import *
     from PyQt5.QtPrintSupport import *
     import requests

from files.system.apps import *
from files.system.setup import setupAOS
from files.system.sdk.sdk import *

from time import sleep,strftime
import importlib
import sys
import os

fontSize = 11
buttonFontSize = f"font-size:{fontSize}px"
buttonX = 20
buttonY = 40
buttonsShown = []
guiTheme = ""

kSeqs = []

def launchExtApp(prgm):
     modulePrgm = importlib.import_module("files.apps."+prgm)
     importlib.reload(modulePrgm)

class AOS(QMainWindow):
     def __init__(self):
          size = app.primaryScreen().size()
          super(AOS, self).__init__()
          global textcolor,bgcolor,ttextcolor,tbgcolor,btextcolor,bbgcolor,buttonsShown,theme,username,password,kSeqs,fontSize,buttonFontSize,guiTheme,clockMode

          f = open("files/system/data/user/data.aos","r")
          content = f.read()
          content = content.split("\n")
          f.close()


          themeColors = userTheme()

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

          guiTheme = content[10]

          clockMode = content[11]

          print("\nStarting up AOS-GUI, please wait...")
          print("Setting up system apps...")

          self.settingsWindow = settingsWidget()
          self.fsWindow = FsWindow()
          self.cInstWindow = camelInstall()
          self.editWindow = editApp()
          self.helpWindow = aoshelp()
          self.atermWindow = aterm()
          self.aLaunchWindow = launcher()
          self.calcWindow = calculator()

          self.setWindowTitle("AOS-GUI")
          # remove title bar
          self.setWindowFlag(Qt.FramelessWindowHint)
          self.setGeometry(0,0,700,500)
          self.setStyleSheet(f"background-color: {bgcolor}; color: {textcolor};")
          print("Finalizing desktop...")
          self.setupMenuBar()
          self.setupButtons()
          self.setupShortcuts()
          print("Finished!")

     def setupButtons(self):
          global buttonX
          global buttonY

          btnName = 0

          for i in buttonsShown:
               if i != "False":
                    globals()[btnName] = DraggableButton(self)
                    globals()[btnName].setGeometry(buttonX,buttonY,100,50)
                    globals()[btnName].setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
                    globals()[btnName].setCursor(Qt.CursorShape.PointingHandCursor)

                    if btnName == 0:
                         globals()[btnName].setText("Settings")
                         globals()[btnName].clicked.connect(self.settingsWindow.show)
                         globals()[btnName].clicked.connect(self.settingsWindow.activateWindow)
                    elif btnName == 1:
                         globals()[btnName].setText("appLauncher")
                         globals()[btnName].clicked.connect(self.aLaunchWindow.show)
                         globals()[btnName].clicked.connect(self.aLaunchWindow.activateWindow)
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
                    elif btnName == 7:
                         globals()[btnName].setText("Calculator")
                         globals()[btnName].clicked.connect(self.calcWindow.show)
                         globals()[btnName].clicked.connect(self.calcWindow.activateWindow)
                    buttonX += 120

                    # later release, make it so buttons linking to external apps possible.

               btnName += 1

     def restart(self):
          print("Restarting...")
          QCoreApplication.quit()
          QProcess.startDetached(sys.executable, sys.argv)

     def setupMenuBar(self):
          global timeMenu
          menuBar = self.menuBar()

          menuBar.setStyleSheet(f"background-color: {tbgcolor}; color: {ttextcolor};")
          # cinstall.window = cinstall.Ui_camelInstaller()

          self.runAction = QAction("&Run...", self)
          # self.cInstAction = QAction("&camelInstall", self)
          self.setAction = QAction("&Settings", self)
          self.restartAction = QAction("&Restart", self)
          self.exitAction = QAction("&Exit", self)

          aosMenu = QMenu(f"&AOS - {username}", self)
          timeMenu = QMenu(strftime('%H:%M:%S - /%m/%d/%Y'), self)

          menuBar.addMenu(aosMenu)
          menuSeparator = menuBar.addMenu("|")
          menuSeparator.setEnabled(False)
          menuBar.addMenu(timeMenu)
          aosMenu.addAction(self.runAction)
          # aosMenu.addAction(self.cInstAction)
          aosMenu.addAction(self.setAction)
          aosMenu.addAction(self.restartAction)
          aosMenu.addAction(self.exitAction)
          timeMenu.setEnabled(False)

          self.runAction.triggered.connect(self.run)
          # self.cInstAction.triggered.connect(cinstall.window.show)
          self.setAction.triggered.connect(self.settingsWindow.show)
          self.restartAction.triggered.connect(self.restart)
          self.exitAction.triggered.connect(self.close)

     def rndr(self):
          rndr,check = QFileDialog.getOpenFileName(None, "Open a .rndr", "", "Renderable file (*.rndr);;All Files (*)")
          if check:
               print(rndr)

     def run(self):
          prgm,done = QInputDialog.getText(
             self, 'Run', 'Type the program you would like to run (.py extension not needed)', flags=Qt.Window | Qt.WindowStaysOnTopHint)
          
          if prgm.isspace() or prgm == "":
               pass
          else:
               if prgm.lower() == "fs":
                    self.fsWindow.show()
               elif prgm.lower() == "editor":
                    self.editWindow.show()
               elif prgm.lower() == "settings":
                    self.settingsWindow.show()
               elif prgm.lower() == "aoshelp":
                    self.helpWindow.show()
               elif prgm.lower() == "cinstall" or prgm.lower() == "camelinstall":
                    self.cInstWindow.show()
               elif prgm.lower() == "aterm" or prgm.lower() == "terminal":
                    self.atermWindow.show()
               elif prgm.lower() == "applauncher":
                    self.aLaunchWindow.show()
               elif prgm.lower() == "splash":
                    splashscreen.__init__()
                    splashscreen.show()
               elif prgm.lower() == "calc":
                    self.calcWindow.show()
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
          self.setSC.activated.connect(self.settingsWindow.show)
          self.helpSC.activated.connect(self.helpWindow.show)

if __name__ == '__main__':
     QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
     app = QApplication([])

     try:
          f = open("files/system/data/user/data.aos", "r")
          window = AOS()
          window.showFullScreen()

          try:
               playsound(os.getcwd().replace("\\","/")+"/files/system/data/silence.wav")
               playsound(os.getcwd().replace("\\","/")+"/files/system/data/AOS.wav")
          except:
               pass

          content = f.read()
          content = content.split("\n")
          if content[1] != "":
               passwordInput = ""
               while passwordInput != content[1]:
                    passwordInput, z = QInputDialog.getText(window, "Password","Please enter your password:", QLineEdit.Normal, "")
          
          if content[9] == "False" or content[9] == "":
               splashscreen = splashScreen()
               splashscreen.show()

          f.close()

          timer = QTimer()
          if clockMode == "True":
               timer.timeout.connect(lambda: timeMenu.setTitle(strftime('%H:%M:%S - %m/%d/%Y')))
          else:
               timer.timeout.connect(lambda: timeMenu.setTitle(strftime('%I:%M:%S - %m/%d/%Y')))
          timer.start(1000)
          app.setStyle(guiTheme)
          
     except Exception as e:
          if not str(e).startswith("[Errno 2] No such file or directory: 'files/system/data/user/data.aos'"):
               print("ERR: "+e)
          else:
               window = setupAOS.installform()
               window.show()

     # window = MainWindow()
     # app.setAttribute(Qt.WA_StyledBackground)
     exit(app.exec_())