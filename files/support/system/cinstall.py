from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import listdir,path

from files.support.system.helpers.funcs import msgBox

class camelInstall(QWidget):

    def __init__(self):
        super(camelInstall, self).__init__()

        self.setFixedSize(660, 460)
        self.setWindowTitle("camelInstall")
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
        self.install.setGeometry(QRect(480, 70, 93, 28))
        self.install.setText("Install")
        self.install.clicked.connect(self.installApp)
        self.viewSource = QPushButton(self.database)
        self.viewSource.setObjectName(u"viewSource")
        self.viewSource.setGeometry(QRect(462, 110, 131, 28))
        self.viewSource.setText("View Source")
        self.viewSource.clicked.connect(self.viewSourceOfApp)
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

        nameItem = QTableWidgetItem()
        nameItem.setText("name")
        descItem = QTableWidgetItem()
        descItem.setText("description")
        verItem = QTableWidgetItem()
        verItem.setText("version")

        self.tableWidget.setColumnCount(3)

        self.tableWidget.setHorizontalHeaderItem(0, nameItem)
        self.tableWidget.setHorizontalHeaderItem(1, descItem)
        self.tableWidget.setHorizontalHeaderItem(2, verItem)

        self.dbTable.setColumnCount(3)
        self.dbTable.setHorizontalHeaderItem(0, nameItem)
        self.dbTable.setHorizontalHeaderItem(1, descItem)
        self.dbTable.setHorizontalHeaderItem(2, verItem)
        self.dbTable.setRowCount(1)
        self.dbTable.setItem(0,0,QTableWidgetItem("hello"))
        self.dbTable.setItem(0,1,QTableWidgetItem("hello"))
        self.dbTable.setItem(0,2,QTableWidgetItem("hello"))

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
                print(f"camelInstall couldn't find info for the app ({name}), getting info from package name...")
                self.tableWidget.setItem(row, 0, QTableWidgetItem(name))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(name))
                row += 1
            f.close()

    

    def installApp(self):
        msgBox(self.dbTable.item(self.dbTable.currentRow(),0).text(),"",0,QMessageBox.Ok)
    
    def searchForApp(self):
        pass

    def viewSourceOfApp(self):
        pass

    def areYouSure(self):
        try:
            retval = msgBox(f"Are you sure you want to uninstall '{self.tableWidget.item(self.tableWidget.currentRow(),0).text()}'?","Uninstall?",QMessageBox.Warning,QMessageBox.Yes|QMessageBox.No)
            if retval == 16384:
                self.doneUninstalling()

        except AttributeError:
            pass

    def doneUninstalling(self):
        msgBox(f"Uninstalled '{self.tableWidget.item(self.tableWidget.currentRow(),0).text()}'!","Uninstalled!",QMessageBox.Information,QMessageBox.Ok)

    # retranslateUi

