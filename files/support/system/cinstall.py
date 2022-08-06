from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import listdir,path

class camelInstall(QWidget):

    def __init__(self):
        super(camelInstall, self).__init__()

        self.setFixedSize(660, 460)
        self.setWindowTitle("camelInstall")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.font = QFont()
        self.font.setPointSize(12)
        self.font.setItalic(True)
        self.camel = QLabel(self)
        self.camel.setText("camelInstall")
        self.camel.setObjectName(u"label")
        self.camel.setGeometry(QRect(530, 10, 111, 16))
        self.camel.setFont(self.font)

        self.tab = QWidget()
        self.tab.setObjectName(u"tab")

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 640, 440))

        self.notyet = QLabel(self.tab)
        self.notyet.setObjectName(u"label_2")
        self.notyet.setGeometry(QRect(80, 140, 481, 101))
        self.notyet.setWordWrap(True)
        self.notyet.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">not implemented yet! check back when a new AOS version is released!</span></p></body></html>")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "installed")
        self.tabWidget.addTab(self.tab, "app database")

        self.tableWidget = QTableWidget(self.tab_2)
        self.tableWidget.setGeometry(QRect(0, 0, 397, 411))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.uninstall = QPushButton(self.tab_2)
        self.uninstall.setText("Uninstall...")
        self.uninstall.setGeometry(QRect(450, 80, 141, 28))
        self.uninstall.clicked.connect(self.areYouSure)

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

    def areYouSure(self):
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Are you sure you want to uninstall '{self.tableWidget.item(self.tableWidget.currentRow(),0).text()}'?")
            msg.setWindowTitle("Uninstall?")
            msg.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
            msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            retval = msg.exec_()

            if retval == 16384:
                self.doneUninstalling()

        except AttributeError:
            pass

    def doneUninstalling(self):
        thing = QMessageBox()
        thing.setIcon(QMessageBox.Information)
        thing.setText(f"Uninstalled '{self.tableWidget.item(self.tableWidget.currentRow(),0).text()}'!")
        thing.setWindowTitle("Uninstalled!")
        thing.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        thing.setStandardButtons(QMessageBox.Ok)
        retval = thing.exec_()

    # retranslateUi

