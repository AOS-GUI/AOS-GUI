from time import sleep
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import io

from os import listdir,path,getcwd,remove,makedirs
from shutil import rmtree

import requests

from files.apps.sdk.sdk import *

class camelInstall(QWidget):
    def __init__(self):
        super(camelInstall, self).__init__()

        self.setFixedSize(660, 460)
        self.setWindowTitle("AOS-GUI/cinstall")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.camel = QLabel(self)
        self.camel.setObjectName(u"camel")
        self.camel.setGeometry(QRect(530, 10, 121, 16))
        font = QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.camel.setFont(font)
        self.camel.setText(u"camelInstall")
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 640, 440))
        self.installed = QWidget()
        self.installed.setObjectName(u"installed")
        self.tableWidget = QTableWidget(self.installed)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(0, 0, 400, 411))
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.uninstall = QPushButton(self.installed)
        self.uninstall.setObjectName(u"uninstall")
        self.uninstall.setGeometry(QRect(450, 80, 141, 28))
        self.uninstall.setText(u"Uninstall...")
        self.uninstall.clicked.connect(self.areYouSure)
        self.runBtn = QPushButton(self.installed)
        self.runBtn.setObjectName(u"runBtn")
        self.runBtn.setGeometry(QRect(470, 120, 93, 28))
        self.runBtn.setText(u"Run")
        self.runBtn.clicked.connect(self.runApp)
        self.tabWidget.addTab(self.installed, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.installed), u"installed")
        self.database = QWidget()
        self.database.setObjectName(u"database")
        self.dbTable = QTableWidget(self.database)
        self.dbTable.setObjectName(u"dbTable")
        self.dbTable.setGeometry(QRect(0, 0, 400, 411))
        self.dbTable.setAutoScroll(False)
        self.dbTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dbTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.dbTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.install = QPushButton(self.database)
        self.install.setObjectName(u"install")
        self.install.setGeometry(QRect(480, 70, 85, 28))
        self.install.setText("Install")
        self.install.clicked.connect(self.installApp)
        # self.viewSource = QPushButton(self.database)
        # self.viewSource.setObjectName(u"viewSource")
        # self.viewSource.setGeometry(QRect(462, 110, 131, 28))
        # self.viewSource.setText("View Source")
        # self.viewSource.clicked.connect(self.viewSourceOfApp)
        self.search = QPushButton(self.database)
        self.search.setObjectName(u"search")
        self.search.setGeometry(QRect(560, 220, 61, 28))
        self.search.setText("Search")
        self.search.clicked.connect(self.searchForApp)
        self.searchEdit = QLineEdit(self.database)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setGeometry(QRect(420, 220, 141, 28))
        self.tabWidget.addTab(self.database, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.database), u"app database")

        self.status = QLabel(self.database)
        self.status.setObjectName(u"status")
        self.status.setGeometry(QRect(400, 320, 230, 20))
        self.status.setText(u"")
        self.status.setAlignment(Qt.AlignCenter)

        nameItem = QTableWidgetItem()
        nameItem.setText("name")
        descItem = QTableWidgetItem()
        descItem.setText("description")
        verItem = QTableWidgetItem()
        verItem.setText("version")
        urlItem = QTableWidgetItem()
        urlItem.setText("url")

        self.tableWidget.setColumnCount(3)

        self.tableWidget.setHorizontalHeaderItem(0, nameItem)
        self.tableWidget.setHorizontalHeaderItem(1, descItem)
        self.tableWidget.setHorizontalHeaderItem(2, verItem)

        self.dbTable.setColumnCount(4)
        self.dbTable.setHorizontalHeaderItem(0, nameItem)
        self.dbTable.setHorizontalHeaderItem(1, descItem)
        self.dbTable.setHorizontalHeaderItem(2, verItem)
        self.dbTable.setHorizontalHeaderItem(3, urlItem)
        self.dbTable.setRowCount(1)

        self.refreshApps()

    def refreshApps(self):
        filepath = "files/apps/"
        files = []
        row = 0

        for file in listdir(filepath):
            if path.isfile(path.join(filepath, file)):
                files.append(file)

        self.tableWidget.setRowCount(len(files))

        for name in sorted(files):
            f = open(f"{filepath}{name}","r")

            try:
                content = f.read()
                content = content.split("#~")
                pkginfo = content[1].split("|")
                pkginfo[2] = pkginfo[2].split("\n")[0]

                self.tableWidget.setItem(row, 0, QTableWidgetItem(pkginfo[0]))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(pkginfo[1]))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(pkginfo[2]))
                row += 1
            except:
                print(f"[WARN] camelInstall couldn't find info for the app ({name}), getting info from package name")
                self.tableWidget.setItem(row, 0, QTableWidgetItem(name))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(name))
                row += 1
            f.close()
        

        try:
            r = requests.get("https://raw.githubusercontent.com/Nanobot567/cInstall/main/dl/appList.txt",timeout=5)
            filesOnline = r.text.splitlines(False)
        except:
            print("[WARN] It seems like you aren't connected to the internet, not gathering camelInstall list for now.")
            filesOnline = ["No internet!|No internet!|No internet!|No internet!"]
        filesOnlineNames = []
        filesOnlineDescs = []
        filesOnlineVers = []
        filesOnlineUrls = []
        i = 0

        for files in filesOnline:
            filesOnlineNames.append(filesOnline[i].split("|")[0])
            filesOnlineDescs.append(filesOnline[i].split("|")[1])
            filesOnlineVers.append(filesOnline[i].split("|")[2])
            filesOnlineUrls.append(filesOnline[i].split("|")[3])
            i+=1


        self.dbTable.setRowCount(len(filesOnlineNames))
        i = 0

        for name in filesOnlineNames:
            self.dbTable.setItem(i, 0, QTableWidgetItem(name))
            i += 1
        i = 0
        for desc in filesOnlineDescs:
            self.dbTable.setItem(i, 1, QTableWidgetItem(desc))
            i += 1
        i = 0
        for ver in filesOnlineVers:
            self.dbTable.setItem(i, 2, QTableWidgetItem(ver))
            i += 1
        i = 0
        for url in filesOnlineUrls:
            self.dbTable.setItem(i, 3, QTableWidgetItem(url))
            i += 1
        i = 0

    def runApp(self):
        prgm = self.tableWidget.item(self.tableWidget.currentRow(),0).text().split(".py")[0]
        openApplication(prgm)

    def openWriteDirs(self,dir,openmode):
        makedirs(path.dirname(dir), exist_ok=True)
        return open(dir, openmode)

    def installApp(self):
        try:
            val = 0
            text = self.dbTable.item(self.dbTable.currentRow(),0).text()
            ret = msgBox("Are you sure you want to install \""+text+"\"?","Install?",QMessageBox.Question,QMessageBox.Yes|QMessageBox.No)
            if ret == 16384:
                urls = self.dbTable.item(self.dbTable.currentRow(),3).text()
                for url in urls.split(";"):
                    self.status.setText("download: "+url.split("/")[-1])
                    self.update()
                    self.repaint()

                    newUrl = ""
                    if url.startswith("db/"):
                        url = url.split("db/")[1]
                        url = "https://aos-gui.github.io/cInstall/dl/"+url

                        r = requests.get(url)
                        url = url.split("/")[5:]

                        for x in url:
                            newUrl += "/"+x

                    elif url.startswith("assets/"):
                        url = url.split("assets/")[1]
                        url = "https://aos-gui.github.io/cInstall/dl/assets/"+self.dbTable.item(self.dbTable.currentRow(),0).text().split(".py")[0]+"/"+url

                        r = requests.get(url)
                        url = url.split("/")[5:]

                        for x in url:
                            newUrl += "/"+x
                    else:
                        newUrl = url
                        print(url)
                        try:
                            r = requests.get(url)
                        except requests.exceptions.MissingSchema:
                            pass
                    
                    if newUrl != "":
                        f = self.openWriteDirs(getcwd().replace("\\","/")+"/files/apps/"+newUrl,"wb")
                    
                        f.write(r.content)
                        f.close()

                    self.status.setText("downloaded: "+newUrl.split("/")[-1])
                    self.update()
                    self.repaint()
                
                self.status.setText("installed: "+self.dbTable.item(self.dbTable.currentRow(),0).text())
                msgBox(f"Installed \"{self.dbTable.item(self.dbTable.currentRow(),0).text()}\"!","Installed!",QMessageBox.Information,QMessageBox.Ok)
                self.refreshApps()
            self.status.setText("")
        except AttributeError:
            pass

    def searchForApp(self):
        try:
            for i in range(self.dbTable.rowCount()):
                if self.searchEdit.text() in self.dbTable.item(i,0).text() or self.searchEdit.text() in self.dbTable.item(i,1).text():
                    self.dbTable.selectRow(i)
        except AttributeError:
            pass

    def viewSourceOfApp(self):
        try:
            url = self.dbTable.item(self.dbTable.currentRow(),3).text()
            if url.startswith("db/"):
                url = url.split("db/")[1]
                url = "https://raw.githubusercontent.com/AOS-GUI/cInstall/main/dl/"+url
            r = requests.get(url)
            msgBox(r.text,"Source")
        except AttributeError:
            pass

    def areYouSure(self):
        try:
            retval = msgBox(f"Are you sure you want to uninstall '{self.tableWidget.item(self.tableWidget.currentRow(),0).text()}'?","Uninstall?",QMessageBox.Warning,QMessageBox.Yes|QMessageBox.No)
            if retval == 16384:
                self.doneUninstalling()

        except AttributeError:
            pass

    def doneUninstalling(self):
        item = self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        if not item.endswith(".py"):
            item = item+".py"
        remove(getcwd().replace("\\","/")+"/files/apps/"+item)

        item = item.split(".py")[0]

        try:
            rmtree(getcwd().replace("\\","/")+"/files/apps/assets/"+item+"/")
        except Exception as e:
            print(e)

        msgBox(f"Uninstalled '{item}'!","Uninstalled!",QMessageBox.Information,QMessageBox.Ok)
        self.refreshApps()
