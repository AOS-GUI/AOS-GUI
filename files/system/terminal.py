from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import listdir,path,getcwd,remove,mkdir
from shutil import rmtree
from files.apps.sdk.sdk import *
from playsound import playsound

filesPath = getAOSdir()

variables = {}

waitForInput = False
waitingForVar = ""
inVarName = False

dir = "/home"
terminalVer = 1.4
helpText = {"help":"aos help (syntax: help {command})",
            "clear":"clears the screen (syntax: clear)",
            "echo":"echoes text (syntax: echo [text] {| [color]}). if a variable name is surrounded by graves (`), the variable's contents will be echoed.",
            "rm":"removes a file or folder (syntax: rm [path from /])",
            "dir":"lists the files and directories inside a directory (syntax: dir [path] {-notypes})",
            "read":"reads a file's contents (syntax: read [file])",
            "script":"runs a script (syntax: script [file] {-v | -verbose})",
            "ver":"shows system and terminal version",
            "term":"restarts terminal (syntax: term)",
            "beep":"plays the current AOS startup sound (syntax: beep)",
            "mkdir":"creates a directory (syntax: mkdir [path])",
            "exec":"executes an app. by default looks in /files/apps. (syntax: exec [file] {path}",
            "restart":"restarts AOS (syntax: restart)",
            "mkfile":"creates a file. (syntax: mkfile [path/filename] {contents})",
            "set":"sets a value to a variable (syntax: set [var] [contents]"}

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
        global waitForInput,variables,inVarName,waitingForVar
        try:
            if command == "":
                # if self.lineEdit.text() != False:
                command = self.lineEdit.text()
                self.echo(text="[YOU] "+command,color="__YOU__")
            else:
                if silentOut == False:
                    self.echo("[SCRIPT] "+command)
                
            lowcommand = command.split(" ")[0].lower()

            self.lineEdit.setText("")
            
            if waitForInput == False:
                match lowcommand:
                    case "echo":
                        varname = ""
                        final = ""

                        for i in self.splitParams(command)[0:]:
                            for t in i:
                                if t == "`":
                                    if inVarName == False:
                                        inVarName = True
                                    else:
                                        final += variables[varname]
                                        varname = ""
                                        inVarName = False
                                    continue
                                else:
                                    if inVarName == True:
                                        varname += t
                                    else:
                                        final += t
                            final += " "

                        self.echo(final)

                    case "rm":
                        param = self.splitParams(command)[0]
                        ok = True

                        if param.startswith("/"):
                            param = param.split("/",1)
                            param = param[1]
                            
                        if param.startswith("system"):
                            retval = msgBox(f"'{param}' is a child of or is the 'system' folder, which contains vital system files. Are you sure you want to delete it?","Are you sure?",QMessageBox.Warning,QMessageBox.Yes|QMessageBox.No)
                            if retval != 16384:
                                ok = False

                        if param.endswith("/"):
                            if ok == True:
                                try:
                                    rmtree((filesPath+param))
                                except FileNotFoundError:
                                    self.echo("ERR: The directory doesn't exist!",True)

                        else:
                            if ok == True:
                                try:
                                    remove((filesPath+param))
                                except FileNotFoundError:
                                    self.echo("ERR: The file or directory doesn't exist!",True)
                                except NotADirectoryError:
                                    self.echo(f"ERR: File not found! Are you sure it's not a directory?",True)

                    case "dir":
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

                                for _ in listdir(filesPath+param):
                                    if lowcommand.__contains__("-notypes"):
                                        self.echo(_)
                                    else:
                                        if path.isdir(filesPath+param+_):
                                            self.echo(_+" [DIR]")
                                        elif path.isfile(filesPath+param+_):
                                            self.echo(_+" [FILE]")
                                        elif path.islink(filesPath+param+_):
                                            self.echo(_+" [LINK]")
                                        elif path.ismount(filesPath+param+_):
                                            self.echo(_+" [MNT]")
                                self.echo()
                            except FileNotFoundError:
                                self.echo("ERR: Directory not found!")

                        except NotADirectoryError:
                            self.echo("ERR: "+param+" is not a directory!", True)

                    case "read":
                        param = self.splitParams(command)[0]
                        if param.startswith("/"):
                            param = param.split("/",1)
                            param = param[1]

                        try:
                            curline = 0

                            self.echo(f"[READ] Reading {param}...")
                            f = open(filesPath+param,"r")
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

                    case "clear":
                        self.listWidget.clear()
                    case "help":
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
                                self.echo(helpText[(self.splitParams(command)[0]).lower()],True,helpText=True)
                            except KeyError:
                                self.echo("Command "+self.splitParams(command)[0]+" not found!")
                    case "script":
                        param = self.splitParams(command)[0]
                        silentOut = True

                        if lowcommand.__contains__("-v") or lowcommand.__contains__("-verbose"):
                            self.echo("[SCRIPT] Running script "+param+"...")
                            silentOut = False

                        self.echo()

                        try:
                            script = open(filesPath+param,"r")
                            script = script.read()
                            script = script.split("\n")

                            i = 0
                            
                            while i < len(script):
                                if waitForInput != True:
                                    self.doCommand(script[i],silentOut)
                                    i += 1
                            # multithreading
                                    
                        except OSError as e:
                            self.echo(f"ERR: {e}")
                    case "ver":
                        z = open(getcwd().replace("\\","/")+"/files/system/data/version","r")
                        self.echo("AOS v"+z.read()+". Terminal v"+str(terminalVer)+".",True)
                        z.close()
                    case "term":
                        self.listWidget.clear()
                        self.echo("AOS Terminal v"+str(terminalVer), True)
                        self.echo("Changed dir to /", True)
                    case "beep":
                        try:
                            playsound(getcwd().replace("\\","/")+"/files/system/data/silence.wav")
                            playsound(getcwd().replace("\\","/")+"/files/system/data/AOS.wav")
                        except:
                            pass
                    case "mkdir":
                        param = self.splitParams(command)[0]

                        try:
                            mkdir(filesPath+param)
                            self.echo("Created directory "+param,True)
                        except FileExistsError:
                            self.echo("ERR: Directory already exists!",True)
                    case "exec":
                        params = self.splitParams(command)

                        try:
                            openApplication(params[0], params[1])
                        except IndexError:
                            openApplication(params[0])
                    case "restart":
                        restart()
                    case "mkfile":
                        params = self.splitParams(command)

                        try:
                            f = open(filesPath+params[0],"w+")
                            f.write(" ".join(params[1:]))
                            f.close()
                        except IndexError:
                            f = open(filesPath+params[0],"w+")
                            f.close()
                        
                        self.echo("Created file "+params[0],True)
                    case "set":
                        params = self.splitParams(command)

                        try:
                            variables[params[0]] = " ".join(params[1:])
                        except IndexError:
                            variables[params[0]] = ""
                    # elif lowcommand.startswith("input"):
                    #     params = self.splitParams(command)
                    #     waitForInput = True
                    #     waitingForVar = params[0]

                    #     try:
                    #         self.echo("[INPUT] "+" ".join(params[1:]))
                    #     except IndexError:
                    #         pass

                    case _:
                        self.echo("ERR: Unknown command "+lowcommand,True)
            else:
                waitForInput = False
                variables[waitingForVar] = command
                waitingForVar = ""
                
        except TypeError:
            pass

        except IndexError:
            self.echo("ERR: No arguments provided!", True)
        except Exception as e:
            self.echo("ERR: "+str(e),True)

    def echo(self, text="", fromSys=False, color="white", helpText=False):
        if color != "__YOU__" and not helpText:
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