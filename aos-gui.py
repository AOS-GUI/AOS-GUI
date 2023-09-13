#! /bin/python3

#  █████╗  ██████╗ ███████╗       ██████╗ ██╗   ██╗██╗
# ██╔══██╗██╔═══██╗██╔════╝      ██╔════╝ ██║   ██║██║
# ███████║██║   ██║███████╗█████╗██║  ███╗██║   ██║██║
# ██╔══██║██║   ██║╚════██║╚════╝██║   ██║██║   ██║██║
# ██║  ██║╚██████╔╝███████║      ╚██████╔╝╚██████╔╝██║
# ╚═╝  ╚═╝ ╚═════╝ ╚══════╝       ╚═════╝  ╚═════╝ ╚═╝
# by nanobot567 ( and contributors :) )

from sys import argv

if len(argv) > 1:
    if argv[1] == "--classic" or argv[1] == "-c":
        from files.system.aosclassic import aosclassic

        raise SystemExit
    elif argv[1] == "--help":
        print("Usage: aos-gui.py [OPTION]")
        print("Aiden's operating system.")
        print("\nOptions:\n  --classic,-c   use aos classic\n  --help         show this help screen\n")
        raise SystemExit # apparently this is much better than quit()

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

try:
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    import psutil
    from playsound import playsound
    import threading
except ModuleNotFoundError:
    print("Installing AOS-GUI requirements...")
    pipmain(["install", "PyQt5"])
    pipmain(["install", "requests"])
    pipmain(["install", "playsound==1.2.2"])
    pipmain(["install", "psutil"])
    print("Done! Starting up...")
    from files.apps.sdk.sdk import restart
    
    restart()

from files.system import aoshelp, calc, cinstall, edit, fs, launcher, settings, splash, terminal, updater
from files.system.setup import setupAOS
from files.apps.sdk.sdk import *

from time import sleep, strftime
import importlib
import sys
import os
import configparser
import platform

fontSize = 11
buttonFontSize = f"font-size:{fontSize}px"
buttonX = 20
buttonY = 40
buttonSpaceX = 20
buttonSpaceY = 40
buttonWidth = 90
buttonHeight = 50
buttonsShown = []
numShortcuts = 8
guiTheme = ""
qsplash = None

sysApps = ["Settings", "appLauncher", "FileSystem", "camelInstall", "Edit", "AOSHelp", "Terminal", "Calculator"]

kSeqs = []

config = configparser.ConfigParser()
config.read("files/system/data/user/data.aos")

try:
    with open("files/system/data/user/data.aos") as f:
        config.read(f)
except:
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    app.setStyle("Windows")
    window = setupAOS.installform()
    window.show()
    exit(app.exec_())


class AOS(QMainWindow):
    def __init__(self):
        super(AOS, self).__init__()
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setObjectName("MainWindow")

        global textcolor, bgcolor, ttextcolor, tbgcolor, btextcolor, bbgcolor, windowcolor, buttonsShown, \
        theme, username, password, kSeqs, fontSize, buttonFontSize, guiTheme, clockMode, buttonWidth, \
        buttonHeight, buttonSpaceX, buttonSpaceY, qsplash

        themeColors,ret = getTheme()
        if ret == -1:
            print("!! WARNING: Theme "+config["theme"]["name"]+" not found, using default-dark...")

        username = config["userinfo"]["name"]
        password = config["userinfo"]["pass"]
        fontSize = config.getint("fontsize", "size")
        buttonFontSize = f"font-size:{fontSize}px"
        for i in config["shortcuts"]:
            kSeqs.append(i)
        textcolor = themeColors[0]
        bgcolor = themeColors[1]
        ttextcolor = themeColors[3]
        tbgcolor = themeColors[2]
        btextcolor = themeColors[5]
        bbgcolor = themeColors[4]
        windowcolor = themeColors[6]

        buttonsShown = []

        for i in config["desktopApps"].values():
            buttonsShown.append(i)

        guiTheme = config["guitheme"]

        clockMode = config.getboolean("24hrclock", "24hour")

        buttonWidth = config.getint("buttonDims", "w")
        buttonHeight = config.getint("buttonDims", "h")
        buttonSpaceX = config.getint("buttonDims", "x")
        buttonSpaceY = config.getint("buttonDims", "y")

        print("\nStarting up AOS-GUI, please wait...")
        print("Setting up system apps", end="")

        self.settingsWindow = settings.settingsWidget()
        print(".", end="")
        self.fsWindow = fs.FsWindow()
        print(".", end="")
        self.cInstWindow = cinstall.camelInstall()
        print(".", end="")
        self.editWindow = edit.editApp()
        print(".", end="")
        self.helpWindow = aoshelp.aoshelp()
        print(".", end="")
        self.atermWindow = terminal.aterm()
        print(".", end="")
        self.aLaunchWindow = launcher.launcher()
        print(".", end="")
        self.calcWindow = calc.calculator()
        print(".")

        stylesheet = f"""
          background-color: {bgcolor};
          color: {textcolor};
          """

        wallpaper = config["wallpaper"]["path"]
        size = app.primaryScreen().size()

        if wallpaper:
            img = QPixmap(wallpaper)
            img = img.scaled(QSize(size.width(), size.height()))
            bgimgLabel = QLabel(self)
            bgimgLabel.setPixmap(img)
            bgimgLabel.setGeometry(0, 0, size.width(), size.height())

        self.setWindowTitle("AOS-GUI")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, size.width(), size.height())
        self.setStyleSheet(stylesheet)

        print("Finalizing desktop", end="")
        self.setupMenuBar()
        print(".", end="")
        self.setupButtons()
        print(".", end="")
        self.setupShortcuts()
        print(".")
        print("Finished!")

    def updateDesktopFile(self):
        global numShortcuts
        f = open(getAOSdir() + "/system/data/user/desktop.aos", "w")

        for i in range(8, numShortcuts):
            f.write(str(globals()["sc" + str(i)].text()))
            if i != numShortcuts - 1:
                f.write("|")

    def removeShortcut(self, prgm=""):
        global buttonX, buttonY, btextcolor, bbgcolor, buttonFontSize, buttonWidth, buttonHeight, buttonSpaceX, buttonSpaceY, numShortcuts, sysApps
        size = app.primaryScreen().size()
        ok = False

        if prgm == False:
            prgm, done = QInputDialog.getText(self, "Remove Shortcut", "Type the program you would like to remove the shortcut to. (Omit .py)", flags=Qt.Window | Qt.WindowStaysOnTopHint)
            ok = True

        if prgm.isspace() or prgm == "":
            pass
        else:
            for i in globals():
                try:
                    if globals().get(i).text() == prgm:
                        if prgm not in sysApps:
                            numShortcuts -= 1
                            globals().get(i).hide()

                            buttonX -= buttonWidth + buttonSpaceX

                            if buttonX + buttonWidth >= size.width() - buttonSpaceX:
                                buttonY -= buttonHeight + buttonSpaceY
                                buttonX = buttonSpaceX
                            break
                except AttributeError:
                    pass
                except TypeError:
                    pass

        if ok == True:
            self.updateDesktopFile()

    def createShortcut(self, prgm=""):
        # replace this with dropdown menu with apps using qwidget instead.
        global buttonX, buttonY, btextcolor, bbgcolor, buttonFontSize, buttonWidth, buttonHeight, buttonSpaceX, buttonSpaceY, numShortcuts
        size = app.primaryScreen().size()
        ok = False

        if prgm == False:
            prgm, done = QInputDialog.getText(self, "Create Shortcut", "Type the program you would like to make a shortcut to. (Omit .py)", flags=Qt.Window | Qt.WindowStaysOnTopHint)
            ok = True

        prgm = prgm.strip()

        if prgm.isspace() or prgm == "":
            pass
        else:
            globals()["sc" + str(numShortcuts)] = DraggableButton(self)
            globals()["sc" + str(numShortcuts)].setGeometry(buttonX, buttonY, buttonWidth, buttonHeight)
            globals()["sc" + str(numShortcuts)].setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
            globals()["sc" + str(numShortcuts)].setCursor(Qt.CursorShape.PointingHandCursor)
            globals()["sc" + str(numShortcuts)].setText(prgm)
            def execRoutine(prgm):
                ret, err = openApplication(prgm)
                if err:
                    msgBox("Error in "+prgm+": "+str(err),"AOS-GUI/execRoutine")
            globals()["sc" + str(numShortcuts)].clicked.connect(lambda: execRoutine(prgm))
            globals()["sc" + str(numShortcuts)].show()

            self.repaint()

            numShortcuts += 1

            buttonX += buttonWidth + buttonSpaceX

            if buttonX + buttonWidth >= size.width() - buttonSpaceX:
                buttonY += buttonHeight + buttonSpaceY
                buttonX = buttonSpaceX

        if ok == True:
            self.updateDesktopFile()

    def setupButtons(self):
        global buttonX, buttonY, buttonSpaceX, buttonSpaceY

        btnName = 0

        buttonX = buttonSpaceX

        for i in buttonsShown:
            if i != "False":
                globals()[btnName] = DraggableButton(self)
                globals()[btnName].setGeometry(buttonX, buttonY, buttonWidth, buttonHeight)
                globals()[btnName].setStyleSheet(f"{buttonFontSize}; background-color: {bbgcolor}; color: {btextcolor};")
                globals()[btnName].setCursor(Qt.CursorShape.PointingHandCursor)

                match btnName:
                    case 0:
                        globals()[btnName].setText("Settings")
                        globals()[btnName].clicked.connect(self.settingsWindow.showNormal)
                        globals()[btnName].clicked.connect(self.settingsWindow.activateWindow)
                    case 1:
                        globals()[btnName].setText("Launcher")
                        globals()[btnName].clicked.connect(self.aLaunchWindow.showNormal)
                        globals()[btnName].clicked.connect(self.aLaunchWindow.activateWindow)
                    case 2:
                        globals()[btnName].setText("Filesystem")
                        globals()[btnName].clicked.connect(self.fsWindow.showNormal)
                        globals()[btnName].clicked.connect(self.fsWindow.activateWindow)
                    case 3:
                        globals()[btnName].setText("camelInstall")
                        globals()[btnName].clicked.connect(self.cInstWindow.showNormal)
                        globals()[btnName].clicked.connect(self.cInstWindow.activateWindow)
                    case 4:
                        globals()[btnName].setText("Editor")
                        globals()[btnName].clicked.connect(lambda: QProcess.startDetached(sys.executable, ["files/system/edit.py"]))
                        # globals()[btnName].clicked.connect(self.editWindow.activateWindow)
                    case 5:
                        globals()[btnName].setText("AOSHelp")
                        globals()[btnName].clicked.connect(self.helpWindow.showNormal)
                        globals()[btnName].clicked.connect(self.helpWindow.activateWindow)
                        globals()[btnName].clicked.connect(self.helpWindow.reset)
                    case 6:
                        globals()[btnName].setText("Terminal")
                        globals()[btnName].clicked.connect(self.atermWindow.showNormal)
                        globals()[btnName].clicked.connect(self.atermWindow.activateWindow)
                    case 7:
                        globals()[btnName].setText("Calculator")
                        globals()[btnName].clicked.connect(self.calcWindow.showNormal)
                        globals()[btnName].clicked.connect(self.calcWindow.activateWindow)
                buttonX += buttonWidth + buttonSpaceX

            btnName += 1

        f = open(getAOSdir() + "/system/data/user/desktop.aos", "r")
        desktopFile = f.read().split("|")
        f.close()

        for i in desktopFile:
            self.createShortcut(i)

    def setupMenuBar(self):
        global timeMenu, batteryMenu, cpuUsageMenu, cpuUsagePerMenu, memoryMenu, ioMenu, menubarSegs
        menuBar = self.menuBar()
        menuBar.setStyleSheet(f"background-color: {tbgcolor}; color: {ttextcolor};")

        self.runAction = QAction("&Run...", self)
        self.setAction = QAction("&Settings", self)
        self.restartAction = QAction("&Restart", self)
        self.exitAction = QAction("&Exit", self)
        self.scAction = QAction("&Create Shortcut...", self)
        self.rscAction = QAction("&Remove Shortcut...", self)

        aosMenu = QMenu(f"&AOS - {username}", self)
        extrasMenu = QMenu(f"Extras", self)

        menuBar.addMenu("|").setEnabled(False)
        menuBar.addMenu(aosMenu)
        menuBar.addMenu("|").setEnabled(False)
        aosMenu.addAction(self.runAction)
        aosMenu.addAction(self.setAction)
        aosMenu.addAction(self.restartAction)
        aosMenu.addAction(self.exitAction)
        menuBar.addMenu(extrasMenu)
        extrasMenu.addAction(self.scAction)
        extrasMenu.addAction(self.rscAction)

        f = open("files/system/data/user/menubar.aos", "r")
        menubarSegs = f.read().split("|")

        timeMenu = QMenu(strftime("%H:%M:%S - /%m/%d/%Y"), self)
        timeMenu.setEnabled(False)
        batteryMenu = QMenu("100%", self) # TODO: setting to enable time left
        batteryMenu.setEnabled(False)
        cpuUsageMenu = QMenu("CPU: 0%", self)
        cpuUsageMenu.setEnabled(False)
        cpuUsagePerMenu = QMenu("CPU (per): 0%", self)
        cpuUsagePerMenu.setEnabled(False)

        memoryMenu = QMenu("RAM: 0 MB", self)
        memoryMenu.setEnabled(False)

        for i in menubarSegs:
            match i:
                case "Clock":
                    menuBar.addMenu("|").setEnabled(False)
                    menuBar.addMenu(timeMenu)
                case "Battery":
                    menuBar.addMenu("|").setEnabled(False)
                    menuBar.addMenu(batteryMenu)
                case "CPU Usage (Total)":
                    menuBar.addMenu("|").setEnabled(False)
                    menuBar.addMenu(cpuUsageMenu)
                case "CPU Usage (Per CPU)":
                    menuBar.addMenu("|").setEnabled(False)
                    menuBar.addMenu(cpuUsagePerMenu)
                case "Available Memory":
                    menuBar.addMenu("|").setEnabled(False)
                    menuBar.addMenu(memoryMenu)

        f.close()

        self.runAction.triggered.connect(self.run)
        self.setAction.triggered.connect(self.settingsWindow.show)
        self.restartAction.triggered.connect(restart)
        def escape():
            raise SystemExit
        self.exitAction.triggered.connect(escape)
        self.scAction.triggered.connect(self.createShortcut)
        self.rscAction.triggered.connect(self.removeShortcut)

    def run(self):
        prgm, done = QInputDialog.getText(self, "Run", "Type the program you would like to run (.py extension not needed)", flags=Qt.Window | Qt.WindowStaysOnTopHint)

        if prgm.isspace() or prgm == "":
            pass
        else:
            if prgm.lower().endswith(".py"):
                prgm = "".join(prgm.split(".py")[:1])

            match prgm.lower():
                case "fs" | "filesystem":
                    self.fsWindow.show()
                case "editor" | "edit":
                    QProcess.startDetached(sys.executable, ["files/system/edit.py"])
                case "settings":
                    self.settingsWindow.show()
                case "aoshelp" | "help":
                    self.helpWindow.show()
                case "cinstall" | "camelinstall":
                    self.cInstWindow.show()
                case "aterm" | "terminal":
                    self.atermWindow.show()
                case "applauncher":
                    self.aLaunchWindow.show()
                case "splash": # figure out why this isn't working
                    splashscreen = splash.splashScreen()
                    splashscreen.__init__()
                    splashscreen.setWindowState(Qt.WindowActive)
                    splashscreen.activateWindow()  # for Windows
                    splashscreen.show()
                case "calc" | "calculator":
                    self.calcWindow.show()
                case "about":
                    QMessageBox.about(self,"About AOS-GUI","AOS-GUI version " + version + ", created by nanobot567.\n\nMore information can be found in AOSHelp or the GitHub repository (https://github.com/AOS-GUI/AOS-GUI/).")
                case _:
                    ret, err = openApplication(prgm)
                    if err:
                        msgBox("Error in "+prgm+": "+str(err),"AOS-GUI/execRoutine")
                    

            self.setStyleSheet(f"background-color: {bgcolor}; color: {textcolor};")

    def setupShortcuts(self):
        self.runSC = QShortcut(QKeySequence(kSeqs[0]), self)
        self.termSC = QShortcut(QKeySequence(kSeqs[1]), self)
        self.setSC = QShortcut(QKeySequence(kSeqs[2]), self)
        self.helpSC = QShortcut(QKeySequence(kSeqs[3]), self)
        self.runSC.activated.connect(self.run)
        self.termSC.activated.connect(self.atermWindow.show)
        self.setSC.activated.connect(self.settingsWindow.show)
        self.helpSC.activated.connect(self.helpWindow.show)

    def showEvent(self, event):
        f = open("files/system/data/user/autorun.aos", "r")
        for i in f.read().split("|"):
            if i:
                ret, err = openApplication(i)
                if ret == -1: # this could be cleaner
                    match i:
                        case "aoshelp":
                            self.helpWindow.show()
                        case "calc":
                            self.calcWindow.show()
                        case "cinstall":
                            self.cInstWindow.show()
                        case "edit":
                            QProcess.startDetached(sys.executable, ["files/system/edit.py"])
                        case "fs":
                            self.fsWindow.show()
                        case "launcher":
                            self.aLaunchWindow.show()
                        case "settings":
                            self.settingsWindow.show()
                        case "terminal":
                            self.atermWindow.show()
                        case "updater":
                            self.updater = updater.updater()
        super().showEvent(event)

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])

    try:
        if config["qsplash"]["show"] == "True":
            pixmap = QPixmap("docs/resources/images/aosgui-white.png")
            qsplash = QSplashScreen(pixmap)
            qsplash.show()
        window = AOS()
        window.showFullScreen()

        try:
            if config["startupSound"]["play"] == "True":
                def play():
                    playsound(getAOSdir() + "/system/data/silence.wav")
                    playsound(getAOSdir() + "/system/data/AOS.wav")
                    return 0 # fix hang

                t = threading.Thread(target=play)
                t.start()
        except:
            pass

        if config["userinfo"]["pass"] != "":
            passwordInput = ""
            while passwordInput != config["userinfo"]["pass"]:
                passwordInput, z = QInputDialog.getText(window, "Password", "Please enter your password.", QLineEdit.Normal, "")

        if config["splash"]["show"] == "True" or config["splash"]["show"] == "":
            splashscreen = splash.splashScreen()
            splashscreen.setWindowState(Qt.WindowActive)
            splashscreen.activateWindow()  # for Windows
            splashscreen.show()

        f.close()

        timer = QTimer()

        for i in menubarSegs:
            match i:
                case "Clock":
                    if clockMode == "True":
                        timer.timeout.connect(lambda: timeMenu.setTitle(strftime("%H:%M:%S - %m/%d/%Y")))
                    else:
                        timer.timeout.connect(lambda: timeMenu.setTitle(strftime("%I:%M:%S - %m/%d/%Y")))
                case "Battery":
                    if psutil.sensors_battery() != None:
                        timer.timeout.connect(lambda: batteryMenu.setTitle(str(round(psutil.sensors_battery().percent,2)) + "%"))
                case "CPU Usage (Total)":
                    timer.timeout.connect(lambda: cpuUsageMenu.setTitle("CPU: " + str(psutil.cpu_percent()) + "%"))
                case "CPU Usage (Per CPU)":
                    def calc():
                        percpu = psutil.cpu_percent(percpu=True);
                        percpu = [str(e)+"%" for e in percpu];
                        percpuText = " / ".join(percpu);

                        cpuUsagePerMenu.setTitle("CPU (per): " + percpuText)

                    timer.timeout.connect(calc)
                case "Available Memory":
                    timer.timeout.connect(lambda: memoryMenu.setTitle("RAM: " + str(round(psutil.virtual_memory().available / 1000000)) + " MB"))

        timer.start(int(config["menubar"]["refreshRate"]))

        app.setStyle(config["guitheme"]["theme"])

    except (FileNotFoundError, KeyError, IndexError, SyntaxError, ValueError, configparser.NoSectionError) as e: # oh, couldn't find a file, or syntax in a file is incorrect? just fall back to installer.
        # i know the above line is disgusting, but i'm trying to reduce the amount of raw python errors
        print("WARN: ran into an issue with configuration files, falling back to installer. Error: \n"+str(e))
        app.setStyle("Windows")
        window = setupAOS.installform()
        window.show()
    else:
        try:
            if config["inAppTheme"]["use"] == "True":
                QGuiApplication.setPalette(getPalette())

        except (FileNotFoundError, NameError):
            pass

    # app.setWindowIcon(QIcon(QPixmap("/".join(getAOSdir().split("/")[:-2])+"/docs/resources/images/aosgui-black.png").scaled(100,100,1))) # when you have a good icon, go for it!
    
    # TODO: create an AOS cursor

    if config["qsplash"]["show"] == "True":
        qsplash.close()

    exit(app.exec_())