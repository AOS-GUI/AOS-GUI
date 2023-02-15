from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import getcwd
from sys import executable,argv
import importlib
import configparser

f = open(getcwd().replace("\\","/")+"/files/system/data/version", "r")
version = f.read()
f.close()

class DraggableButton(QPushButton):
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DraggableButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(DraggableButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DraggableButton, self).mouseReleaseEvent(event)

def getAOSdir():
    return getcwd().replace("\\","/")+"/files/"

def restart():
    print("Restarting...")
    QCoreApplication.quit()
    # print(sys.executable)
    QProcess.startDetached(executable, argv)

def openApplication(app, path="files/apps/", silentFail=False):
    if app.endswith(".py"):
        app = app.split(".py")[0]
        
    try:
        f = open(path+app+".py", "r")
        if f.read().find("QMainWindow") != -1:
            QProcess.startDetached(executable, [path+app+".py"])
        else:
            modulePrgm = importlib.import_module(path.replace("/",".")+app)
            importlib.reload(modulePrgm)
        f.close()
        return 1
    except ModuleNotFoundError:
        if silentFail == False:
            msgBox(f"No app called \"{app}\" found in {path}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)
        return -1
    except Exception as err:
        if silentFail == False:
            msgBox(f"Critical error in app \"{app}\": {err}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)
        return -1

def msgBox(text, title="AOS-GUI", icon=QMessageBox.Information, buttons=QMessageBox.Ok, x=None,y=None):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(str(text))
    msg.setWindowTitle(title)
    msg.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
    msg.setStandardButtons(buttons)
    if x != None and y != None:
        msg.move(x,y)
    retval = msg.exec_()

    return retval

def getPalette():
    theme = userTheme()

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(theme[6]))
    palette.setColor(QPalette.WindowText, QColor(theme[0]))
    palette.setColor(QPalette.Base, QColor(theme[1]))
    palette.setColor(QPalette.AlternateBase, QColor(theme[6]))
    palette.setColor(QPalette.ToolTipBase, QColor(theme[1]))
    palette.setColor(QPalette.ToolTipText, QColor(theme[0]))
    palette.setColor(QPalette.Text, QColor(theme[0]))
    palette.setColor(QPalette.Button, QColor(theme[1]))
    palette.setColor(QPalette.ButtonText, QColor(theme[5]))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(theme[4]))
    palette.setColor(QPalette.HighlightedText, QColor(theme[0]))

    return palette

def aosVersion():
    return version

def userSettings():
    f = open("files/system/data/user/data.aos","r")
    content = f.read()
    content = content.split("\n")
    f.close()

    return content

def userTheme():
    config = configparser.ConfigParser()
    config.read("files/system/data/user/data.aos")

    try:
        themeText = open("files/system/data/user/themes/"+config["theme"]["name"]+".theme","r")
    except FileNotFoundError:
        print("!! WARNING: Theme "+config["theme"]["name"]+" not found, using default-dark...")
        themeText = open("files/system/data/user/themes/default-dark.theme","r")

    themeTextStr = themeText.read()
    themeColors = themeTextStr.split("\n")

    themeText.close()

    return themeColors

def toBool(str):
     if str == "True":
          return True
     else:
          return False