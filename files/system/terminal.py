from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import listdir,path,getcwd,remove,mkdir,makedirs
import sys
from shutil import rmtree
from playsound import playsound
import requests
import re

from files.apps.sdk.sdk import *

filesPath = getAOSdir()

variables = {}
aliases = {}

waitForInput = False
waitingForVar = ""
inVarName = False
allowColor = True
maxLines = 500
allowEcho = True

camel = Camel()

dir = "/"
dirstack = []
terminalVer = 1.8
helpText = {"help":"aos help (syntax: help {command})",
            "clear":"clears the screen (syntax: clear)",
            "echo":"echoes text (syntax: echo [text] {| [color]}). if a variable name is surrounded by graves (`), the variable's contents will be echoed.",
            "rm":"removes a file or folder (syntax: rm [file/folder] {-y | --yes})",
            "dir":"lists the files and directories inside a directory (syntax: dir {path} {-n | --notypes})",
            "read":"reads a file's contents (syntax: read [file] {-n | --nolinenum})",
            "script":"runs a script (syntax: script [file] {-v | --verbose})",
            "ver":"shows system and terminal version",
            "term":"restarts terminal (syntax: term)",
            "beep":"plays the current AOS startup sound (syntax: beep)",
            "mkdir":"creates a directory (syntax: mkdir [path])",
            "exec":"executes an app. (syntax: exec [file] {path})",
            "restart":"restarts AOS (syntax: restart)",
            "mkfile":"creates a file. (syntax: mkfile [path/filename] {contents})",
            "set":"sets a value to a variable (syntax: set [var] {contents}",
            "py":"executes a python script (syntax: py [path])",
            "camel":"camelInstall CLI. run 'camel help' for more information",
            "dl":"downloads the contents of a url (syntax: dl [url] {output file path} {-s | --status})",
            "cd":"changes current working directory (syntax: cd {path} {-v | --verbose})",
            "alias":"creates an alias for a command, or if no name is given shows all current aliases (syntax: alias {name} {command})",
            "color":"enables or disables color (syntax: color {1 | 0 | true | false})",
            "note":"a line omitted from execution, mainly used for scripting (similar to # in Python or Bash) (syntax: note {text})",
            "edit":"opens the AOS editor. if 'file' is given and does not exist, creates the file and opens it. (syntax: edit {file})"}


class aterm(QWidget):
    def __init__(self):
        super(aterm, self).__init__()

        theme = getTheme()

        self.setWindowTitle("AOS-GUI/terminal")
        self.setFixedSize(620, 440)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 400, 600, 31))
        self.lineEdit.setStyleSheet(f"font: 8pt \"Consolas\"; color:{theme[0]}; background-color: {theme[1]}")
        self.lineEdit.returnPressed.connect(self.doCommand)

        self.listWidget = QListWidget(self)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 10, 601, 381))
        self.listWidget.setStyleSheet(f"font: 8pt \"Consolas\"; color:white; background-color: black")
        self.listWidget.setAutoScroll(False)
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.listWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.echo("AOS Terminal v"+str(terminalVer), True)
        self.echo("null -> /", True)

        try:
            with open(getAOSdir()+"/system/data/user/terminal.aos","r") as f:
                for i in f.read().strip("\n").split("\n"):
                    self.doCommand(i,True)
        except FileNotFoundError:
            pass
    
    def doCommand(self, command="",silentOut=False):
        global aliases,waitForInput,variables,inVarName,waitingForVar,dir,dirstack,allowColor,maxLines,allowEcho

        variables["%DIR"] = dir
        variables["%DIRSTACK"] = str(dirstack)
        variables["%ECHO"] = str(allowEcho)
        variables["%COLOR"] = str(allowColor)
        variables["%MAXLINES"] = str(maxLines)
        variables["%SPLASH"] = "[random splash]"

        varsVar = variables.copy()
        if "%VARS" in varsVar:
            varsVar.pop("%VARS")
        variables["%VARS"] = str(varsVar)

        try:
            if command == "":
                command = self.lineEdit.text()
                if command != "" and not command.isspace():
                    self.echo(text="[YOU] "+command,color="__YOU__")
                    command = self.parseString(command)
                else:
                    return
            elif command.strip() == "":
                return
            else:
                if silentOut == False:
                    self.echo("[SCRIPT] "+command.replace("|","||"),color="cyan")
                command = self.parseString(command)
                
            lowcommand = command.lower().split(" ")[0]

            self.lineEdit.setText("")
            
            if lowcommand == "echo":
                final = " ".join(self.splitParams(command)[0:])

                if final:
                    self.echo(final)
                else:
                    raise IndexError

            elif lowcommand == "rm":
                params = self.splitParams(command)
                param = params[0]
                ok = True

                if param.startswith("/"):
                    param = param.split("/",1)
                    param = param[1]
                    
                if param.startswith("system") or dir.startswith("/system/"):
                    if not ("-y" in params or "--yes" in params):
                        retval = msgBox(f"'{param}' is a child of or is the 'system' folder, which contains vital system files. Are you sure you want to delete it?","Are you sure?",QMessageBox.Warning,QMessageBox.Yes|QMessageBox.No)
                        if retval != 16384:
                            ok = False

                if param.endswith("/"):
                    if ok == True:
                        try:
                            rmtree((filesPath+dir+param))
                            self.echo("removed directory "+dir+param,fromSys=True)
                        except FileNotFoundError:
                            self.echo("ERR: The directory doesn't exist!",True,color="red")

                else:
                    if ok == True: # terrible code, but it works so ok
                        try:
                            remove((filesPath+dir+param))
                            self.echo("removed file "+dir+param,fromSys=True)
                        except FileNotFoundError:
                            self.echo("ERR: The file or directory doesn't exist!",True,color="red")
                        except NotADirectoryError:
                            self.echo(f"ERR: File not found! Are you sure it's not a directory?",True,color="red")

            elif lowcommand == "dir":
                try:
                    params = self.splitParams(command)
                    param = params[0]

                    if param == "-n" or param == "--notypes":
                        params[1] = "-n"
                        param = dir
                    else:
                        if param.startswith("/"):
                            if param != "/":
                                param = param.split("/",1)
                                param = param[1]

                        if not param.endswith("/"):
                            param = param+"/"

                        param = dir+param
                except IndexError:
                    param = dir

                try:
                    try:
                        param = param.replace("//","/")
                        self.echo("List of files/directories in "+param+":")
                        self.echo()

                        for _ in listdir(filesPath+param):
                            append = ""
                            if path.isdir(filesPath+param+_):
                                append = "/"

                            if "--notypes" in params or "-n" in params:
                                pass
                            else:
                                if path.isfile(filesPath+param+_):
                                    append = " [FILE]"
                                elif path.isdir(filesPath+param+_):
                                    append += " [DIR]"
                                elif path.islink(filesPath+param+_):
                                    append = " [LINK]"
                                elif path.ismount(filesPath+param+_):
                                    append = " [MNT]"

                            self.echo(_+append)
                        self.echo()
                    except FileNotFoundError:
                        self.echo("ERR: Directory not found!",color="red")

                except NotADirectoryError:
                    self.echo("ERR: "+param+" is not a directory!", True,color="red")

            elif lowcommand == "read":
                linenums = True
                params = self.splitParams(command)
                param = dir+params[0].strip("/")

                try:
                    if params[1] == "-n" or params[1] == "--nolinenum":
                        linenums = False
                except IndexError:
                    pass

                try:
                    curline = 0

                    self.echo(f"[READ] Reading {param}...")
                    f = open(filesPath+param,"r")
                    textInFile = f.readlines()
                    self.echo(f"[READ] Got {len(textInFile)} lines!",color="green")
                    self.echo()
                    for l in textInFile:
                        l = l.strip("\n")
                        curline += 1
                        if linenums:
                            self.echo(f"[READ:{curline}] {l}",color="__YOU__")
                        else:
                            self.echo(l,color="__YOU__")
                
                except FileNotFoundError:
                    self.echo("ERR: File not found!",True,color="red")
                except PermissionError:
                    self.echo("ERR: File not found! Did you try to read a directory?",True,color="red")

            elif lowcommand == "clear":
                self.listWidget.clear()
            elif lowcommand == "help":
                try:
                    param = self.splitParams(command)[0].lower()
                    try:
                        self.echo(helpText[param],True,helpText=True)
                    except KeyError:
                        self.echo("Command "+helpText[param]+" not found!")
                except IndexError:
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
                    
            elif lowcommand == "script":
                try:
                    newdir = dir
                    params = self.splitParams(command)
                    if params[0].startswith("/"):
                        newdir = "/"
                    params[0] = newdir+params[0].strip("/")
                    silentOut = True

                    if len(params) == 2 and (params[1] == "-v" or params[1] == "--verbose"):
                        self.echo("[SCRIPT] Running script "+params[0]+"...",color="cyan")
                        silentOut = False

                    self.echo()

                    try:
                        script = open(filesPath+params[0],"r")
                        script = script.read()
                        script = re.split("\n|;",script)
                        script = list(filter(None, script))

                        i = 0
                        
                        while i < len(script):
                            if waitForInput != True:
                                self.doCommand(script[i],silentOut)
                                i += 1
                                
                    except OSError as e:
                        self.echo(f"ERR: {e}",color="red")
                except Exception as e:
                    self.echo("[SCRIPT] ERR: "+str(e))
            elif lowcommand == "ver":
                z = open(getAOSdir()+"/system/data/version","r")
                self.echo("AOS v"+z.read()+". Terminal v"+str(terminalVer)+".",True)
                z.close()
            elif lowcommand == "term":
                self.listWidget.clear()
                dir = "/"
                dirstack = []
                variables = {}
                aliases = {}

                waitForInput = False
                waitingForVar = ""
                inVarName = False
                allowColor = True
                maxLines = 500
                allowEcho = True
                
                self.echo("AOS Terminal v"+str(terminalVer), True)
                self.echo("null -> /", True)

                try:
                    with open(getAOSdir()+"/system/data/user/terminal.aos","r") as f:
                        for i in f.readlines():
                            self.doCommand(i,True)
                except FileNotFoundError:
                    pass
            elif lowcommand == "beep":
                try:
                    self.echo("[BEEP] beeping...")
                    playsound(getAOSdir()+"/system/data/silence.wav")
                    playsound(getAOSdir()+"/system/data/AOS.wav")
                    self.echo("[BEEP] beeped successfully!",color="green")
                except Exception as e:
                    self.echo("[BEEP]: ERR: "+str(e),color="red")
            elif lowcommand == "mkdir":
                param = self.splitParams(command)[0]

                param = dir+param.strip("/")

                try:
                    mkdir(filesPath+param)
                    self.echo("Created directory "+param,True)
                except FileExistsError:
                    self.echo("ERR: Directory already exists!",True,color="red")
            elif lowcommand == "exec":
                params = self.splitParams(command)

                try:
                    params[1] = dir+params[1].strip("/")
                except Exception as e:
                    pass

                try:
                    ret, err = openApplication(params[0], "files"+params[1]+"/")
                    if err:
                        self.echo("[EXEC] ERR: "+str(err),color="red")
                except IndexError:
                    ret, err = openApplication(params[0], "files/"+(dir.strip("/"))+"/")
                    if err:
                        self.echo("[EXEC] ERR: "+str(err),color="red")
            elif lowcommand == "restart":
                restart()
            elif lowcommand == "mkfile":
                params = self.splitParams(command)
                params[0] = dir+params[0].strip("/")

                try:
                    f = open(filesPath+params[0],"w+")
                    f.write(" ".join(params[1:]))
                    f.close()
                except IndexError:
                    f = open(filesPath+params[0],"w+")
                    f.close()
                
                self.echo("Created file "+params[0],True)
            elif lowcommand == "set":
                params = self.splitParams(command)
                passed = True
                try:
                    orig = variables[params[0]]
                except KeyError:
                    orig = "(null)"

                try:
                    variables[params[0]] = " ".join(params[1:])
                    if params[0] == "%MAXLINES":
                        try:
                            variables[params[0]] = int(params[1])
                            maxLines = int(params[1])
                        except Exception as e:
                            self.echo("[SET] ERR: cannot set environment variable %MAXLINES to string",color="red")
                            passed = False
                    elif params[0] == "%ECHO":
                        try:
                            variables[params[0]] = toBool(params[1])
                            allowEcho = toBool(params[1])
                        except Exception as e:
                            self.echo("[SET] ERR: cannot set environment variable %ECHO to string",color="red")

                        passed = False
                except IndexError:
                    variables[params[0]] = ""

                if passed:
                    self.echo("[SET] "+params[0]+": "+str(orig)+" -> "+str(variables[params[0]]))
            elif lowcommand == "py":
                param = self.splitParams(command)[0]
                param = dir+param.strip("/")
                
                f = open(filesPath+param,"r")
                data = f.read()
                try:
                    exec(data)
                    self.echo("[PY] script completed.",color="green")
                except Exception as e:
                    self.echo("[PY] ERR in script: "+str(e),color="red")
                f.close()

            elif lowcommand == "camel":
                global camel

                def updateStuff():
                    ret, err = camel.update()
                        
                    if ret == -1:
                        self.echo("[CAMEL] ERR: Could not gather app list! "+str(err),color="red")
                    else:
                        self.echo("[CAMEL] Updated app list!")

                        outdateds = verCheck()

                        if outdateds:
                            self.echo("[CAMEL] WARN: Some of your apps are outdated: ",color="yellow")
                            for i in outdateds:
                                self.echo(f"  - {i[0]} (local: {i[1]}, server: {i[2]})",color="yellow")
                            self.echo()
                            self.echo("[CAMEL] Please upgrade if you care! (run 'camel upgrade')",color="yellow")

                def verCheck():
                    global camel
                    v = camel.getVersions()
                    n = camel.getNames()
                    outdateds = []

                    for i in range(len(camel.getVersions())):
                        try:
                            f = open(f"files/apps/{n[i]}.py","r")

                            try:
                                content = f.read()
                                content = content.split("#~")
                                pkginfo = content[1].split("|")
                                pkginfo[2] = pkginfo[2].split("\n")[0]

                                if compareVersion(pkginfo[2], v[i]) == -1:
                                    outdateds.append([n[i],pkginfo[2],v[i]])
                            except Exception as e:
                                self.echo("[CAMEL] ERR: "+str(e),color="red")
                        except FileNotFoundError:
                            pass
                    return outdateds

                params = self.splitParams(command)

                if camel.isUpdated() == False:
                    updateStuff()
                
                if camel.isUpdated():
                    if params[0] == "update":
                        updateStuff()
                    elif params[0] == "upgrade":
                        self.echo("[CAMEL] Upgrading...")

                        p = verCheck()

                        if p:
                            for i in p:
                                self.echo("[CAMEL] Upgrading package "+i[0]+"...")
                                camel.install(i[0])
                                self.listWidget.addItem(self.listWidget.takeItem(self.listWidget.count()-1).text()+"done!")
                                self.colorLine(self.listWidget.count()-1,color="green")
                            self.echo("[CAMEL] Finished upgrading packages!",color="green")
                        else:
                            self.echo("[CAMEL] No packages need upgrading! :)",color="green")

                    elif params[0] == "install":
                        for package in params[1:]:
                            self.echo("[CAMEL] Checking catalog for "+package+"...")
                            if package in camel.pkgnames:
                                self.echo("[CAMEL] Package found and delivered! Unpacking...")

                                camel.install(package)
                                
                                self.echo("[CAMEL] Finished unpacking "+package+"!",color="green")
                            else:
                                self.echo("[CAMEL] ERR: No package found!",color="red")
                    elif params[0] == "uninstall":
                        for package in params[1:]:
                            ret,err = camel.uninstall(package)
                            if ret != -1:
                                self.echo("[CAMEL] Uninstalled "+package+"!",color="green")
                            else:
                                self.echo("[CAMEL] ERR: "+err,color="red")
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
                                    self.echo(f"[WARN] camel couldn't find info for the app ({name}), getting info from package name",color="yellow")
                                    self.echo("[CAMEL] "+name+" - "+camel.getDescs()[camel.getNames().index(i)])
                                f.close()
                        else:
                            for i in camel.getNames():
                                self.echo("[CAMEL] "+i+" - "+camel.getDescs()[camel.getNames().index(i)])
                    elif params[0] == "info":
                        if params[1] in camel.getNames():
                            installed = "no"
                            if params[1]+".py" in listdir("files/apps/"):
                                installed = "yes"
                            self.echo("[CAMEL] Information for package "+params[1]+":")
                            self.echo("[CAMEL]")
                            self.echo("[CAMEL] Description: "+camel.getDescs()[camel.getNames().index(params[1])])
                            self.echo("[CAMEL] URL: "+camel.getURLs()[camel.getNames().index(params[1])])
                            self.echo("[CAMEL] Version: "+camel.getVersions()[camel.getNames().index(params[1])])
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
                                    self.echo(f"[WARN] camel couldn't find info for the app ({params[1]}), getting info from package name",color="yellow")
                                f.close()

                                self.echo("[CAMEL] Information for local package "+params[1]+":")
                                self.echo("[CAMEL]")
                                self.echo("[CAMEL] Description: "+str(pkginfo[1]))
                                self.echo("[CAMEL] URL: None")
                                self.echo("[CAMEL] Version: "+str(pkginfo[2]))
                                self.echo("[CAMEL] Installed: yes")
                            else:
                                self.echo("[CAMEL] ERR: Package not found!",color="red")
                    elif params[0] == "search":
                        self.echo("[CAMEL] Searching...")
                        results = []
                        
                        try:
                            for i in camel.getNames():
                                if " ".join(params[1:]) in i:
                                    results.append(i+" - "+camel.getDescs()[camel.getNames().index(i)])

                            for i in camel.getDescs():
                                if " ".join(params[1:]) in i:
                                    results.append(camel.getNames()[camel.getDescs().index(i)]+" - "+i)
                            
                            results = list(dict.fromkeys(results))

                            self.echo("[CAMEL] Results:")
                            
                            for i in results:
                                self.echo("[CAMEL] "+i)
                        except Exception as e:
                            self.echo("[CAMEL] ERR: "+str(e),color="red")

                    elif params[0] == "help":
                        for n in ["-- camelInstall CLI help --",
                                        "",
                                        "update - updates package list. this is run automatically on first command use",
                                        "upgrade - upgrades all packages that are outdated",
                                        "install <package> [package2...] - install package(s)",
                                        "info <package> - package information",
                                        "list [-i / --installed] - lists all packages on the server (if -i is found, lists local packages)",
                                        "search <package name or description> - searches for the specified package or package matching the description in the database",
                                        "uninstall <package> [package2...] - uninstall package(s)"
                                        ]:
                            self.echo("[CAMEL] "+n)
                    else:
                        self.echo("[CAMEL] ERR: Invalid subcommand "+params[0],color="red")
            elif lowcommand == "dl":
                params = self.splitParams(command)
                if params[0]:
                    r = requests.get(params[0])

                    try:
                        if "-s" in params or "--status" in params:
                            color = "white"
                            stat = str(r.status_code)
                            if stat == "404":
                                color = "red"
                            elif stat == "200":
                                color = "green"

                            self.echo("[DL] status: "+stat,color=color)

                        if params[1] == "-s" or params[1] == "--status":
                            params[1] = params[2]

                        f = open(getAOSdir()+dir+params[1].strip("/"),"wb")
                        f.write(r.content)
                        f.close()
                    except IndexError:
                        try:
                            for i in r.content.decode().split("\n"):
                                self.echo(i)
                        except Exception as e:
                            self.echo("[DL] ERR: "+str(e),color="red")
            elif lowcommand == "cd":
                success = True
                params = self.splitParams(command)
                verbose = False
                olddir = dir
                try:
                    if params[1] == "-v" or params[1] == "--verbose":
                        verbose = True
                except IndexError:
                    pass

                if params[0].startswith("/"): # could probably make this cleaner, but it works!
                    dir = "/"
                    dirstack = []

                if params[0].strip("/") == ".":
                    pass
                elif params[0] == "/" or params[0] == "~":
                    dir = "/"
                    dirstack = []
                else:
                    if verbose:
                        self.echo("breaking apart directory...",fromSys=True,color="cyan")
                    for i in params[0].strip("/").split("/"):
                        if verbose:
                            self.echo("currently at "+i,fromSys=True,color="cyan")

                        if i == "..":
                            if verbose:
                                self.echo("found a .., moving back",fromSys=True,color="cyan")
                            try:
                                if len(dirstack) == 1:
                                    dir = "/"
                                else:
                                    dir = dirstack.pop()
                            except IndexError:
                                self.echo("WARN: cannot go past /, stopping here",color="yellow")
                        elif i == ".":
                            if verbose:
                                self.echo("path, when simplified, is just a dot lol",fromSys=True,color="cyan")
                            pass
                        else:
                            if path.exists(getAOSdir()+dir+i+"/"):
                                if verbose:
                                    self.echo("path exists, moving in",fromSys=True,color="cyan")
                                dirstack.append(dir)
                                dir = dir+i+"/"
                            else:
                                self.echo("ERR: directory not found: "+dir+i+"/",color="red")
                                success = False

                if success:
                    if verbose:
                        self.echo("successfully changed dirs, finalizing...",fromSys=True,color="cyan")
                    dir = dir.replace("//","/")
                    dirstack = list(dict.fromkeys(dirstack))
                    dirstack = [ x for x in dirstack if not "//" == x ]
                    variables["%DIR"] = dir
                    self.echo(olddir+" -> "+dir,True)
            elif lowcommand == "alias":
                params = self.splitParams(command)

                try:
                    joined = " ".join(params[1:])
                    if joined == "" or joined.isspace():
                        try:
                            aliases.pop(params[0])
                            self.echo("[ALIAS] cleared alias "+params[0])
                        except KeyError:
                            self.echo("[ALIAS] WARN: no alias "+params[0]+" to clear",color="yellow")
                    else:
                        aliases[params[0]] = " ".join(params[1:]).strip()
                        self.echo("[ALIAS] alias "+params[0]+" = "+" ".join(params[1:]))
                        
                except IndexError:
                    self.echo("[ALIAS] aliases:")
                    for i in aliases:
                        self.echo("[ALIAS] "+i+" = "+aliases[i])
            elif lowcommand == "color":
                oldcolor = allowColor
                yesstrs = ["1","true"]
                nostrs = ["0","false"]
                param = self.splitParams(command)[0]
                if param in yesstrs:
                    allowColor = True
                elif param in nostrs:
                    allowColor = False

                self.echo("use color "+str(oldcolor)+" -> "+str(allowColor),True)
            elif lowcommand.startswith("note"):
                pass
            elif lowcommand.startswith("edit"):
                param = self.splitParams(command)[0]
                QProcess.startDetached(sys.executable, ["files/system/edit.py",getAOSdir()+dir+param])
            else:
                if lowcommand in aliases:
                    fullcmd = aliases[lowcommand]
                    params = self.splitParams(command)
                    if params:
                        fullcmd += " "+" ".join(params)
                    self.doCommand(fullcmd,True)
                else:
                    self.echo("ERR: Unknown command "+lowcommand,True,color="red")
                
        except TypeError:
            pass

        except IndexError:
            try:
                self.echo(helpText[command.lower()],True,helpText=True)
            except KeyError:
                self.echo("Command "+self.splitParams(command)[0]+" not found!",True,color="red")
        except Exception as e:
            self.echo("ERR: "+str(e),True,color="red")
        
        # add environment variables for other stuff!

    def echo(self, text="", fromSys=False, color="white", helpText=False, debug=False):
        global allowColor,maxLines,allowEcho

        if allowEcho:
            text = str(text)
            while self.listWidget.count() >= maxLines:
                self.listWidget.takeItem(0)

            if color != "__YOU__" and not helpText:
                origcolor = color
                if "|" in text:
                    try:
                        color = text.split("|")[-1]
                        if color == "":
                            color = origcolor
                        else:
                            text = "|".join(text.split("|")[:-1])
                    except IndexError:
                        color = origcolor

            text = text.replace("||","|")

            if fromSys:
                self.listWidget.addItem("[SYS] "+text)
            elif debug:
                self.listWidget.addItem("[DEBUG] "+text)
            else:
                self.listWidget.addItem(text)
            
            if color != "__YOU__" and allowColor:
                self.listWidget.item(self.listWidget.count()-1).setForeground(QColor(color))

            self.listWidget.scrollToBottom()

            self.update()
            self.repaint()

    def parseString(self, text):
        origtext = text
        varname = ""
        final = ""
        index = 0
        inVarName = False

        for t in text:
            if t == "`":
                if inVarName == False:
                    inVarName = True
                else:
                    try:
                        if varname == "%SPLASH":
                            final += getSplashText()
                        elif varname == "":
                            final += "`"
                        else:
                            final += variables[varname]
                        varname = ""
                        inVarName = False
                    except KeyError:
                        self.echo("ERR: No variable named "+varname,True,color="red")
                continue
            else:
                if inVarName == True:
                    varname += t
                else:
                    final += t
        # final += " "

        if inVarName == True:
            return origtext
        else:
            return final
    
    def splitParams(self, text):
        text = text.strip("\n")
        try:
            text = text.split(" ")
            text = text[1:]
            return text
        except IndexError:
            text = text.split(" ")
            text = text[1]
            return text

    def colorLine(self, line, color="green", fromEnd=False):
        place = line
        if fromEnd == True:
            place = self.listWidget.count()-line-1
        self.listWidget.item(place).setForeground(QColor(color))
