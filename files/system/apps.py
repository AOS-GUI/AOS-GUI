# before you yell at me for not splitting up the AOS apps, i did this because it looks better in vscode and
# it's easier to import an app this way


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import listdir,path,getcwd,remove,rmdir,mkdir
import importlib
from time import sleep
import requests
from shutil import rmtree
from random import choice
from playsound import playsound

from files.system.sdk.sdk import msgBox,userSettings

# -- FOR AOSHELP -- #

f = open("MDs/manual.md")
text = f.read()
f.close()

# -- FOR ATERM -- #
dir = "/home"
terminalVer = 1.0
helpText = {"help":"aos help (syntax: help {command})",
            "clear":"clears the screen (syntax: clear)",
            "echo":"echoes text (syntax: echo [text])",
            "rm":"removes a file (syntax: rm [path from /])",
            "dir":"lists the files and directories inside a directory (syntax: dir [path] {-notypes})",
            "read":"reads a file's contents (syntax: read [file])",
            "script":"runs a script (syntax: script [file] {-v | -verbose})",
            "ver":"shows system and terminal version",
            "aterm":"restarts aterm (syntax: aterm)",
            "beep":"plays the current AOS startup sound (syntax: beep)"}

# -- FOR CALC -- #

num = 0
waitingForNum = False

# -- FOR EDITOR -- #
filePath = ""
currentlyOpenFile = "Untitled"
currentlyOpenFileName = "Untitled"
originalText = ""

# -- FOR SPLASH -- #

f = open("files/system/data/splashes")
splashTexts = f.readlines()
f.close()

f = open("files/system/data/version","r")
version = f.read()
f.close()

class aoshelp(QWidget):
    def __init__(self):
        super(aoshelp, self).__init__()
        self.setFixedSize(500, 500)
        self.setWindowTitle("AOS-GUI/help")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.helpText = QTextEdit(self)
        self.helpText.setGeometry(QRect(0, 0, 500, 500))
        self.helpText.setReadOnly(True)

        self.helpText.setMarkdown(text)

class launcher(QWidget):
    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        super(launcher, self).__init__()

        self.setFixedSize(400, 300)
        self.setWindowTitle(u"appLauncher")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.appList = QListWidget(self)
        self.appList.setObjectName(u"appList")
        self.appList.setGeometry(QRect(0, 0, 401, 261))
        self.launchButton = QPushButton(self)
        self.launchButton.setObjectName(u"launchButton")
        self.launchButton.setGeometry(QRect(100, 270, 81, 23))
        self.launchButton.setText(u"Launch App")
        self.launchButton.clicked.connect(self.launchExtApp)
        self.refreshButton = QPushButton(self)
        self.refreshButton.setObjectName(u"refreshButton")
        self.refreshButton.setGeometry(QRect(220, 270, 75, 23))
        self.refreshButton.setText(u"Refresh")
        self.refreshButton.clicked.connect(self.grabExtApps)

        self.grabExtApps()

    def launchExtApp(self):
        prgm = self.appList.currentItem().text().split(".py")[0]
        try:
            modulePrgm = importlib.import_module("files.apps."+prgm)
            importlib.reload(modulePrgm)
        except ModuleNotFoundError:
                msgBox(f"No app called \"{prgm}\" found in files/apps","ERROR!",QMessageBox.Critical,QMessageBox.Ok)
        except Exception as err:
                msgBox(f"Critical error in app \"{prgm}\": {err}","ERROR!",QMessageBox.Critical,QMessageBox.Ok)

    def grabExtApps(self):
        self.appList.clear()
        for file in listdir("files/apps/"):
            if path.isfile(path.join("files/apps/", file)):
                self.appList.addItem(QListWidgetItem(file))

class aterm(QWidget):
    def __init__(self):
        super(aterm, self).__init__()
        self.setWindowTitle("AOS-GUI/aterm")
        self.setFixedSize(620, 440)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 400, 521, 31))
        self.lineEdit.setStyleSheet(u"background-color: black; color: white; \n"
"font: 8pt \"Consolas\";")
        self.lineEdit.returnPressed.connect(self.doCommand)

        self.listWidget = QListWidget(self)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 10, 601, 381))
        self.listWidget.setStyleSheet(u"font: 8pt \"Consolas\"; background-color:black; color: white;")
        self.listWidget.setAutoScroll(False)
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.go = QPushButton(self)
        self.go.setObjectName(u"pushButton")
        self.go.setGeometry(QRect(540, 400, 71, 31))
        self.go.setText("Enter")
        self.go.clicked.connect(self.doCommand)


        self.echo("AOSTerminal v"+str(terminalVer), True)
        self.echo("Changed dir to /", True)
    
    def doCommand(self, command="",silentOut=False):
        try:
            if command == "":
                # if self.lineEdit.text() != False:
                command = self.lineEdit.text()
                self.echo(text="[YOU] "+command,color="__YOU__")
            else:
                if silentOut == False:
                    self.echo("[SCRIPT] "+command)
                
            lowcommand = command.lower()

            self.lineEdit.setText("")

            splitUnneededSlash = False
            if lowcommand.startswith("echo"):
                final = self.splitParams(command)[0]

                for i in self.splitParams(command)[1:]:
                    final += " "+i

                self.echo(final)

            elif lowcommand.startswith("rm"):
                param = self.splitParams(command)[0]
                ok = True

                if param.startswith("/"):
                    param = param.split("/",1)
                    param = param[1]
                    
                if param.startswith("support"):
                    retval = msgBox(f"'{param}' is a child of or is the 'support' folder, which contains vital system files. Are you sure you want to delete it?","Are you sure?",QMessageBox.Warning,QMessageBox.Yes|QMessageBox.No)
                    if retval != 16384:
                        ok = False

                if param.endswith("/"):
                    if ok == True:
                        try:
                            rmdir((getcwd().replace("\\","/")+"/files/"+param))
                        except FileNotFoundError:
                            self.echo("ERR: The directory doesn't exist!",True)
                        except OSError:
                            self.echo(f"ERR: The directory isn't empty or doesn't exist!",True)
                else:
                    if ok == True:
                        try:
                            remove((getcwd().replace("\\","/")+"/files/"+param+"/"))
                        except FileNotFoundError:
                            self.echo("ERR: The file or directory doesn't exist!",True)
                        except NotADirectoryError:
                            self.echo(f"ERR: File not found! Are you sure it's not a directory?",True)

            elif lowcommand.startswith("dir"):
                param = self.splitParams(command)[0]

                if param.startswith("/"):
                    if param != "/":
                        param = param.split("/",1)
                        param = param[1]

                if not param.endswith("/"):
                    param = param+"/"

                try:
                    try:
                        self.echo("List of files/directories in "+param+":")
                        self.echo()

                        for _ in listdir(getcwd().replace("\\","/")+"/files/"+param):
                            if lowcommand.__contains__("-notypes"):
                                self.echo(_)
                            else:
                                if path.isdir(getcwd().replace("\\","/")+"/files/"+param+_):
                                    self.echo(_+" [DIR]")
                                elif path.isfile(getcwd().replace("\\","/")+"/files/"+param+_):
                                    self.echo(_+" [FILE]")
                                elif path.islink(getcwd().replace("\\","/")+"/files/"+param+_):
                                    self.echo(_+" [LINK]")
                                elif path.ismount(getcwd().replace("\\","/")+"/files/"+param+_):
                                    self.echo(_+" [MNT]")
                        self.echo()
                    except FileNotFoundError:
                        self.echo("ERR: Directory not found!")

                except NotADirectoryError:
                    self.echo("ERR: "+param+" is not a directory!", True)

            elif lowcommand.startswith("read"):
                param = self.splitParams(command)[0]
                if param.startswith("/"):
                    param = param.split("/",1)
                    param = param[1]

                try:
                    curline = 0

                    self.echo(f"[READ] Reading {param}...")
                    f = open(getcwd().replace("\\","/")+"/files/"+param,"r")
                    textInFile = f.readlines()
                    self.echo(f"[READ] Got {len(textInFile)} lines!")
                    self.echo()
                    for _ in textInFile:
                        _ = _.strip("\n")
                        curline += 1
                        self.echo(f"[READ:{curline}] {_}")
                except FileNotFoundError:
                    self.echo("ERR: File not found!",True)
                except PermissionError:
                    self.echo("ERR: File not found! Did you try to read a directory?",True)

            elif lowcommand.startswith("clear"):
                self.listWidget.clear()
            elif lowcommand.startswith("help"):
                if lowcommand.strip() == "help":
                    self.echo("List of all commands in database:")
                    self.echo()
                    tempList = []

                    for _ in helpText:
                        tempList.append(_)
                    
                    tempList.sort()
                    
                    for x in tempList:
                        self.echo(x)
                    self.echo()
                    self.echo("Type 'help {command}' for help on that command.")
                    self.echo()
                else:
                    try:
                        self.echo(helpText[(self.splitParams(command)[0]).lower()],True)
                    except KeyError:
                        self.echo("Command "+self.splitParams(command)[0]+" not found!")
            elif lowcommand.startswith("script"):
                param = self.splitParams(command)[0]
                silentOut = True

                if lowcommand.__contains__("-v") or lowcommand.__contains__("-verbose"):
                    self.echo("[SCRIPT] Running script "+param+"...")
                    silentOut = False

                self.echo()

                try:
                    script = open(getcwd().replace("\\","/")+"/files/"+param,"r")
                    script = script.read()
                    script = script.split("\n")

                    for i in script:
                        self.doCommand(i,silentOut)
                except OSError as e:
                    self.echo(f"ERR: {e}")
            elif lowcommand.startswith("ver"):
                z = open(getcwd().replace("\\","/")+"/files/system/data/version","r")
                self.echo("AOS v"+z.read()+". Terminal v"+str(terminalVer)+".",True)
                z.close()
            elif lowcommand.startswith("aterm"):
                self.listWidget.clear()
                self.echo("AOSTerminal v"+str(terminalVer), True)
                self.echo("Changed dir to /", True)
            elif lowcommand.startswith("beep"):
                try:
                    playsound(getcwd().replace("\\","/")+"/files/system/data/silence.wav")
                    playsound(getcwd().replace("\\","/")+"/files/system/data/AOS.wav")
                except:
                    pass
        except TypeError:
            pass

        except IndexError:
            self.echo("ERR: No arguments provided!", True)

    def echo(self, text="", fromSys=False, color="white"):
        if color != "__YOU__":
            try:
                color = text.split("|")[1]
                text = text.split("|")[0]
            except:
                pass

        if fromSys == True:
            self.listWidget.addItem("[SYS] "+text)
        else:
            self.listWidget.addItem(text)
        
        if color != "__YOU__":
            self.listWidget.item(self.listWidget.count()-1).setForeground(QColor(color))

        self.listWidget.scrollToBottom()

    
    def splitParams(self, text):
        try:
            text = text.split(" ")
            text = text[1:]
            return text
        except IndexError:
            text = text.split(" ")
            text = text[1]
            return text

class calculator(QWidget):

    def __init__(self):
        super(calculator, self).__init__()
        self.setWindowTitle("AOS-GUI/calc")
        self.setFixedSize(270, 340)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.ui()

    def ui(self):
        self.ans = QLineEdit(self)
        self.ans.setObjectName(u"ans")
        self.ans.setGeometry(QRect(9, 10, 251, 40))
        self.ans.setReadOnly(True)
        self.ans.setAlignment(Qt.AlignRight)
        self.ans.setFont(QFont('Arial', 15))
        self.push1 = QPushButton(self)
        self.push1.setObjectName(u"push1")
        self.push1.setGeometry(QRect(10, 100, 51, 51))
        self.push1.setText(u"1")
        self.push2 = QPushButton(self)
        self.push2.setObjectName(u"push2")
        self.push2.setGeometry(QRect(70, 100, 51, 51))
        self.push2.setText(u"2")
        self.push3 = QPushButton(self)
        self.push3.setObjectName(u"push3")
        self.push3.setGeometry(QRect(130, 100, 51, 51))
        self.push3.setText(u"3")
        self.push_plus = QPushButton(self)
        self.push_plus.setObjectName(u"add")
        self.push_plus.setGeometry(QRect(210, 60, 51, 51))
        self.push_plus.setText(u"+")
        self.push4 = QPushButton(self)
        self.push4.setObjectName(u"push4")
        self.push4.setGeometry(QRect(10, 160, 51, 51))
        self.push4.setText(u"4")
        self.push5 = QPushButton(self)
        self.push5.setObjectName(u"push5")
        self.push5.setGeometry(QRect(70, 160, 51, 51))
        self.push5.setText(u"5")
        self.push6 = QPushButton(self)
        self.push6.setObjectName(u"push6")
        self.push6.setGeometry(QRect(130, 160, 51, 51))
        self.push6.setText(u"6")
        self.push_minus = QPushButton(self)
        self.push_minus.setObjectName(u"push_minus")
        self.push_minus.setGeometry(QRect(210, 120, 51, 51))
        self.push_minus.setText(u"-")
        self.push_mul = QPushButton(self)
        self.push_mul.setObjectName(u"mult")
        self.push_mul.setGeometry(QRect(210, 180, 51, 51))
        self.push_mul.setText(u"*")
        self.push_div = QPushButton(self)
        self.push_div.setObjectName(u"div")
        self.push_div.setGeometry(QRect(210, 240, 51, 51))
        self.push_div.setText(u"/")
        self.push_equal = QPushButton(self)
        self.push_equal.setObjectName(u"equ")
        self.push_equal.setGeometry(QRect(210, 300, 51, 31))
        self.push_equal.setText(u"=")
        self.push_equal.setStyleSheet("background-color:darkred;")
        self.push7 = QPushButton(self)
        self.push7.setObjectName(u"push7")
        self.push7.setGeometry(QRect(10, 220, 51, 51))
        self.push7.setText(u"7")
        self.push8 = QPushButton(self)
        self.push8.setObjectName(u"push8")
        self.push8.setGeometry(QRect(70, 220, 51, 51))
        self.push8.setText(u"8")
        self.push9 = QPushButton(self)
        self.push9.setObjectName(u"push9")
        self.push9.setGeometry(QRect(130, 220, 51, 51))
        self.push9.setText(u"9")
        self.push0 = QPushButton(self)
        self.push0.setObjectName(u"push0")
        self.push0.setGeometry(QRect(70, 280, 51, 51))
        self.push0.setText(u"0")
        self.push_del = QPushButton(self)
        self.push_del.setObjectName(u"push_del")
        self.push_del.setGeometry(QRect(100, 60, 81, 23))
        self.push_del.setText(u"Del")
        self.push_clear = QPushButton(self)
        self.push_clear.setObjectName(u"push_clear")
        self.push_clear.setGeometry(QRect(10, 60, 75, 23))
        self.push_clear.setText(u"Clear")
        self.push_point = QPushButton(self)
        self.push_point.setObjectName(u"push_point")
        self.push_point.setGeometry(QRect(10, 280, 51, 51))
        self.push_point.setText(u".")
        self.push_minus.clicked.connect(self.action_minus)
        self.push_equal.clicked.connect(self.action_equal)
        self.push0.clicked.connect(self.action0)
        self.push1.clicked.connect(self.action1)
        self.push2.clicked.connect(self.action2)
        self.push3.clicked.connect(self.action3)
        self.push4.clicked.connect(self.action4)
        self.push5.clicked.connect(self.action5)
        self.push6.clicked.connect(self.action6)
        self.push7.clicked.connect(self.action7)
        self.push8.clicked.connect(self.action8)
        self.push9.clicked.connect(self.action9)
        self.push_div.clicked.connect(self.action_div)
        self.push_mul.clicked.connect(self.action_mul)
        self.push_plus.clicked.connect(self.action_plus)
        self.push_point.clicked.connect(self.action_point)
        self.push_clear.clicked.connect(self.action_clear)
        self.push_del.clicked.connect(self.action_del)


    def action_equal(self):
        equation = self.ans.text()

        try:
            ans = eval(equation)
            self.ans.setText(str(ans))

        except:
            self.ans.setText("NaN")

    def action_plus(self):
        text = self.ans.text()
        self.ans.setText(text + " + ")

    def action_minus(self):
        text = self.ans.text()
        self.ans.setText(text + " - ")

    def action_div(self):
        text = self.ans.text()
        self.ans.setText(text + " / ")

    def action_mul(self):
        text = self.ans.text()
        self.ans.setText(text + " * ")

    def action_point(self):
        text = self.ans.text()
        self.ans.setText(text + ".")

    def action0(self):
        text = self.ans.text()
        self.ans.setText(text + "0")

    def action1(self):
        text = self.ans.text()
        self.ans.setText(text + "1")

    def action2(self):
        text = self.ans.text()
        self.ans.setText(text + "2")

    def action3(self):
        text = self.ans.text()
        self.ans.setText(text + "3")

    def action4(self):
        text = self.ans.text()
        self.ans.setText(text + "4")

    def action5(self):
        text = self.ans.text()
        self.ans.setText(text + "5")

    def action6(self):
        text = self.ans.text()
        self.ans.setText(text + "6")

    def action7(self):
        text = self.ans.text()
        self.ans.setText(text + "7")

    def action8(self):
        text = self.ans.text()
        self.ans.setText(text + "8")

    def action9(self):
        text = self.ans.text()
        self.ans.setText(text + "9")

    def action_clear(self):
        self.ans.setText("")

    def action_del(self):
        text = self.ans.text()
        self.ans.setText(text[:len(text)-1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.action1()
        elif event.key() == Qt.Key_2:
            self.action2()
        elif event.key() == Qt.Key_3:
            self.action3()
        elif event.key() == Qt.Key_4:
            self.action4()
        elif event.key() == Qt.Key_5:
            self.action5()
        elif event.key() == Qt.Key_6:
            self.action6()
        elif event.key() == Qt.Key_7:
            self.action7()
        elif event.key() == Qt.Key_8:
            self.action8()
        elif event.key() == Qt.Key_9:
            self.action9()
        elif event.key() == Qt.Key_0:
            self.action0()
        elif event.key() == Qt.Key_Plus:
            self.action_plus()
        elif event.key() == Qt.Key_Minus:
            self.action_minus()
        elif event.key() == Qt.Key_Asterisk:
            self.action_mul()
        elif event.key() == Qt.Key_Slash:
            self.action_div()
        elif event.key() == Qt.Key_Return:
            self.action_equal()
        elif event.key() == Qt.Key_Backspace:
            self.action_del()
        elif event.key() == Qt.Key_Period:
            self.action_point()
        elif event.key() == Qt.Key_Escape:
            self.action_clear()

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
                print(f"camelInstall couldn't find info for the app ({name}), getting info from package name...")
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

    def installApp(self):
        try:
            val = 0
            text = self.dbTable.item(self.dbTable.currentRow(),0).text()
            ret = msgBox("Are you sure you want to install \""+text+"\"?","Install?",QMessageBox.Question,QMessageBox.Yes|QMessageBox.No)
            if ret == 16384:
                url = self.dbTable.item(self.dbTable.currentRow(),3).text()
                if url.startswith("db/"):
                    url = url.split("db/")[1]
                    url = "https://raw.githubusercontent.com/Nanobot567/cInstall/main/dl/"+url
                r = requests.get(url)
                f = open(getcwd().replace("\\","/")+"/files/apps/"+(url.split("/")[len(url.split("/"))-1]).split("\n")[0],"w")
                f.write(r.text)
                f.close()
                msgBox(f"Installed \"{self.dbTable.item(self.dbTable.currentRow(),0).text()}\"!","Installed!",QMessageBox.Information,QMessageBox.Ok)
                self.refreshApps()
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
                url = "https://raw.githubusercontent.com/Nanobot567/cInstall/main/dl/"+url
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
        msgBox(f"Uninstalled '{item}'!","Uninstalled!",QMessageBox.Information,QMessageBox.Ok)
        self.refreshApps()

    # retranslateUi

class editApp(QWidget):
    def __init__(self):
        super(editApp, self).__init__()
        global textEdit
        self.originalText = ""
        self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFile}")
        self.setFixedSize(640, 480)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        textEdit = QTextEdit(self)
        textEdit.setObjectName(u"textEdit")
        textEdit.setGeometry(QRect(10, 40, 621, 431))
        self.open = QPushButton(self)
        self.open.setObjectName(u"open")
        self.open.setGeometry(QRect(60, 10, 51, 28))
        self.open.setText(u"Open")
        self.open.clicked.connect(self.openFile)
        self.save = QPushButton(self)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(120, 10, 51, 28))
        self.save.setText(u"Save")
        self.save.clicked.connect(self.saveFile)
        self.saveAs = QPushButton(self)
        self.saveAs.setObjectName(u"saveAs")
        self.saveAs.setGeometry(QRect(180, 10, 71, 28))
        self.saveAs.setText(u"Save As")
        self.saveAs.clicked.connect(self.saveAsFile)
        self.newFileBtn = QPushButton(self)
        self.newFileBtn.setObjectName(u"newFile")
        self.newFileBtn.setGeometry(QRect(10, 10, 41, 28))
        self.newFileBtn.setText("New")
        self.newFileBtn.clicked.connect(self.newFile)
        self.formatBox = QComboBox(self)
        self.formatBox.addItem(u"Plaintext")
        self.formatBox.addItem(u"Markdown")
        self.formatBox.addItem(u"HTML")
        self.formatBox.setObjectName(u"formatBox")
        self.formatBox.setGeometry(QRect(490, 10, 141, 21))
        self.formatBox.activated.connect(self.updateText)
        

    def updateText(self):
        if self.formatBox.currentText() == "Plaintext":
            if self.originalText != "":
                textEdit.setText(self.originalText)
            else:
                textEdit.setText(textEdit.toPlainText())
        elif self.formatBox.currentText() == "Markdown":
            self.originalText = textEdit.toPlainText()
            textEdit.setMarkdown(textEdit.toMarkdown())
        elif self.formatBox.currentText() == "HTML":
            self.originalText = textEdit.toPlainText()
            textEdit.setHtml(textEdit.toHtml())

    def newFile(self):
        global currentlyOpenFile,currentlyOpenFileName
        file,check = QFileDialog.getSaveFileName(None, "New File", directory=getcwd().replace("\\","/")+"/files/")
        if check:
            text = open(file,"w")
            text.close()
            currentlyOpenFile = file
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
            self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")


    def openFile(self):
        file,check = QFileDialog.getOpenFileName(None, "Open a file", getcwd().replace("\\","/")+"/files/", "All Files (*)")
        if check:
            text = open(file,"r")
            textEdit.setText(text.read())
            text.close()

            global currentlyOpenFile,currentlyOpenFileName
            currentlyOpenFile = file
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
            self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")
    
    def saveFile(self):
        global currentlyOpenFile,currentlyOpenFileName

        if currentlyOpenFileName == "Untitled":
            self.saveAsFile()
        else:
            text = open(currentlyOpenFile,"w")
            text.write(textEdit.toPlainText())
            text.close()
    
    def saveAsFile(self):
        global currentlyOpenFile,currentlyOpenFileName

        file,check = QFileDialog.getSaveFileName(None, "Save", directory=getcwd().replace("\\","/")+"/files/")
        if check:
            text = open(file,"w")
            text.write(textEdit.toPlainText())
            text.close()
            currentlyOpenFile = file
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
            self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")

    def openViaOutsideSource(self, path):
        if self == None:
            self = super(editApp, self).__init__
            print("self none")
        text = open(path,"r")
        textEdit.setText(text.read())
        text.close()

        global currentlyOpenFile,currentlyOpenFileName
        currentlyOpenFile = path
        currentlyOpenFileName = currentlyOpenFile.split("/")
        currentlyOpenFileName = currentlyOpenFileName[-1]
        editApp().setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")
        editApp().show()
        print("yea")

class FsWindow(QWidget):
    def __init__(self):
        super(FsWindow, self).__init__()
        self.setWindowTitle("AOS-GUI/fs")
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.treeView = QTreeView(self)
        self.treeView.setGeometry(10,10,580,380)
        self.fileSystemModel = QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(False)
        root = self.fileSystemModel.setRootPath("files")
        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex(root)
        self.treeView.setDragDropMode(QAbstractItemView.InternalMove)
        self.treeView.setDragEnabled(True)
        self.treeView.setAcceptDrops(True)
        self.treeView.setDropIndicatorShown(True)

        # self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.treeView.customContextMenuRequested.connect(self.menuContextTree)

    def dragEnterEvent(self, event):
        m = event.mimeData()
        if m.hasUrls():
            for url in m.urls():
                if url.isLocalFile():
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        if event.source():
            QTreeView.dropEvent(self, event)
        else:
            ix = self.indexAt(event.pos())
            if not self.model().isDir(ix):
                ix = ix.parent()
            pathDir = self.model().filePath(ix)
            m = event.mimeData()
            if m.hasUrls():
                urlLocals = [url for url in m.urls() if url.isLocalFile()]
                accepted = False
                for urlLocal in urlLocals:
                    path = urlLocal.toLocalFile()
                    info = QFileInfo(path)
                    n_path = QDir(pathDir).filePath(info.fileName())
                    o_path = info.absoluteFilePath()
                    if n_path == o_path:
                        continue
                    if info.isDir():
                        QDir().rename(o_path, n_path)
                    else:
                        qfile = QFile(o_path)
                        if QFile(n_path).exists():
                            n_path += "(copy)" 
                        qfile.rename(n_path)
                    accepted = True
                if accepted:
                    event.acceptProposedAction()

    # def createFolder(self):
    #     index = self.treeView.currentIndex()
    #     if not self.model().isDir(index):
    #         index = index.parent()
    #     pathDir = self.model().filePath(index)
    #     mkdir(pathDir+"/New Folder")

    def menuContextTree(self, point):
        index = self.treeView.indexAt(point)

        if not index.isValid():
            return

        # item = self.treeView.childAt(point)
        name = index.data()

        menu = QMenu()
        action = menu.addAction(name)
        menu.addSeparator()
        action_1 = menu.addAction("Delete")
        action_2 = menu.addAction("New Folder")
        action_3 = menu.addAction("3")

        app = editApp()

        menu.exec_(self.treeView.mapToGlobal(point))

        # action_2.triggered.connect(self.createFolder)


class settingsWidget(QWidget):
    def __init__(self):
        super(settingsWidget, self).__init__()

        self.setFixedSize(450, 540)
        self.setWindowTitle(u"AOS-GUI/settings")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.tabs = QTabWidget(self)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setGeometry(QRect(10, 10, 431, 521))
        self.tabs.setMovable(False)
        self.general = QWidget()
        self.general.setObjectName(u"general")
        self.user = QGroupBox(self.general)
        self.user.setObjectName(u"user")
        self.user.setGeometry(QRect(10, 0, 251, 81))
        self.user.setTitle(u"User")
        self.uLabel = QLabel(self.user)
        self.uLabel.setObjectName(u"uLabel")
        self.uLabel.setGeometry(QRect(20, 20, 81, 21))
        self.uLabel.setText(u"Username:")
        self.uLE = QLineEdit(self.user)
        self.uLE.setObjectName(u"uLE")
        self.uLE.setGeometry(QRect(100, 20, 131, 21))
        self.uLE.setText(u"")
        self.pLabel = QLabel(self.user)
        self.pLabel.setObjectName(u"pLabel")
        self.pLabel.setGeometry(QRect(20, 50, 81, 21))
        self.pLabel.setText(u"Password:")
        self.pLE = QLineEdit(self.user)
        self.pLE.setObjectName(u"pLE")
        self.pLE.setGeometry(QRect(100, 50, 131, 21))
        self.pLE.setText(u"")
        self.pLE.setEchoMode(QLineEdit.Password)
        self.eBg = QPushButton(self.general)
        self.eBg.setObjectName(u"eBg")
        self.eBg.setGeometry(QRect(170, 460, 91, 28))
        self.eBg.setText(u"Ok")
        self.clockBox = QGroupBox(self.general)
        self.clockBox.setObjectName(u"clockBox")
        self.clockBox.setGeometry(QRect(270, 0, 151, 51))
        self.clockBox.setTitle(u"Clock")
        self.clockMode = QCheckBox(self.clockBox)
        self.clockMode.setObjectName(u"clockMode")
        self.clockMode.setGeometry(QRect(10, 20, 131, 17))
        self.clockMode.setText(u"24 hour clock")
        self.tabs.addTab(self.general, "")
        self.tabs.setTabText(self.tabs.indexOf(self.general), u"General")
        self.customization = QWidget()
        self.customization.setObjectName(u"customization")
        self.colors = QGroupBox(self.customization)
        self.colors.setObjectName(u"colors")
        self.colors.setGeometry(QRect(10, 0, 401, 211))
        self.colors.setTitle(u"Colors (all colors/hex codes valid)")
        self.cL = QLabel(self.colors)
        self.cL.setObjectName(u"cL")
        self.cL.setGeometry(QRect(10, 30, 71, 16))
        self.cL.setText(u"Text Color:")
        self.cL_2 = QLabel(self.colors)
        self.cL_2.setObjectName(u"cL_2")
        self.cL_2.setGeometry(QRect(10, 60, 71, 16))
        self.cL_2.setText(u"BG Color:")
        self.cL_3 = QLabel(self.colors)
        self.cL_3.setObjectName(u"cL_3")
        self.cL_3.setGeometry(QRect(10, 90, 91, 16))
        self.cL_3.setText(u"Taskbar Color:")
        self.cL_4 = QLabel(self.colors)
        self.cL_4.setObjectName(u"cL_4")
        self.cL_4.setGeometry(QRect(10, 120, 121, 16))
        self.cL_4.setText(u"Taskbar Text Color:")
        self.cL_5 = QLabel(self.colors)
        self.cL_5.setObjectName(u"cL_5")
        self.cL_5.setGeometry(QRect(10, 150, 121, 16))
        self.cL_5.setText(u"Button Color:")
        self.cL_6 = QLabel(self.colors)
        self.cL_6.setObjectName(u"cL_6")
        self.cL_6.setGeometry(QRect(10, 180, 121, 16))
        self.cL_6.setText(u"Button Text Color:")
        self.cLE = QLineEdit(self.colors)
        self.cLE.setObjectName(u"cLE")
        self.cLE.setGeometry(QRect(130, 30, 81, 22))
        self.cLE_2 = QLineEdit(self.colors)
        self.cLE_2.setObjectName(u"cLE_2")
        self.cLE_2.setGeometry(QRect(130, 60, 81, 22))
        self.cLE_3 = QLineEdit(self.colors)
        self.cLE_3.setObjectName(u"cLE_3")
        self.cLE_3.setGeometry(QRect(130, 90, 81, 22))
        self.cLE_4 = QLineEdit(self.colors)
        self.cLE_4.setObjectName(u"cLE_4")
        self.cLE_4.setGeometry(QRect(130, 120, 81, 22))
        self.cLE_5 = QLineEdit(self.colors)
        self.cLE_5.setObjectName(u"cLE_5")
        self.cLE_5.setGeometry(QRect(130, 150, 81, 22))
        self.cLE_6 = QLineEdit(self.colors)
        self.cLE_6.setObjectName(u"cLE_6")
        self.cLE_6.setGeometry(QRect(130, 180, 81, 22))
        self.themes = QGroupBox(self.colors)
        self.themes.setObjectName(u"themes")
        self.themes.setGeometry(QRect(220, 10, 171, 131))
        self.themes.setTitle(u"Color Themes")
        self.themeCB = QComboBox(self.themes)
        self.themeCB.setObjectName(u"themeCB")
        self.themeCB.setGeometry(QRect(20, 30, 131, 22))
        self.themeCB.setCurrentText(u"")
        self.tApply = QPushButton(self.themes)
        self.tApply.setObjectName(u"tApply")
        self.tApply.setGeometry(QRect(40, 60, 93, 28))
        self.tApply.setText(u"Apply")
        self.tSave = QPushButton(self.themes)
        self.tSave.setObjectName(u"tSave")
        self.tSave.setGeometry(QRect(40, 90, 93, 28))
        self.tSave.setText(u"Save")
        self.guiThemes = QGroupBox(self.colors)
        self.guiThemes.setObjectName(u"guiThemes")
        self.guiThemes.setGeometry(QRect(220, 150, 171, 51))
        self.guiThemes.setTitle(u"GUI Themes")
        self.guiThemeCB = QComboBox(self.guiThemes)
        self.guiThemeCB.setObjectName(u"guiThemeCB")
        self.guiThemeCB.setGeometry(QRect(10, 20, 151, 22))
        self.showOnDesktop = QGroupBox(self.customization)
        self.showOnDesktop.setObjectName(u"showOnDesktop")
        self.showOnDesktop.setGeometry(QRect(10, 220, 101, 231))
        self.showOnDesktop.setTitle(u"Show On Desktop")
        self.dCHB = QCheckBox(self.showOnDesktop)
        self.dCHB.setObjectName(u"dCHB")
        self.dCHB.setGeometry(QRect(10, 30, 81, 20))
        self.dCHB.setText(u"Settings")
        self.dCHB_2 = QCheckBox(self.showOnDesktop)
        self.dCHB_2.setObjectName(u"dCHB_2")
        self.dCHB_2.setGeometry(QRect(10, 50, 81, 20))
        self.dCHB_2.setText(u"appLauncher")
        self.dCHB_3 = QCheckBox(self.showOnDesktop)
        self.dCHB_3.setObjectName(u"dCHB_3")
        self.dCHB_3.setGeometry(QRect(10, 70, 91, 20))
        self.dCHB_3.setText(u"FileSystem")
        self.dCHB_4 = QCheckBox(self.showOnDesktop)
        self.dCHB_4.setObjectName(u"dCHB_4")
        self.dCHB_4.setGeometry(QRect(10, 90, 101, 20))
        self.dCHB_4.setText(u"camelInstall")
        self.dCHB_5 = QCheckBox(self.showOnDesktop)
        self.dCHB_5.setObjectName(u"dCHB_5")
        self.dCHB_5.setGeometry(QRect(10, 110, 81, 20))
        self.dCHB_5.setText(u"Editor")
        self.dCHB_6 = QCheckBox(self.showOnDesktop)
        self.dCHB_6.setObjectName(u"dCHB_6")
        self.dCHB_6.setGeometry(QRect(10, 130, 81, 20))
        self.dCHB_6.setText(u"AOSHelp")
        self.dCHB_7 = QCheckBox(self.showOnDesktop)
        self.dCHB_7.setObjectName(u"dCHB_7")
        self.dCHB_7.setGeometry(QRect(10, 150, 81, 20))
        self.dCHB_7.setText(u"ATerm")
        self.dCHB_8 = QCheckBox(self.showOnDesktop)
        self.dCHB_8.setObjectName(u"dCHB_8")
        self.dCHB_8.setGeometry(QRect(10, 170, 81, 20))
        self.dCHB_8.setText(u"Calculator")
        self.eBc = QPushButton(self.customization)
        self.eBc.setObjectName(u"eBc")
        self.eBc.setGeometry(QRect(170, 460, 91, 28))
        self.eBc.setText(u"Ok")
        self.font = QGroupBox(self.customization)
        self.font.setObjectName(u"font")
        self.font.setGeometry(QRect(270, 220, 141, 51))
        self.font.setTitle(u"Font")
        self.fSB = QSpinBox(self.font)
        self.fSB.setObjectName(u"fSB")
        self.fSB.setGeometry(QRect(20, 20, 51, 22))
        self.fSB.setSuffix(u"px")
        self.fL = QLabel(self.font)
        self.fL.setObjectName(u"fL")
        self.fL.setGeometry(QRect(80, 23, 61, 16))
        self.fL.setText(u"Font Size")
        self.splash = QGroupBox(self.customization)
        self.splash.setObjectName(u"splash")
        self.splash.setGeometry(QRect(120, 220, 141, 51))
        self.splash.setTitle(u"Splash Dialog")
        self.showSplashOnStartup = QCheckBox(self.splash)
        self.showSplashOnStartup.setObjectName(u"checkBox")
        self.showSplashOnStartup.setGeometry(QRect(10, 20, 131, 20))
        self.showSplashOnStartup.setText(u"Show on startup")
        self.tabs.addTab(self.customization, "")
        self.shortcuts = QWidget()
        self.shortcuts.setObjectName(u"shortcuts")
        self.sDesktop = QGroupBox(self.shortcuts)
        self.sDesktop.setObjectName(u"groupBox")
        self.sDesktop.setGeometry(QRect(10, 0, 401, 451))
        self.sDesktop.setTitle(u"Desktop")
        self.KS = QKeySequenceEdit(self.sDesktop)
        self.KS.setObjectName(u"KS")
        self.KS.setGeometry(QRect(90, 30, 113, 22))
        self.KS.setKeySequence(u"Ctrl+R")
        self.sL = QLabel(self.sDesktop)
        self.sL.setObjectName(u"sL")
        self.sL.setGeometry(QRect(20, 30, 55, 16))
        self.sL.setText(u"Run...")
        self.KS_2 = QKeySequenceEdit(self.sDesktop)
        self.KS_2.setObjectName(u"KS_2")
        self.KS_2.setGeometry(QRect(90, 60, 113, 22))
        self.KS_2.setKeySequence(u"Ctrl+T")
        self.sL_2 = QLabel(self.sDesktop)
        self.sL_2.setObjectName(u"sL_2")
        self.sL_2.setGeometry(QRect(20, 60, 55, 16))
        self.sL_2.setText(u"Terminal")
        self.KS_3 = QKeySequenceEdit(self.sDesktop)
        self.KS_3.setObjectName(u"KS_3")
        self.KS_3.setGeometry(QRect(90, 90, 113, 22))
        self.KS_3.setKeySequence(u"Ctrl+Shift+S")
        self.sL_3 = QLabel(self.sDesktop)
        self.sL_3.setObjectName(u"sL_3")
        self.sL_3.setGeometry(QRect(20, 90, 55, 16))
        self.sL_3.setText(u"Settings")
        self.sL_4 = QLabel(self.sDesktop)
        self.sL_4.setObjectName(u"sL_4")
        self.sL_4.setGeometry(QRect(20, 120, 55, 16))
        self.sL_4.setText(u"Help")
        self.KS_4 = QKeySequenceEdit(self.sDesktop)
        self.KS_4.setObjectName(u"KS_4")
        self.KS_4.setGeometry(QRect(90, 120, 113, 22))
        self.KS_4.setKeySequence(u"Ctrl+H")
        self.eBs = QPushButton(self.shortcuts)
        self.eBs.setObjectName(u"eBs")
        self.eBs.setGeometry(QRect(170, 460, 91, 28))
        self.eBs.setText(u"Ok")
        self.tabs.addTab(self.shortcuts, "")
        self.reset = QWidget()
        self.reset.setObjectName(u"reset")
        self.rAOS = QPushButton(self.reset)
        self.rAOS.setObjectName(u"rAOS")
        self.rAOS.setGeometry(QRect(130, 50, 161, 28))
        self.rAOS.setText(u"Reset AOS...")
        self.rAOS.clicked.connect(self.resetAOS)
        self.tabs.addTab(self.reset, "")
        self.tabs.setTabText(self.tabs.indexOf(self.reset), u"Reset")

        self.retranslateUi()

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(self)
    # setupUi

    def resetAOS(self, andmodules = False):
        retval = msgBox(f"Are you sure you want to reset AOS to its default settings?","Reset AOS?",QMessageBox.Warning,QMessageBox.Yes|QMessageBox.No)

        if retval == 16384:
            retval2 = msgBox(f"Are you SURE? All of your documents and user data will be erased!","Are you SURE?",QMessageBox.Warning,QMessageBox.Yes|QMessageBox.No)
            if retval2 == 16384:
                retval3 = msgBox("If you say so...","Whatever you say!",QMessageBox.Warning,QMessageBox.Yes|QMessageBox.No)
                if retval3 == 16384:
                    self.eraseAllData()


    def retranslateUi(self):
        self.pLE.setInputMask("")
        self.tabs.setTabText(self.tabs.indexOf(self.customization), QCoreApplication.translate("settings", u"Customization", None))
        self.tabs.setTabText(self.tabs.indexOf(self.shortcuts), QCoreApplication.translate("settings", u"Shortcuts", None))

        self.tApply.clicked.connect(self.applyTheme)
        self.tSave.clicked.connect(self.saveTheme)
        self.eBg.clicked.connect(self.getmeout)
        self.eBc.clicked.connect(self.getmeout)
        self.eBs.clicked.connect(self.getmeout)
        self.getCurrentSettings()

    def eraseAllData(self):
        homeCwd = getcwd().replace("\\","/")+"/files/home/"

        remove(getcwd().replace("\\","/")+"/files/system/data/user/data.aos")
        rmtree(homeCwd)
        sleep(2)
        mkdir(homeCwd)
        msgBox("AOS has been factory reset.","Done.",QMessageBox.Information,QMessageBox.Ok)
        exit()

    def toBool(self, string):
        if string == "True":
            return True
        elif string == "False":
            return False
        
    # retranslateUi
    def getCurrentSettings(self):
        # pass

        f = open("files/system/data/user/data.aos","r")
        content = f.read()
        content = content.split("\n")

        try:
            themeText = open("files/system/data/user/themes/"+content[2]+".theme","r")
        except FileNotFoundError:
            themeText = open("files/system/data/user/themes/default-dark.theme","r")
        themeText = themeText.read()
        themeColors = themeText.split("\n")

        self.guiThemeCB.clear()
        self.themeCB.clear()

        for _ in listdir(getcwd().replace("\\","/")+"/files/system/data/user/themes/"):
            self.themeCB.addItem(_.split(".theme")[0])

        self.uLE.setText(content[0])
        self.pLE.setText(content[1])
        self.themeCB.setCurrentText(content[2])
        self.cLE.setText(themeColors[0])
        self.cLE_2.setText(themeColors[1])
        self.cLE_3.setText(themeColors[2])
        self.cLE_4.setText(themeColors[3])
        self.cLE_5.setText(themeColors[4])
        self.cLE_6.setText(themeColors[5])
        self.fSB.setValue(int(content[3]))
        self.KS.setKeySequence(content[4])
        self.KS_2.setKeySequence(content[5])
        self.KS_3.setKeySequence(content[6])
        self.KS_4.setKeySequence(content[7])

        desktopCheckmarkVals = content[8].split("|")

        self.dCHB.setChecked(self.toBool(desktopCheckmarkVals[0]))
        self.dCHB_2.setChecked(self.toBool(desktopCheckmarkVals[1]))
        self.dCHB_3.setChecked(self.toBool(desktopCheckmarkVals[2]))
        self.dCHB_4.setChecked(self.toBool(desktopCheckmarkVals[3]))
        self.dCHB_5.setChecked(self.toBool(desktopCheckmarkVals[4]))
        self.dCHB_6.setChecked(self.toBool(desktopCheckmarkVals[5]))
        self.dCHB_7.setChecked(self.toBool(desktopCheckmarkVals[6]))
        self.dCHB_8.setChecked(self.toBool(desktopCheckmarkVals[7]))

        self.showSplashOnStartup.setChecked(not self.toBool(content[9]))
        
        for i in QStyleFactory.keys():
            self.guiThemeCB.addItem(i)
        
        self.guiThemeCB.setCurrentText(content[10])

        self.clockMode.setChecked(self.toBool(content[11]))


    def applyTheme(self):
        tFile = open("files/system/data/user/themes/"+self.themeCB.currentText()+".theme","r")
        colors = tFile.read()
        themeColors = colors.split("\n")

        self.cLE.setText(themeColors[0])
        self.cLE_2.setText(themeColors[1])
        self.cLE_3.setText(themeColors[2])
        self.cLE_4.setText(themeColors[3])
        self.cLE_5.setText(themeColors[4])
        self.cLE_6.setText(themeColors[5])


    def saveTheme(self):
        currentColors = [self.cLE.text(),self.cLE_2.text(),self.cLE_3.text(),self.cLE_4.text(),self.cLE_5.text(),self.cLE_6.text()]

        tFile,check = QFileDialog.getSaveFileName(None, "Save to theme", getcwd().replace("\\","/")+"/files/system/data/user/themes/", "AOS theme (*.theme)")
        if check:
            themeFile = open(tFile,"w")

            for i in range(5):
                themeFile.write(currentColors[i]+"\n")
            themeFile.write(currentColors[5])

            themeFile.close()
        self.getCurrentSettings()

    def getmeout(self):
        retval = 0

        f = open("files/system/data/user/data.aos","w")
        themeFile = open("files/system/data/user/themes/"+self.themeCB.currentText()+".theme","r")
        tFile = getcwd().replace("\\","/")+"/files/system/data/user/themes/"+self.themeCB.currentText()+".theme"

        tFsplit = themeFile.read().split("\n")

        currentColors = [self.cLE.text(),self.cLE_2.text(),self.cLE_3.text(),self.cLE_4.text(),self.cLE_5.text(),self.cLE_6.text()]

        if currentColors != tFsplit:
            tFile = getcwd().replace("\\","/")+"/files/system/data/user/themes/"+self.themeCB.currentText()+".theme"

            retval = msgBox(f"You have unsaved color changes. Would you like to save them to a new theme?", "Save changes to theme?", QMessageBox.Warning, QMessageBox.Yes|QMessageBox.No)

            if retval == 16384: # yes value
                tFile,check = QFileDialog.getSaveFileName(None, "Save to theme", getcwd().replace("\\","/")+"/files/system/data/user/themes/", "AOS theme (*.theme)")
                if check:
                    themeFile.close()
                    themeFile = open(tFile,"w")

                    for i in range(5):
                        themeFile.write(currentColors[i]+"\n")
                    themeFile.write(currentColors[5])

                    themeFile.close()

        f.write(self.uLE.text()+"\n")
        f.write(self.pLE.text()+"\n")
        if retval == 16384:
            tFile = tFile.split("/")
            tFile = tFile[len(tFile)-1].split(".")
            tFile = tFile[0]
            f.write(tFile+"\n")
        else:
            f.write(self.themeCB.currentText()+"\n")
        f.write(str(self.fSB.value())+"\n")
        f.write(self.KS.keySequence().toString()+"\n")
        f.write(self.KS_2.keySequence().toString()+"\n")
        f.write(self.KS_3.keySequence().toString()+"\n")
        f.write(self.KS_4.keySequence().toString()+"\n")
        f.write(str(self.dCHB.isChecked())+"|")
        f.write(str(self.dCHB_2.isChecked())+"|")
        f.write(str(self.dCHB_3.isChecked())+"|")
        f.write(str(self.dCHB_4.isChecked())+"|")
        f.write(str(self.dCHB_5.isChecked())+"|")
        f.write(str(self.dCHB_6.isChecked())+"|")
        f.write(str(self.dCHB_7.isChecked())+"|")
        f.write(str(self.dCHB_8.isChecked())+"\n")
        f.write(str(not self.showSplashOnStartup.isChecked())+"\n")
        f.write(self.guiThemeCB.currentText()+"\n")
        f.write(str(self.clockMode.isChecked()))

        msgBox("Your settings have been applied! Please restart AOS-GUI to see your changes.", "Settings set!", QMessageBox.Information, QMessageBox.Ok)
        self.close()

class splashScreen(QWidget):

    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        global splashTexts
        super(splashScreen, self).__init__()

        self.setFixedSize(460, 310)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setWindowTitle(u"AOS-GUI")
        self.aosgui = QLabel(self)
        self.aosgui.setObjectName(u"aosgui")
        self.aosgui.setGeometry(QRect(-2, 10, 450, 91))
        self.aosgui.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:48pt;\">AOS-GUI</span></p></body></html>")
        self.aosgui.setTextFormat(Qt.RichText)
        self.aidensos = QLabel(self)
        self.aidensos.setObjectName(u"aidensos")
        self.aidensos.setGeometry(QRect(0, 100, 451, 21))
        self.aidensos.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Aiden's Operating System - Graphical User Interface</span></p></body></html>")
        self.button = QPushButton(self)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(46, 230, 370, 41))
        font = QFont()
        font.setFamily(u"MS Shell Dlg 2")
        font.setPointSize(12)
        self.button.setFont(font)
        self.button.setText(u"Let me in!")
        self.button.clicked.connect(self.letsgo)
        self.version = QLabel(self)
        self.version.setObjectName(u"version")
        self.version.setGeometry(QRect(-78, 290, 211, 20))
        self.version.setText(u"<html><head/><body><p align=\"center\">"+version+" <span style=\" color:#ff0000;\">alpha</span></p></body></html>")
        self.createdby = QLabel(self)
        self.createdby.setObjectName(u"createdby")
        self.createdby.setGeometry(QRect(126, 120, 211, 20))
        self.createdby.setText(u"<html><head/><body><p align=\"center\"><a href=\"https://github.com/nanobot567/\"><span style=\" text-decoration: underline; color:#0000ff;\">created by nanobot567</span></a></p></body></html>")
        self.createdby.setOpenExternalLinks(True)
        self.dontshowagain = QCheckBox(self)
        self.dontshowagain.setObjectName(u"dontshowagain")
        self.dontshowagain.setGeometry(QRect(165, 280, 150, 20))
        self.dontshowagain.setText(u"Don't show this again")
        self.splashTextLabel = QLabel(self)
        self.splashTextLabel.setObjectName(u"splashTextLabel")
        self.splashTextLabel.setGeometry(QRect(0, 160, 462, 41))
        self.splashTextLabel.setText(u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; blink;\">"+choice(splashTexts)+"</span></p></body></html>")

        QMetaObject.connectSlotsByName(self)

        
    
    def letsgo(self):
        f = open("files/system/data/user/data.aos","r")
        content = f.readlines()
        f.close()
        f = open("files/system/data/user/data.aos","w")
        content[9] = str(self.dontshowagain.isChecked())+"\n"
        for i in content:
            if i != "":
                f.write(i)
        f.close()
        self.close()