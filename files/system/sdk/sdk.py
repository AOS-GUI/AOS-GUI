from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import getcwd
from sys import executable,argv
import importlib

f = open(getcwd().replace("\\","/")+"/files/system/data/version", "r")
version = f.read()

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

def restart():
    print("Restarting...")
    QCoreApplication.quit()
    # print(sys.executable)
    QProcess.startDetached(executable, argv)

def openApplication(app, path="files/apps/"):
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
    except ModuleNotFoundError:
        msgBox(f"No app called \"{app}\" found in {path}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)
    except Exception as err:
        msgBox(f"Critical error in app \"{app}\": {err}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)

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

def aosVersion():
    return version

def userSettings():
    f = open("files/system/data/user/data.aos","r")
    content = f.read()
    content = content.split("\n")
    f.close()

    content[1] = "NO PERMS"

    return content

def userTheme():
    f = open("files/system/data/user/data.aos","r")
    content = f.read()
    content = content.split("\n")
    f.close()

    try:
        themeText = open("files/system/data/user/themes/"+content[2]+".theme","r")
    except FileNotFoundError:
        print("!! WARNING: Theme "+content[2]+" not found, going to default-dark...")
        themeText = open("files/system/data/user/themes/default-dark.theme","r")

    themeTextStr = themeText.read()
    themeColors = themeTextStr.split("\n")

    themeText.close()

    return themeColors