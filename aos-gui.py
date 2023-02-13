#! /bin/python

#  █████╗  ██████╗ ███████╗       ██████╗ ██╗   ██╗██╗
# ██╔══██╗██╔═══██╗██╔════╝      ██╔════╝ ██║   ██║██║
# ███████║██║   ██║███████╗█████╗██║  ███╗██║   ██║██║
# ██╔══██║██║   ██║╚════██║╚════╝██║   ██║██║   ██║██║
# ██║  ██║╚██████╔╝███████║      ╚██████╔╝╚██████╔╝██║
# ╚═╝  ╚═╝ ╚═════╝ ╚══════╝       ╚═════╝  ╚═════╝ ╚═╝
# by nanobot567

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
     pipmain(["install","playsound==1.2.2"])
     pipmain(["install","psutil"])
     # pipmain(["install","PyQtWebEngine"])
     print("Done! Starting up...")

     from PyQt5.QtGui import *
     from PyQt5.QtWidgets import *
     from PyQt5.QtCore import *
     from PyQt5.QtPrintSupport import *
     import requests

from files.system import aoshelp,calc,cinstall,edit,fs,launcher,settings,splash, terminal
from files.system.setup import setupAOS
from files.apps.sdk.sdk import *

from time import sleep,strftime
import importlib
import sys
import os
import psutil

fontSize = 11
buttonFontSize = f"font-size:{fontSize}px"
buttonX = 20
buttonY = 40
buttonSpaceX = 20
buttonSpaceY = 40
buttonWidth = 100
buttonHeight = 50
buttonsShown = []
numShortcuts = 8
guiTheme = ""

sysApps = ["Settings","appLauncher","FileSystem","camelInstall","Edit","AOSHelp","Terminal","Calculator"]

kSeqs = []

class AOS(QMainWindow):
     def __init__(self):
          super(AOS, self).__init__()
          self.setContextMenuPolicy(Qt.ActionsContextMenu)

          global textcolor,bgcolor,ttextcolor,tbgcolor,btextcolor,bbgcolor, \
              windowcolor,buttonsShown,theme,username,password,kSeqs,fontSize, \
              buttonFontSize,guiTheme,clockMode,buttonWidth,buttonHeight, \
              buttonSpaceX,buttonSpaceY \

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
          windowcolor = themeColors[6]
          
          buttonsShown = content[8].split("|")

          guiTheme = content[10]

          clockMode = content[11]

          buttonWidth = int(content[12].split("|")[0])
          buttonHeight = int(content[12].split("|")[1])
          buttonSpaceX = int(content[12].split("|")[2])
          buttonSpaceY = int(content[12].split("|")[3])

          print("\nStarting up AOS-GUI, please wait...")
          print("Setting up system apps...")

          self.settingsWindow = settings.settingsWidget()
          self.fsWindow = fs.FsWindow()
          self.cInstWindow = cinstall.camelInstall()
          self.editWindow = edit.editApp()
          self.helpWindow = aoshelp.aoshelp()
          self.atermWindow = terminal.aterm()
          self.aLaunchWindow = launcher.launcher()
          self.calcWindow = calc.calculator()

          self.setWindowTitle("AOS-GUI")
          self.setWindowFlag(Qt.FramelessWindowHint)
          self.setGeometry(0,0,700,500)
          self.setStyleSheet(f"background-color: {bgcolor}; color: {textcolor};")
          print("Finalizing desktop...")
          self.setupMenuBar()
          self.setupButtons()
          self.setupShortcuts()
          print("Finished!")

     def updateDesktopFile(self):
          global numShortcuts
          f = open(getcwd().replace("\\","/")+"/files/system/data/user/desktop.aos","w")

          for i in range(8,numShortcuts):
               f.write(str(globals()["sc"+str(i)].text()))
               if i != numShortcuts-1:
                    f.write("|")

     def removeShortcut(self, prgm=""):
          global buttonX,buttonY,btextcolor,bbgcolor,buttonFontSize,buttonWidth,buttonHeight,buttonSpaceX,buttonSpaceY,numShortcuts,sysApps
          size = app.primaryScreen().size()
          ok = False

          if prgm == False:
               prgm,done = QInputDialog.getText(
               self, 'Remove Shortcut', 'Type the program you would like to remove the shortcut to. (Omit .py)', flags=Qt.Window | Qt.WindowStaysOnTopHint)
               ok = True
          
          if prgm.isspace() or prgm == "":
               pass
          else:
               for i in globals():
                    try:
                         if globals().get(i).text() == prgm:
                              if prgm not in sysApps:
                                   numShortcuts -= 1
                                   globals().get(i).hide()

                                   buttonX -= buttonWidth + buttonSpaceX

                                   if buttonX+buttonWidth >= size.width()-buttonSpaceX:
                                        buttonY -= buttonHeight+buttonSpaceY
                                        buttonX = buttonSpaceX
                                   break
                    except AttributeError:
                         pass
                    except TypeError:
                         pass

          if ok==True:
               self.updateDesktopFile()
          
     def createShortcut(self, prgm=""):
          # replace this with dropdown menu with apps using qwidget instead.
          global buttonX,buttonY,btextcolor,bbgcolor,buttonFontSize,buttonWidth,buttonHeight,buttonSpaceX,buttonSpaceY,numShortcuts
          size = app.primaryScreen().size()
          ok = False

          if prgm == False:
               prgm,done = QInputDialog.getText(
               self, 'Create Shortcut', 'Type the program you would like to make a shortcut to. (Omit .py)', flags=Qt.Window | Qt.WindowStaysOnTopHint)
               ok = True
          
          if prgm.isspace() or prgm == "":
               pass
          else:
               globals()["sc"+str(numShortcuts)] = DraggableButton(self)
               globals()["sc"+str(numShortcuts)].setGeometry(buttonX,buttonY,buttonWidth,buttonHeight)
               globals()["sc"+str(numShortcuts)].setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
               globals()["sc"+str(numShortcuts)].setCursor(Qt.CursorShape.PointingHandCursor)
               globals()["sc"+str(numShortcuts)].setText(prgm)
               globals()["sc"+str(numShortcuts)].clicked.connect(lambda: openApplication(prgm))
               globals()["sc"+str(numShortcuts)].show()

               self.repaint()

               numShortcuts += 1

               buttonX += buttonWidth + buttonSpaceX

               if buttonX+buttonWidth >= size.width()-buttonSpaceX:
                    buttonY += buttonHeight+buttonSpaceY
                    buttonX = buttonSpaceX

          if ok==True:
               self.updateDesktopFile()

     def setupButtons(self):
          global buttonX,buttonY,buttonSpaceX,buttonSpaceY

          btnName = 0

          buttonX = buttonSpaceX

          for i in buttonsShown:
               if i != "False":
                    globals()[btnName] = DraggableButton(self)
                    globals()[btnName].setGeometry(buttonX,buttonY,buttonWidth,buttonHeight)
                    globals()[btnName].setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
                    globals()[btnName].setCursor(Qt.CursorShape.PointingHandCursor)

                    match btnName:
                         case 0:
                              globals()[btnName].setText("Settings")
                              globals()[btnName].clicked.connect(self.settingsWindow.showNormal)
                              globals()[btnName].clicked.connect(self.settingsWindow.activateWindow)
                         case 1:
                              globals()[btnName].setText("appLauncher")
                              globals()[btnName].clicked.connect(self.aLaunchWindow.showNormal)
                              globals()[btnName].clicked.connect(self.aLaunchWindow.activateWindow)
                         case 2:
                              globals()[btnName].setText("FileSystem")
                              globals()[btnName].clicked.connect(self.fsWindow.showNormal)
                              globals()[btnName].clicked.connect(self.fsWindow.activateWindow)
                         case 3:
                              globals()[btnName].setText("camelInstall")
                              globals()[btnName].clicked.connect(self.cInstWindow.showNormal)
                              globals()[btnName].clicked.connect(self.cInstWindow.activateWindow)
                         case 4:
                              globals()[btnName].setText("Edit")
                              globals()[btnName].clicked.connect(self.editWindow.showNormal)
                              globals()[btnName].clicked.connect(self.editWindow.activateWindow)
                         case 5:
                              globals()[btnName].setText("AOSHelp")
                              globals()[btnName].clicked.connect(self.helpWindow.showNormal)
                              globals()[btnName].clicked.connect(self.helpWindow.activateWindow)
                         case 6:
                              globals()[btnName].setText("Terminal")
                              globals()[btnName].clicked.connect(self.atermWindow.showNormal)
                              globals()[btnName].clicked.connect(self.atermWindow.activateWindow)
                         case 7:
                              globals()[btnName].setText("Calculator")
                              globals()[btnName].clicked.connect(self.calcWindow.showNormal)
                              globals()[btnName].clicked.connect(self.calcWindow.activateWindow)
                    buttonX += buttonWidth + buttonSpaceX

                    # later release, make it so buttons linking to external apps possible.

               btnName += 1
          
          f = open(getcwd().replace("\\","/")+"/files/system/data/user/desktop.aos","r")
          desktopFile = f.read().split("|")
          f.close()

          for i in desktopFile:
               self.createShortcut(i)

     def restart(self):
          print("Restarting...")
          QCoreApplication.quit()
          QProcess.startDetached(sys.executable, sys.argv)

     def setupMenuBar(self):
          global timeMenu,batteryMenu,cpuUsageMenu,memoryMenu,menubarSegs
          menuBar = self.menuBar()
          menuBar.setStyleSheet(f"background-color: {tbgcolor}; color: {ttextcolor};")

          self.runAction = QAction("&Run...", self)
          self.setAction = QAction("&Settings", self)
          self.restartAction = QAction("&Restart", self)
          self.exitAction = QAction("&Exit", self)
          self.scAction = QAction("&Create Shortcut...", self)
          self.rscAction = QAction("&Remove Shortcut...", self)

          aosMenu = QMenu(f"&AOS - {username}", self)
          extrasMenu = QMenu(f"Extras", self)

          menuBar.addMenu(aosMenu)
          menuSeparator = menuBar.addMenu("|")
          menuSeparator.setEnabled(False)
          aosMenu.addAction(self.runAction)
          aosMenu.addAction(self.setAction)
          aosMenu.addAction(self.restartAction)
          aosMenu.addAction(self.exitAction)
          menuBar.addMenu(extrasMenu)
          extrasMenu.addAction(self.scAction)
          extrasMenu.addAction(self.rscAction)

          f = open("files/system/data/user/menubar.aos", "r")
          menubarSegs = f.read().split("|")

          timeMenu = QMenu(strftime('%H:%M:%S - /%m/%d/%Y'), self)
          timeMenu.setEnabled(False)
          batteryMenu = QMenu("100%", self)
          batteryMenu.setEnabled(False)
          cpuUsageMenu = QMenu("CPU: 0%", self)
          cpuUsageMenu.setEnabled(False)
          memoryMenu = QMenu("RAM: 0 MB", self)
          memoryMenu.setEnabled(False)

          for i in menubarSegs:
               match i:
                    case "Clock":
                         menuBar.addMenu("|").setEnabled(False)
                         menuBar.addMenu(timeMenu)
                    case "Battery":
                         menuBar.addMenu("|").setEnabled(False)
                         menuBar.addMenu(batteryMenu)
                    case "CPU Usage":
                         menuBar.addMenu("|").setEnabled(False)
                         menuBar.addMenu(cpuUsageMenu)
                    case "Available Memory":
                         menuBar.addMenu("|").setEnabled(False)
                         menuBar.addMenu(memoryMenu)

          f.close()


          self.runAction.triggered.connect(self.run)
          self.setAction.triggered.connect(self.settingsWindow.show)
          self.restartAction.triggered.connect(self.restart)
          self.exitAction.triggered.connect(QCoreApplication.quit)
          self.scAction.triggered.connect(self.createShortcut)
          self.rscAction.triggered.connect(self.removeShortcut)

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
               if prgm.lower().endswith(".py"):
                    prgm = "".join(prgm.split(".py")[:1])

               match prgm.lower():
                    case "fs" | "filesystem":
                         self.fsWindow.show()
                    case "editor" | "edit":
                         self.editWindow.show()
                    case "settings":
                         self.settingsWindow.show()
                    case "aoshelp" | "help":
                         self.helpWindow.show()
                    case "cinstall" | "camelinstall":
                         self.cInstWindow.show()
                    case "aterm" | "terminal":
                         self.atermWindow.show()
                    case "applauncher":
                         self.aLaunchWindow.show()
                    case "splash":
                         splashscreen.__init__()
                         splashscreen.show()
                    case "calc" | "calculator":
                         self.calcWindow.show()
                    case "about":
                         msgBox("AOS-GUI version "+version+", created by nanobot567 on GitHub. More information can be found in AOSHelp or the GitHub repository.","About")
                    case _:
                         openApplication(prgm)

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

     def showEvent(self, event):
          f = open("files/system/data/user/autorun.aos","r")
          for i in f.read().split("|"):
               if i:
                    if openApplication(i, silentFail=True) == -1:
                         match i:
                              case "aoshelp":
                                   self.helpWindow.show()
                              case "calc":
                                   self.calcWindow.show()
                              case "cinstall":
                                   self.cInstWindow.show()
                              case "edit":
                                   self.editWindow.show()
                              case "fs":
                                   self.fsWindow.show()
                              case "launcher":
                                   self.aLaunchWindow.show()
                              case "settings":
                                   self.settingsWindow.show()
                              case "terminal":
                                   self.atermWindow.show()
          super().showEvent(event)

if __name__ == '__main__':
     QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
     app = QApplication([])

     try:
          f = open("files/system/data/user/data.aos", "r")

          window = AOS()
          window.showFullScreen()

          content = f.read()
          content = content.split("\n")

          try:
               if content[13] == "True":
                    playsound(os.getcwd().replace("\\","/")+"/files/system/data/silence.wav")
                    playsound(os.getcwd().replace("\\","/")+"/files/system/data/AOS.wav")
          except:
               pass

          if content[1] != "":
               passwordInput = ""
               while passwordInput != content[1]:
                    passwordInput, z = QInputDialog.getText(window, "Password","Please enter your password.", QLineEdit.Normal, "")
          
          if content[9] == "False" or content[9] == "":
               splashscreen = splash.splashScreen()
               splashscreen.show()

          f.close()

          timer = QTimer()

          for i in menubarSegs:
               match i:
                    case "Clock":
                         if clockMode == "True":
                              timer.timeout.connect(lambda: timeMenu.setTitle(strftime('%H:%M:%S - %m/%d/%Y')))
                         else:
                              timer.timeout.connect(lambda: timeMenu.setTitle(strftime('%I:%M:%S - %m/%d/%Y')))
                    case "Battery":
                         timer.timeout.connect(lambda: batteryMenu.setTitle(str(psutil.sensors_battery().percent)+"%"))
                    case "CPU Usage":
                         timer.timeout.connect(lambda: cpuUsageMenu.setTitle("CPU: "+str(psutil.cpu_percent())+"%"))
                    case "Available Memory":
                         timer.timeout.connect(lambda: memoryMenu.setTitle("RAM: "+str(round(psutil.virtual_memory().available / 1000000))+" MB"))

          timer.start(1000)

          app.setStyle(guiTheme)

     except FileNotFoundError as  err:
          app.setStyle("Windows")
          window = setupAOS.installform()
          window.show()
     except Exception as e:
          print("ERR: " + str(e))

     try:
          if userSettings()[len(userSettings())-1] == "True":
               QGuiApplication.setPalette(getPalette())
     except (FileNotFoundError, NameError):
          pass

     # window = MainWindow()
     # app.setAttribute(Qt.WA_StyledBackground)
     exit(app.exec_())
