from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import listdir,path,getcwd,remove,rmdir,mkdir
from files.system.sdk.sdk import *
from playsound import playsound

dir = "/home"
terminalVer = 1.3
helpText = {"help":"aos help (syntax: help {command})",
            "clear":"clears the screen (syntax: clear)",
            "echo":"echoes text (syntax: echo [text] {| [color]})",
            "rm":"removes a file (syntax: rm [path from /])",
            "dir":"lists the files and directories inside a directory (syntax: dir [path] {-notypes})",
            "read":"reads a file's contents (syntax: read [file])",
            "script":"runs a script (syntax: script [file] {-v | -verbose})",
            "ver":"shows system and terminal version",
            "term":"restarts terminal (syntax: term)",
            "beep":"plays the current AOS startup sound (syntax: beep)",
            "mkdir":"creates a directory (syntax: mkdir [path])",
            "exec":"executes an app. by default looks in /files/apps. (syntax: exec [file] {path}",
            "restart":"restarts AOS (syntax: restart)"}

class aterm(QWidget):
    def __init__(self):
        super(aterm, self).__init__()
        self.setWindowTitle("AOS-GUI/terminal")
        self.setFixedSize(620, 440)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 400, 521, 31))
        self.lineEdit.setStyleSheet(u"font: 8pt \"Consolas\";")
        self.lineEdit.returnPressed.connect(self.doCommand)

        self.listWidget = QListWidget(self)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 10, 601, 381))
        self.listWidget.setStyleSheet(u"font: 8pt \"Consolas\";")
        self.listWidget.setAutoScroll(False)
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.go = QPushButton(self)
        self.go.setObjectName(u"pushButton")
        self.go.setGeometry(QRect(540, 400, 71, 31))
        self.go.setText("Enter")
        self.go.clicked.connect(self.doCommand)


        self.echo("AOS Terminal v"+str(terminalVer), True)
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
            elif lowcommand.startswith("term"):
                self.listWidget.clear()
                self.echo("AOS Terminal v"+str(terminalVer), True)
                self.echo("Changed dir to /", True)
            elif lowcommand.startswith("beep"):
                try:
                    playsound(getcwd().replace("\\","/")+"/files/system/data/silence.wav")
                    playsound(getcwd().replace("\\","/")+"/files/system/data/AOS.wav")
                except:
                    pass
            elif lowcommand.startswith("mkdir"):
                param = self.splitParams(command)[0]

                try:
                    mkdir(getcwd().replace("\\","/")+"/files/"+param)
                    self.echo("Created directory "+param,True)
                except FileExistsError:
                    self.echo("ERR: Directory already exists!",True)
            elif lowcommand.startswith("exec"):
                params = self.splitParams(command)

                try:
                    openApplication(params[0], params[1])
                except IndexError:
                    openApplication(params[0])
            elif lowcommand.startswith("restart"):
                restart()
            else:
                self.echo("ERR: Unknown command "+lowcommand,True)
                
        except TypeError:
            pass

        except IndexError:
            self.echo("ERR: No arguments provided!", True)
        except Exception as e:
            self.echo("ERR: "+str(e),True)

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