from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import getcwd,remove,makedirs,path
from sys import executable,argv,modules
from shutil import rmtree
import importlib
import configparser
import requests
import platform
from random import choice
import re

importedModules = {}

f = open(getcwd().replace("\\","/")+"/files/system/data/version", "r")
version = f.read()
f.close()

class Camel():
    def __init__(self):
        self.updated = False
        self.pkgnames = []
        self.pkgdescs = []
        self.pkgvers = []
        self.pkgurls = []

    def update(self):
        self.pkgnames = []
        self.pkgdescs = []
        self.pkgvers = []
        self.pkgurls = []

        try:
            r = requests.get("https://raw.githubusercontent.com/AOS-GUI/cInstall/main/dl/appList.txt",timeout=5)
            filesOnline = r.text.splitlines(False)
            i = 0

            for files in filesOnline:
                self.pkgnames.append(filesOnline[i].split("|")[0])
                self.pkgdescs.append(filesOnline[i].split("|")[1])
                self.pkgvers.append(filesOnline[i].split("|")[2])
                self.pkgurls.append(filesOnline[i].split("|")[3])
                i+=1
            self.updated = True

            return 0,[self.pkgnames,self.pkgdescs,self.pkgvers,self.pkgurls]
        except Exception as e:
            self.updated = True
            return -1,e

    def install(self, package):
        urls = self.pkgurls[self.pkgnames.index(package)]

        try:
            for url in urls.split(";"):
                newUrl = ""
                if url.startswith("db/"):
                    url = url.split("db/")[1]
                    url = "https://raw.githubusercontent.com/AOS-GUI/cInstall/main/dl/"+url

                    r = requests.get(url)
                    url = url.split("/")[7:]

                    for x in url:
                        newUrl += "/"+x

                elif url.startswith("assets/"):
                    url = url.split("assets/")[1]
                    url = "https://raw.githubusercontent.com/AOS-GUI/cInstall/main/dl/assets/"+package.split(".py")[0]+"/"+url

                    r = requests.get(url)
                    url = url.split("/")[7:]

                    for x in url:
                        newUrl += "/"+x
                else:
                    newUrl = url
                    try:
                        r = requests.get(url)
                    except requests.exceptions.MissingSchema:
                        pass
                
                if newUrl != "":
                    makedirs(path.dirname(getAOSdir()+"/apps/"+newUrl), exist_ok=True)
                    f = open(getAOSdir()+"/apps/"+newUrl,"wb")
                
                    f.write(r.content)
                    f.close()
            return 0,None
        except Exception as e:
            return -1,e

    def uninstall(self, package):
        item = package
        try:
            if not item.endswith(".py"):
                item = item+".py"
            remove(getAOSdir()+"/apps/"+item)

            item = item.split(".py")[0]

            try:
                rmtree(getAOSdir()+"/apps/assets/"+item+"/")
            except:
                pass
            return 0,None
        except Exception as e:
            return -1,str(e)

    def getNames(self):
        return self.pkgnames
    def getDescs(self):
        return self.pkgdescs
    def getVersions(self):
        return self.pkgvers
    def getURLs(self):
        return self.pkgurls
    def getAppInfo(self):
        return self.pkgnames, self.pkgdescs, self.pkgvers, self.pkgurls
    def isUpdated(self):
        return self.updated

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

def openApplication(app, path="files/apps/"):
    global importedModules
    if app.endswith(".py"):
        app = app.split(".py")[0]
        
    try:
        f = open(path+app+".py", "r")
        if f.read().find("QMainWindow") != -1:
            QProcess.startDetached(executable, [path+app+".py"])
        else:
            if path.replace("/",".")+app in importedModules:
                importlib.reload(importedModules[path.replace("/",".")+app])
            else:
                modulePrgm = importlib.import_module(path.replace("/",".")+app)
                importedModules[path.replace("/",".")+app] = modulePrgm
            # TODO: make it so aos default apps can be run
        f.close()
        return 0,None
    except ModuleNotFoundError as err: # TODO: change so instead of msgBox it's the str
        # if silentFail == False:
        #     msgBox(f"No app called \"{app}\" found in {path}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)
        return -1,err
    except Exception as err:
        # if silentFail == False:
        #     msgBox(f"Critical error in app \"{app}\": {err}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)
        return -1,err

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

def promptBox(text, title="AOS-GUI", parent=None, x=None, y=None, mode="text", args=None):
    dialog = QInputDialog()
    dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Popup)

    if x != None and y != None:
        dialog.move(x,y)

    output = None
    done = None
    if mode == "text":
        output, done = dialog.getText(None, title, text)
    elif mode == "int":
        output, done = dialog.getInt(None, title, text)
    elif mode == "double":
        output, done = dialog.getDouble(None, title, text)
    elif mode == "item":
        output, done = dialog.getItem(None, title, text, args)

    if done:
        return output
    return -1

def getPalette():
    theme,ret = getTheme()

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

def getVersion():
    return version

def getSettings():
    config = configparser.ConfigParser()
    config.read("files/system/data/user/data.aos")

    content = config

    return content

def getTheme():
    ret = 0
    config = configparser.ConfigParser()
    config.read("files/system/data/user/data.aos")

    try:
        themeText = open("files/system/data/user/themes/"+config["theme"]["name"]+".theme","r")
    except FileNotFoundError:
        ret = -1
        themeText = open("files/system/data/user/themes/default-dark.theme","r")

    themeTextStr = themeText.read()
    themeColors = themeTextStr.split("\n")

    themeText.close()

    return themeColors, ret

def toBool(str):
    if str == "True":
        return True
    else:
        return False

def _cmpstr(substr1, substr2):
    if (substr1 > substr2):
        return 1
    elif(substr1 < substr2):
        return -1
    return 0

def compareVersion(v1, v2):
    s1 = v1.split("[.]")
    s2 = v2.split("[.]")
    lenV1 = len(s1)
    lenV2 = len(s2)
    i = 0
    j = 0

    while (i < lenV1 or j < lenV2):
        x = ""
        y = ""
        if (i < lenV1):
            if (s1[i][0] == '0'):
                leng = len(s1[i])
                k = 0
                while (k < leng and s1[i][k] == '0'):
                    k += 1
                x += s1[i][k:]
            else:
                x += s1[i]
        if (j < lenV2):
            if (s2[i][0] == '0'):
                leng = len(s2[i])
                k = 0
                while (k < leng and s2[i][k] == '0'):
                    k += 1
                y += s2[i][k:]
            else:
                y = s2[i]

        res = _cmpstr(x, y)
        if (res != 0):
            return res
        i += 1
        j += 1

    return 0

def getSplashText(withHTML=False):
    f = open("files/system/data/splashes")
    splashTexts = f.readlines()
    f.close()

    text = choice(splashTexts).strip()

    if withHTML == True:
        return text
    else:
        return re.sub("<[^>]*>","",text)