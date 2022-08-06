from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep
import os

dir = "/home"

helpText = {"help":"aos help (syntax: help {command})",
            "clear":"clears the screen (syntax: clear)",
            "echo":"echoes text (syntax: echo [text])",
            "rm":"removes a file (syntax: rm [path from /])",
            "dir":"lists the files and directories inside a directory (syntax: dir [path] {-notypes})",
            "read":"reads a file's contents (syntax: read [file])",
            "script":"runs a script (syntax: script [file] {-v | -verbose})"}

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


        self.echo("AOSTerminal v1.0", True)
        self.echo("Changed dir to /", True)
    
    def doCommand(self, command="",silentOut=False):
        if command == "":
            command = self.lineEdit.text()
            self.echo("[YOU] "+command)
        else:
            if silentOut == False:
                self.echo("[SCRIPT] "+command)
            

        lowcommand = command.lower()

        self.lineEdit.setText("")

        splitUnneededSlash = False

        try:
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
                    warn = QMessageBox()
                    warn.setIcon(QMessageBox.Warning)
                    warn.setText(f"'{param}' is a child of or is the 'support' folder, which contains vital system files. Are you sure you want to delete it?")
                    warn.setWindowTitle("Are you sure?")
                    warn.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
                    warn.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                    retval = warn.exec_()

                    if retval != 16384:
                        ok = False

                if param.endswith("/"):
                    if ok == True:
                        try:
                            os.rmdir((os.getcwd().replace("\\","/")+"/files/"+param))
                        except FileNotFoundError:
                            self.echo("ERR: The directory doesn't exist!",True)
                        except OSError:
                            self.echo(f"ERR: The directory isn't empty or doesn't exist!",True)
                else:
                    try:
                        os.remove((os.getcwd().replace("\\","/")+"/files/"+param))
                    except FileNotFoundError:
                        self.echo("ERR: The file or directory doesn't exist!",True)
                    except NotADirectoryError:
                        self.echo(f"ERR: File not found! Are you sure it's not a directory?",True)
                            
                #.replace("/","\\")
                # fix
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

                        for _ in os.listdir(os.getcwd().replace("\\","/")+"/files/"+param):
                            if lowcommand.__contains__("-notypes"):
                                self.echo(_)
                            else:
                                if os.path.isdir(os.getcwd().replace("\\","/")+"/files/"+param+_):
                                    self.echo(_+" [DIR]")
                                elif os.path.isfile(os.getcwd().replace("\\","/")+"/files/"+param+_):
                                    self.echo(_+" [FILE]")
                                elif os.path.islink(os.getcwd().replace("\\","/")+"/files/"+param+_):
                                    self.echo(_+" [LINK]")
                                elif os.path.ismount(os.getcwd().replace("\\","/")+"/files/"+param+_):
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
                    f = open(os.getcwd().replace("\\","/")+"/files/"+param,"r")
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
                    script = open(os.getcwd().replace("\\","/")+"/files/"+param,"r")
                    script = script.read()
                    script = script.split("\n")

                    for i in script:
                        self.doCommand(i,silentOut)
                except OSError as e:
                    self.echo(f"ERR: {e}")
                

        except IndexError:
            self.echo("ERR: No arguments provided!", True)

    def echo(self, text="", fromSys=False):
        # add statuses, like warning or error (bg color should change on that line)

        if fromSys == True:
            self.listWidget.addItem("[SYS] "+text)
        else:
            self.listWidget.addItem(text)

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