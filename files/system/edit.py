from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import re

from sys import path,argv,exit,executable
import os
path.append(os.getcwd())

from files.apps.sdk.sdk import *

filePath = ""
currentlyOpenFile = "Untitled"
currentlyOpenFileName = "Untitled"
originalText = ""

fontsize = 0.0

allowHighlighting = True
tabsAreSpaces = True

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mapping = {}

    def addMapping(self, pattern, patternFormat):
        self._mapping[pattern] = patternFormat

    def removeMapping(self, pattern):
        if pattern in self._mapping:
            self._mapping[pattern] = None

    def clearMapping(self):
        self._mapping.clear()

    def highlightBlock(self, text):
        for pattern, fmt in self._mapping.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end-start, fmt)

class PyEdit(QTextEdit):
    def __init__(self,parent=None):
        super(PyEdit,self).__init__(parent=None)
    def keyPressEvent(self,event):
        global tabsAreSpaces
        if event.key() == Qt.Key_Tab and tabsAreSpaces:
            tc = self.textCursor()
            tc.insertText("    ")
            return
        return QTextEdit.keyPressEvent(self,event)

class editApp(QMainWindow):
    def updateStatus(self):
        global fontsize

        if currentlyOpenFile != "Untitled":
            with open(currentlyOpenFile,"r",encoding="utf-8") as f:
                if self.textEdit.toPlainText() != f.read():
                    self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}*")
        self.textEdit.setFontPointSize(fontsize)
        self.textEdit.setFontFamily("Consolas")

    def updateText(self):
        if self.formatBox.currentText() == "Plaintext":
            if self.originalText != "":
                self.textEdit.setText(self.originalText)
            else:
                self.textEdit.setText(self.textEdit.toPlainText())
        elif self.formatBox.currentText() == "Markdown":
            self.originalText = self.textEdit.toPlainText()
            self.textEdit.setMarkdown(self.textEdit.toMarkdown())
        elif self.formatBox.currentText() == "HTML":
            self.originalText = self.textEdit.toPlainText()
            self.textEdit.setHtml(self.textEdit.toHtml())

    def setupUi(self, editApp):
        global fontsize, allowHighlighting

        self.setObjectName("editApp")
        self.resize(500, 400)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout_2 = QFormLayout(self.centralwidget)
        self.formLayout_2.setObjectName("formLayout_2")
        self.textEdit = PyEdit(self.centralwidget)
        self.textEdit.setEnabled(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setWordWrapMode(False)
        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.textEdit)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 500, 23))
        self.menubar.setObjectName("menubar")
        if os.name == "nt":
            self.menubar.setStyleSheet(
                """
                QMenuBar
                {
                    background-color: #fff;
                    color: #000;
                }
                QMenuBar::item
                {
                    background-color: #fff;
                    color: #000;
                }
                QMenuBar::item::selected
                {
                    background-color: #3399cc;
                    color: #fff;
                }
                QMenu
                {
                    background-color: #fff;
                    color: #000;
                }
                QMenu::item::selected
                {
                    background-color: #333399;
                    color: #999;
                }
                """
            )
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuDev = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionWordWrap = QAction(self)
        self.actionWordWrap.setObjectName("actionPreferences")
        self.actionNew = QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionNewWindow = QAction(self)
        self.actionOpen = QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QAction(self)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionExit = QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionFontSize = QAction(self)
        self.actionFontSize.setObjectName("actionFontSize")
        self.actionHighlighting = QAction(self)
        self.actionHighlighting.setObjectName("actionHighlighting")
        self.actionRun = QAction(self)
        self.actionTabsSpaces = QAction(self)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionNewWindow)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionExit)
        self.menuSettings.addAction(self.actionWordWrap)
        self.menuSettings.addAction(self.actionFontSize)
        self.menuSettings.addAction(self.actionHighlighting)
        self.menuSettings.addAction(self.actionTabsSpaces)
        self.menuDev.addAction(self.actionRun)
        self.menubar.addAction(self.menuFile.menuAction())
        #self.menubar.addAction(self.menuDev.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.actionNew.triggered.connect(self.newFile)
        self.actionNewWindow.triggered.connect(lambda: QProcess.startDetached(executable, ["files/system/edit.py"]))
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSaveAs.triggered.connect(self.saveAsFile)

        def escape():
            global currentlyOpenFile
            goodToQuit = False
            text = self.textEdit.toPlainText()

            try:
                with open(currentlyOpenFile,"r",encoding="utf-8") as fl:
                    if text != fl.read():
                        ret = msgBox("Would you like to save your current file?", "Save?", QMessageBox.Information, QMessageBox.Yes|QMessageBox.No)
                        if ret == QMessageBox.Yes:
                            if self.saveFile() == 0:
                                goodToQuit = True
                        else:
                            goodToQuit = True
                    else:
                        goodToQuit = True
            except FileNotFoundError:
                if not (text.isspace() or text == ""):
                    ret = msgBox("Would you like to save your current file?", "Save?", QMessageBox.Information, QMessageBox.Yes|QMessageBox.No)
                    if ret == QMessageBox.Yes:
                        if self.saveFile() == 0:
                            goodToQuit = True
                    else:
                        goodToQuit = True
                else:
                    goodToQuit = True

            if goodToQuit:
                raise SystemExit

        self.actionExit.triggered.connect(escape)
        self.actionWordWrap.triggered.connect(lambda: self.textEdit.setWordWrapMode(not self.textEdit.wordWrapMode()))
        self.actionWordWrap.setCheckable(True)
        self.actionHighlighting.triggered.connect(lambda: self.changeAllowHighlighting(self.actionHighlighting.isChecked()))
        self.actionHighlighting.setCheckable(True)
        self.actionHighlighting.setChecked(True)
        self.actionFontSize.triggered.connect(self.setNewFontSize)
        self.actionTabsSpaces.triggered.connect(lambda: self.setTabsSpaces(self.actionTabsSpaces.isChecked()))
        self.actionTabsSpaces.setCheckable(True)
        self.actionTabsSpaces.setChecked(True)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        fontsize = 10.0

        self.textEdit.setFontPointSize(fontsize)
        self.textEdit.setFontFamily("Consolas")
        self.textEdit.textChanged.connect(self.updateStatus)

        self.saveSC = QShortcut(QKeySequence("Ctrl+S"), self)
        self.saveSC.activated.connect(self.saveFile)
        self.saveAsSC = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        self.saveAsSC.activated.connect(self.saveAsFile)
        self.openSC = QShortcut(QKeySequence("Ctrl+O"), self)
        self.openSC.activated.connect(self.openFile)
        self.newSC = QShortcut(QKeySequence("Ctrl+N"), self)
        self.newSC.activated.connect(self.newFile)
        self.newWindowSC = QShortcut(QKeySequence("Ctrl+Shift+N"), self)
        self.newWindowSC.activated.connect(lambda: QProcess.startDetached(executable, ["files/system/edit.py"]))
        self.escSC = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.escSC.activated.connect(escape)
        self.runSC = QShortcut(QKeySequence("F5"), self)
        self.runSC.activated.connect(self.execFile)

        self.highlight = Highlighter()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
        self.menuFile.setTitle(_translate("editApp", "File"))
        self.menuSettings.setTitle(_translate("editApp", "Settings"))
        self.menuDev.setTitle("Development")
        self.actionRun.setText("Run...")
        self.actionWordWrap.setText(_translate("editApp", "Word Wrap"))
        self.actionNew.setText(_translate("editApp", "New"))
        self.actionOpen.setText(_translate("editApp", "Open..."))
        self.actionSave.setText(_translate("editApp", "Save"))
        self.actionSaveAs.setText(_translate("editApp", "Save As..."))
        self.actionFontSize.setText(_translate("editApp", "Font Size..."))
        self.actionNewWindow.setText("New Window...")
        self.actionHighlighting.setText("Syntax Highlighting")
        self.actionExit.setText("Exit")
        self.actionTabsSpaces.setText("Replace tabs with 4 spaces")

    def setTabsSpaces(self, spaces):
        global tabsAreSpaces
        tabsAreSpaces = spaces

    def execFile(self):
        global currentlyOpenFileName,currentlyOpenFile
        index = 0
        finalindex = 0
        filepath = currentlyOpenFile.split("/")
        for i in filepath:
            index += 1
            if i == "files":
                finalindex = index-1
        directory = "/".join(currentlyOpenFile.split("/")[finalindex:-1])+"/"
        # msgBox(directory)
        ret, err = openApplication(currentlyOpenFileName, directory)
        if err:
            msgBox("Error in "+currentlyOpenFileName+": "+str(err),"AOS-GUI/execRoutine")

    def newFile(self):
        ret = msgBox("Would you like to save your current file?", "Save?", QMessageBox.Information, QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.saveAsFile()

        self.textEdit.setText("")
        # self.formatBox.setCurrentText("Plaintext")

    def openFile(self, f=""):
        global currentlyOpenFile,currentlyOpenFileName
        passall = False
        if not f:
            file,check = QFileDialog.getOpenFileName(None, "Open a file", getAOSdir()+"/", "All Files (*)", options=QFileDialog.Options() | QFileDialog.DontUseNativeDialog)
        else:
            check = True
            file = f
        if check:
            try:
                with open(currentlyOpenFile,"r",encoding="utf-8") as fl:
                    if self.textEdit.toPlainText() != fl.read():
                        ret = msgBox("Would you like to save your current file?", "Save?", QMessageBox.Information, QMessageBox.Yes|QMessageBox.No)
                        if ret == QMessageBox.Yes:
                            self.saveFile()
                        else:
                            passall = True
            except FileNotFoundError:
                if f:
                    try:
                        open(f,"r",encoding="utf-8")
                    except FileNotFoundError:
                        self.saveFile(f)
            if passall == False:
                text = open(file,"r",encoding="utf-8")
                self.textEdit.setPlainText(text.read())
                text.close()

                currentlyOpenFile = file
                currentlyOpenFileName = currentlyOpenFile.split("/")
                currentlyOpenFileName = currentlyOpenFileName[-1]
                self.setupHighlighting()
                self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")

                if currentlyOpenFileName.endswith(".py"):
                    self.menubar.removeAction(self.menuSettings.menuAction())
                    self.menubar.addAction(self.menuDev.menuAction())
                    self.menubar.addAction(self.menuSettings.menuAction())
                    self.actionRun.triggered.connect(self.execFile)
                else:
                    self.menubar.removeAction(self.menuDev.menuAction())
    
    def saveFile(self, path=""):
        global currentlyOpenFile,currentlyOpenFileName

        if path:
            text = open(path, "w",encoding="utf-8")
            text.write(self.textEdit.toPlainText())
            text.close()
            currentlyOpenFile = path
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
            self.setupHighlighting()
            self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
        else:
            if currentlyOpenFileName == "Untitled":
                return self.saveAsFile()
            else:
                text = open(currentlyOpenFile,"w",encoding="utf-8")
                text.write(self.textEdit.toPlainText())
                text.close()
                self.setupHighlighting()
                self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
        return 0
    
    def saveAsFile(self):
        global currentlyOpenFile,currentlyOpenFileName

        file,check = QFileDialog.getSaveFileName(None, "Save", directory=getAOSdir(), options=QFileDialog.Options() | QFileDialog.DontUseNativeDialog)
        if check:
            text = open(file,"w",encoding="utf-8")
            text.write(self.textEdit.toPlainText())
            text.close()
            currentlyOpenFile = file
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
        self.setupHighlighting()
        self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")

        if currentlyOpenFileName.endswith(".py"):
            self.menubar.removeAction(self.menuSettings.menuAction())
            self.menubar.addAction(self.menuDev.menuAction())
            self.menubar.addAction(self.menuSettings.menuAction())
            self.actionRun.triggered.connect(self.execFile)
        else:
            self.menubar.removeAction(self.menuDev.menuAction())

        if not check:
            return -1
        else:
            return 0

    def changeAllowHighlighting(self, allow):
        global allowHighlighting

        allowHighlighting = allow
        self.setupHighlighting()

    def setNewFontSize(self):
        global fontsize
        fontsize, done = QInputDialog.getDouble(self, "Font Size", "Enter the new font size: ",fontsize)
        self.textEdit.setFontPointSize(fontsize) # fix so all text is made that size

    def setupHighlighting(self):
        global allowHighlighting
        blueFormat = QTextCharFormat()
        blueFormat.setForeground(QColor("blue"))
        orangeFormat = QTextCharFormat()
        orangeFormat.setForeground(QColor("orange"))
        redFormat = QTextCharFormat()
        redFormat.setForeground(QColor("red"))
        
        pyKeywords = [
        "and", "as", "assert", "break", "class", "continue", "def",
        "del", "elif", "else", "except", "exec", "finally",
        "for", "from", "global", "if", "import", "in",
        "is", "lambda", "not", "or", "pass", "print",
        "raise", "return", "try", "while", "with", "yield",
        "None", "True", "False", "match", "case"
        ]

        aoshKeywords = [
            "help","clear","echo","rm","dir","read","script",
            "ver","term","beep","mkdir","exec","restart","mkfile",
            "set","py","camel","dl","alias","cd","note","color",
            "edit"
        ]

        aoshEnvVars = [
            "%DIR","%DIRSTACK","%ECHO","%COLOR","%MAXLINES","%VARS"
        ]

        operators = [
        '=',
        '==', '!=', '<', '<=', '>', '>=',
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        '\+=', '-=', '\*=', '/=', '\%=',
        '\^', '\|', '\&', '\~', '>>', '<<',
        ]

        braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
        ]


        if currentlyOpenFileName.lower().endswith(".py"):
            keywordFormat = QTextCharFormat()
            theme, err = getTheme()
            keywordFormat.setForeground(QColor(theme[4]))
            keywordFormat.setFontWeight(QFont.Bold)

            defclassFormat = QTextCharFormat()
            defclassFormat.setForeground(Qt.red)
            defclassFormat.setFontWeight(QFont.Bold)

            for i in pyKeywords:
                pattern = fr"((?<=\s)|\A)({i}*?)(?=(\s|\:))"
                self.highlight.addMapping(pattern, keywordFormat)
            
            self.highlight.addMapping(r'\bdef\b\s*(\w+)', defclassFormat)
            self.highlight.addMapping(r'\bclass\b\s*(\w+)', defclassFormat)
            self.highlight.addMapping(r'\bself\b', keywordFormat)

            operatorFormat = QTextCharFormat()
            operatorFormat.setForeground(Qt.yellow)

            for i in operators:
                self.highlight.addMapping(fr'{i}', operatorFormat)

            braceFormat = QTextCharFormat()
            braceFormat.setForeground(Qt.yellow)

            for i in braces:
                self.highlight.addMapping(fr'{i}', braceFormat)

            stringFormat = QTextCharFormat()
            stringFormat.setForeground(QColor("orange"))
            # stringFormat.setFontItalic(True)
            self.highlight.addMapping(r'"[^"\\]*(\\.[^"\\]*)*"', stringFormat)
            self.highlight.addMapping(r"'[^'\\]*(\\.[^'\\]*)*'", stringFormat)

            numberFormat = QTextCharFormat()
            numberFormat.setForeground(QColor("cyan"))
            self.highlight.addMapping(r'\b[+-]?[0-9]+[lL]?\b', numberFormat)
            self.highlight.addMapping(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', numberFormat)
            self.highlight.addMapping(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', numberFormat)

            commentFormat = QTextCharFormat()
            commentFormat.setForeground(Qt.green)
            pattern = r"^\s*#.*$"
            self.highlight.addMapping(pattern, commentFormat)

            pattern = r"#.*$"
        elif currentlyOpenFileName.lower().endswith("md"):
            for i in range(1,7):
                self.highlight.addMapping(r"(#{"+str(i)+"}\s)(.*)", blueFormat) # header

            self.highlight.addMapping("(\*|\_)+(\S+)(\*|\_)+", redFormat) # italic/bold text
            self.highlight.addMapping("(\[.*\])(\((http)(?:s)?(\:\/\/).*\))", blueFormat) # link, fix please
            # self.highlight.addMapping("(\!)(\[(?:.*)?\])(\(.*(\.(jpg|png|gif|tiff|bmp))(?:(\s\"|\')(\w|\W|\d)+(\"|\'))?\)", blueFormat) #img
            self.highlight.addMapping("(^(\s+)?(\W{1})(\s)(?:$)?)+", blueFormat) # ul
            self.highlight.addMapping("(^(\s+)?(\d+\.)(\s)(?:$)?)+", blueFormat) # ol
            self.highlight.addMapping("((^(\>{1})(\s)(.*)(?:$)?))+", orangeFormat) # block quote
            self.highlight.addMapping("\`([^\`].*?)\`", orangeFormat) # inline code
            self.highlight.addMapping("(\\`{3}\\n+)(.*)(\\n+\\`{3})", orangeFormat) # code block
            self.highlight.addMapping("(\={3}|\-{3}|\*{3})", redFormat) # horizontal line
            self.highlight.addMapping("(\<{1})(\S+@\S+)(\>{1})", blueFormat) #email
            self.highlight.addMapping("|(?:([^\r\n|]*)\|)+\r?\n\|(?:(:?-+:?)\|)+\r?\n(\|(?:([^\r\n|]*)\|)+\r?\n)+", blueFormat) #table
        elif currentlyOpenFileName.lower().endswith("script") or currentlyOpenFileName.lower().endswith("aosh") or currentlyOpenFile == getAOSdir()+"system/data/user/terminal.aos":
            blueFormat = QTextCharFormat()
            theme, err = getTheme()
            blueFormat.setForeground(QColor(theme[4]))
            orangeFormat = QTextCharFormat()
            orangeFormat.setForeground(QColor("orange"))

            for i in aoshKeywords:
                pattern = fr"((?<=\s)|\A|(?<=;))({i}*?)(?=(\s|\:|;))"
                self.highlight.addMapping(pattern, blueFormat)
            for i in aoshEnvVars:
                pattern = fr"((?<=\s)|\A|(?<=;))({i}*?)(?=(\s|\:|;))"
                self.highlight.addMapping(pattern, orangeFormat)
            self.highlight.addMapping("(?<=);",redFormat)
        else:
            self.highlight.clearMapping()

        if not allowHighlighting:
            self.highlight.clearMapping()

        self.highlight.setDocument(self.textEdit.document())


if __name__ == "__main__":
    app = QApplication([])
    edit = editApp()
    edit.setupUi(editApp)

    if getSettings()["inAppTheme"]["use"] == "True":
        app.setPalette(getPalette())

    edit.show()

    try:
        edit.openFile(argv[1])
    except:
        pass
    exit(app.exec_())
