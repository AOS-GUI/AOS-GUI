from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import listdir,path,getcwd,remove,mkdir,makedirs
from shutil import rmtree
from files.apps.sdk.sdk import *
from playsound import playsound
import requests

filesPath = getAOSdir()

variables = {}

waitForInput = False
waitingForVar = ""
inVarName = False
updatedCamel = False

dir = "/home"
terminalVer = 1.6
helpText = {"help":"aos help (syntax: help {command})",
            "clear":"clears the screen (syntax: clear)",
            "echo":"echoes text (syntax: echo [text] {| [color]}). if a variable name is surrounded by graves (`), the variable's contents will be echoed.",
            "rm":"removes a file or folder (syntax: rm [path from /])",
            "dir":"lists the files and directories inside a directory (syntax: dir [path] {-n | --notypes})",
            "read":"reads a file's contents (syntax: read [file])",
            "script":"runs a script (syntax: script [file] {-v | -verbose})",
            "ver":"shows system and terminal version",
            "term":"restarts terminal (syntax: term)",
            "beep":"plays the current AOS startup sound (syntax: beep)",
            "mkdir":"creates a directory (syntax: mkdir [path])",
            "exec":"executes an app. by default looks in /files/apps. (syntax: exec [file] {path}",
            "restart":"restarts AOS (syntax: restart)",
            "mkfile":"creates a file. (syntax: mkfile [path/filename] {contents})",
            "set":"sets a value to a variable (syntax: set [var] [contents]",
            "py":"executes a python script (syntax: py [path])",
            "camel":"camelInstall CLI. run 'camel help' for more information",
            "dl":"downloads the contents of a url (syntax: dl [url] {output file path} {-s | --status})"}

class aterm(QWidget):
    def __init__(self):
        super(aterm, self).__init__()

        theme = getTheme()

        self.setWindowTitle("AOS-GUI/terminal")
        self.setFixedSize(620, 440)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 400, 521, 31))
        self.lineEdit.setStyleSheet(f"font: 8pt \"Consolas\"; color:{theme[0]}; background-color: {theme[1]}")
        self.lineEdit.returnPressed.connect(self.doCommand)

        self.listWidget = QListWidget(self)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 10, 601, 381))
        self.listWidget.setStyleSheet(f"font: 8pt \"Consolas\"; color:white; background-color: black")
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
                command = self.parseString(command)
            else:
                if silentOut == False:
                    self.echo("[SCRIPT] "+command)
                command = self.parseString(command)
                
            lowcommand = command.lower()

            self.lineEdit.setText("")
            
            if waitForInput == False:
                if lowcommand.startswith("echo"):
                    final = " ".join(self.splitParams(command)[0:])

                    if final:
                        self.echo(final)
                    else:
                        raise IndexError

                elif lowcommand.startswith("rm"):
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

                            for _ in listdir(filesPath+param):
                                if "--notypes" in lowcommand or "-n" in lowcommand:
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

                elif lowcommand.startswith("read"):
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
                            self.echo(helpText[(self.splitParams(command)[0]).lower()],True,helpText=True)
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
                        script = open(filesPath+param,"r")
                        script = script.read()
                        script = script.split("\n")
                        script = list(filter(None, script))

                        i = 0
                        
                        while i < len(script):
                            if waitForInput != True:
                                self.doCommand(script[i],silentOut)
                                i += 1
                                
                    except OSError as e:
                        self.echo(f"ERR: {e}")
                elif lowcommand.startswith("ver"):
                    z = open(getcwd().replace("\\","/")+"/files/system/data/version","r")
                    self.echo("AOS v"+z.read()+". Terminal v"+str(terminalVer)+".",True)
                    z.close()
                elif lowcommand.startswith("term"):
                    self.listWidget.clear()
                    variables = {}
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
                        mkdir(filesPath+param)
                        self.echo("Created directory "+param,True)
                    except FileExistsError:
                        self.echo("ERR: Directory already exists!",True)
                elif lowcommand.startswith("exec"):
                    params = self.splitParams(command)

                    try:
                        if not params[1].endswith("/"):
                            params[1] = params[1]+"/"

                        openApplication(params[0], "files/"+params[1])
                    except IndexError:
                        openApplication(params[0])
                elif lowcommand.startswith("restart"):
                    restart()
                elif lowcommand.startswith("mkfile"):
                    params = self.splitParams(command)

                    try:
                        f = open(filesPath+params[0],"w+")
                        f.write(" ".join(params[1:]))
                        f.close()
                    except IndexError:
                        f = open(filesPath+params[0],"w+")
                        f.close()
                    
                    self.echo("Created file "+params[0],True)
                elif lowcommand.startswith("set"):
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
                elif lowcommand.startswith("py"):
                    param = self.splitParams(command)[0]
                    
                    f = open(filesPath+param,"r")
                    data = f.read()
                    exec(data)
                    f.close()

                elif lowcommand.startswith("camel"):
                    global updatedCamel,filesOnlineNames,filesOnlineDescs,filesOnlineUrls,filesOnlineVers
                    params = self.splitParams(command)

                    if updatedCamel == False:
                        r = requests.get("https://raw.githubusercontent.com/AOS-GUI/cInstall/main/dl/appList.txt",timeout=5)
                        filesOnline = r.text.splitlines(False)

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

                        self.echo("[CAMEL] Updated app list!")

                        updatedCamel = True
                    
                    if updatedCamel:
                        if params[0] == "update":
                            r = requests.get("https://raw.githubusercontent.com/AOS-GUI/cInstall/main/dl/appList.txt",timeout=5)
                            filesOnline = r.text.splitlines(False)

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

                            self.echo("[CAMEL] Updated app list!")

                        elif params[0] == "install":
                            self.echo("[CAMEL] Checking catalog for "+params[1]+"...")
                            if params[1] in filesOnlineNames:
                                self.echo("[CAMEL] Package found and delivered! Unpacking...")

                                urls = filesOnlineUrls[filesOnlineNames.index(params[1])]
                                
                                self.echo()
                                for url in urls.split(";"):
                                    self.listWidget.takeItem(self.listWidget.count()-1)
                                    self.echo("[CAMEL] Unpacking "+url.split("/")[-1]+"...")

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
                                        url = "https://aos-gui.github.io/cInstall/dl/assets/"+params[1].split(".py")[0]+"/"+url

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
                                        makedirs(path.dirname(getcwd().replace("\\","/")+"/files/apps/"+newUrl), exist_ok=True)
                                        f = open(getcwd().replace("\\","/")+"/files/apps/"+newUrl,"wb")
                                    
                                        f.write(r.content)
                                        f.close()

                                    self.listWidget.takeItem(self.listWidget.count()-1)
                                    self.echo("[CAMEL] Unpacked "+newUrl.split("/")[-1]+"!")
                                
                                self.echo("[CAMEL] Finished unpacking "+params[1]+"!")
                        elif params[0] == "uninstall":
                            item = params[1]
                            try:
                                self.echo("[CAMEL] Repacking "+params[1]+"...")

                                if not item.endswith(".py"):
                                    item = item+".py"
                                remove(getcwd().replace("\\","/")+"/files/apps/"+item)

                                item = item.split(".py")[0]

                                try:
                                    rmtree(getcwd().replace("\\","/")+"/files/apps/assets/"+item+"/")
                                except Exception as e:
                                    print(e)

                                self.echo("[CAMEL] Sold "+params[1]+"!")
                            except FileNotFoundError:
                                self.echo("[CAMEL] "+params[1]+" doesn't exist!")
                        elif params[0] == "list":
                            extraThing = ""
                            try:
                                if params[1] == "-i" or params[1] == "--installed":
                                    extraThing = " (local)"
                            except IndexError:
                                pass

                            self.echo("[CAMEL] Package list"+extraThing+":")
                            self.echo("[CAMEL]")
                            if extraThing:
                                filepath = "files/apps/"
                                files = []
                                row = 0

                                for file in listdir(filepath):
                                    if path.isfile(path.join(filepath, file)):
                                        files.append(file)

                                for name in sorted(files):
                                    f = open(f"{filepath}{name}","r")

                                    try:
                                        content = f.read()
                                        content = content.split("#~")
                                        pkginfo = content[1].split("|")
                                        pkginfo[2] = pkginfo[2].split("\n")[0]

                                        self.echo("[CAMEL] "+pkginfo[0]+" - "+pkginfo[1])
                                    except:
                                        self.echo(f"[WARN] camel couldn't find info for the app ({name}), getting info from package name")
                                        self.echo("[CAMEL] "+name+" - "+filesOnlineDescs[filesOnlineNames.index(i)])
                                    f.close()
                            else:
                                for i in filesOnlineNames:
                                    self.echo("[CAMEL] "+i+" - "+filesOnlineDescs[filesOnlineNames.index(i)])
                        elif params[0] == "info":
                            if params[1] in filesOnlineNames:
                                installed = "no"
                                if params[1]+".py" in listdir("files/apps/"):
                                    installed = "yes"
                                self.echo("[CAMEL] Information for package "+params[1]+":")
                                self.echo("[CAMEL]")
                                self.echo("[CAMEL] Description: "+filesOnlineDescs[filesOnlineNames.index(params[1])])
                                self.echo("[CAMEL] URL: "+filesOnlineUrls[filesOnlineNames.index(params[1])])
                                self.echo("[CAMEL] Version: "+filesOnlineVers[filesOnlineNames.index(params[1])])
                                self.echo("[CAMEL] Installed: "+installed)
                            else:
                                if params[1]+".py" in listdir("files/apps/"):
                                    f = open(f"files/apps/{params[1]}.py","r")

                                    try:
                                        content = f.read()
                                        content = content.split("#~")
                                        pkginfo = content[1].split("|")
                                        pkginfo[2] = pkginfo[2].split("\n")[0]
                                    except:
                                        self.echo(f"[WARN] camel couldn't find info for the app ({params[1]}), getting info from package name")
                                    f.close()

                                    self.echo("[CAMEL] Information for local package "+params[1]+":")
                                    self.echo("[CAMEL]")
                                    self.echo("[CAMEL] Description: "+str(pkginfo[1]))
                                    self.echo("[CAMEL] URL: None")
                                    self.echo("[CAMEL] Version: "+str(pkginfo[2]))
                                    self.echo("[CAMEL] Installed: yes")
                                else:
                                    self.echo("[CAMEL] Package not found!")
                        elif params[0] == "search":
                            self.echo("[CAMEL] Searching...")
                            results = []

                            for i in filesOnlineNames:
                                if " ".join(params[1:]) in i:
                                    results.append(i+" - "+filesOnlineDescs[filesOnlineNames.index(i)])

                            for i in filesOnlineDescs:
                                if " ".join(params[1:]) in i:
                                    results.append(filesOnlineNames[filesOnlineDescs.index(i)]+" - "+i)
                            
                            results = list(dict.fromkeys(results))

                            self.echo("[CAMEL] Results:")
                            
                            for i in results:
                                self.echo("[CAMEL] "+i)

                        elif params[0] == "help":
                            for n in ["-- camelInstall CLI help --",
                                         "",
                                         "update - updates package list. this is run automatically on first command use",
                                         "install <package name> - install package",
                                         "info <package name> - package information",
                                         "list [-i / --installed] - lists all packages on the server (if -i is found, lists local packages)",
                                         "search <package name or description> - searches for the specified package or package matching the description in the database",
                                         "uninstall <package name> - uninstall package"
                                         ]:
                                self.echo("[CAMEL] "+n)
                elif lowcommand.startswith("dl"):
                    params = self.splitParams(command)
                    if params[0]:
                        if "http://" not in params[0]:
                            params[0] = "http://"+params[0]
                        r = requests.get(params[0])

                        try:
                            if "-s" in params or "--status" in params:
                                self.echo("[DL] status: "+str(r.status_code))

                            if params[1] == "-s" or params[1] == "--status":
                                params[1] = params[2]

                            f = open(getAOSdir()+params[1],"wb")
                            f.write(r.content)
                            f.close()
                        except IndexError:
                            try:
                                for i in r.content.decode().split("\n"):
                                    self.echo(i)
                            except Exception as e:
                                self.echo(e)
                else:
                    self.echo("ERR: Unknown command "+lowcommand,True)
            else:
                waitForInput = False
                variables[waitingForVar] = command
                waitingForVar = ""
                
        except TypeError:
            pass

        except IndexError:
            try:
                self.echo(helpText[command.lower()],True,helpText=True)
            except KeyError:
                self.echo("Command "+self.splitParams(command)[0]+" not found!")
        except Exception as e:
            self.echo("ERR: "+str(e),True)
    

    def echo(self, text="", fromSys=False, color="white", helpText=False):
        if self.listWidget.count() == 500:
            self.listWidget.takeItem(0)

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

        self.update()
        self.repaint()

    def parseString(self, text):
        varname = ""
        final = ""
        inVarName = False

        for t in text:
            if t == "`":
                if inVarName == False:
                    inVarName = True
                else:
                    try:
                        final += variables[varname]
                        varname = ""
                        inVarName = False
                    except KeyError:
                        self.echo("ERR: No variable named "+varname,True)
                continue
            else:
                if inVarName == True:
                    varname += t
                else:
                    final += t
        # final += " "

        return final
    
    def splitParams(self, text):
        try:
            text = text.split(" ")
            text = text[1:]
            return text
        except IndexError:
            text = text.split(" ")
            text = text[1]
            return text
