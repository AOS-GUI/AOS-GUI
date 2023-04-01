from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import re

from sys import path,argv,exit
from os import getcwd
path.append(getcwd())

from files.apps.sdk.sdk import *

filePath = ""
currentlyOpenFile = "Untitled"
currentlyOpenFileName = "Untitled"
originalText = ""

fontsize = 0.0

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

class editApp(QMainWindow):
    def updateStatus(self):
        global fontsize
        self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}*")
        self.textEdit.setFontPointSize(fontsize)
        self.textEdit.setFontFamily("Courier New")

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
        global fontsize
        self.setObjectName("editApp")
        self.resize(500, 400)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout_2 = QFormLayout(self.centralwidget)
        self.formLayout_2.setObjectName("formLayout_2")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setEnabled(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setWordWrapMode(False)
        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.textEdit)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 500, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionWordWrap = QAction(self)
        self.actionWordWrap.setObjectName("actionPreferences")
        self.actionNew = QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QAction(self)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionFontSize = QAction(self)
        self.actionFontSize.setObjectName("actionFontSize")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuSettings.addAction(self.actionWordWrap)
        self.menuSettings.addAction(self.actionFontSize)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_As.triggered.connect(self.saveAsFile)
        self.actionWordWrap.triggered.connect(lambda: self.textEdit.setWordWrapMode(not self.textEdit.wordWrapMode()))
        self.actionWordWrap.setCheckable(True)
        self.actionFontSize.triggered.connect(self.setNewFontSize)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        fontsize = float(getSettings()["fontsize"]["size"])

        self.textEdit.setFontPointSize(fontsize)
        self.textEdit.setFontFamily("Courier New")
        self.textEdit.textChanged.connect(self.updateStatus)

        self.saveSC = QShortcut(QKeySequence("Ctrl+S"), self)
        self.saveSC.activated.connect(self.saveFile)
        self.saveAsSC = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        self.saveAsSC.activated.connect(self.saveAsFile)
        self.openSC = QShortcut(QKeySequence("Ctrl+O"), self)
        self.openSC.activated.connect(self.openFile)
        self.newSC = QShortcut(QKeySequence("Ctrl+N"), self)
        self.newSC.activated.connect(self.newFile)

        self.highlight = Highlighter()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
        self.menuFile.setTitle(_translate("editApp", "File"))
        self.menuSettings.setTitle(_translate("editApp", "Settings"))
        self.actionWordWrap.setText(_translate("editApp", "Word Wrap"))
        self.actionNew.setText(_translate("editApp", "New"))
        self.actionOpen.setText(_translate("editApp", "Open..."))
        self.actionSave.setText(_translate("editApp", "Save"))
        self.actionSave_As.setText(_translate("editApp", "Save As..."))
        self.actionFontSize.setText(_translate("editApp", "Font Size..."))

    def newFile(self):
        ret = msgBox("Would you like to save your current file?", "Save?", QMessageBox.Information, QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.saveAsFile()

        self.textEdit.setText("")
        self.formatBox.setCurrentText("Plaintext")

        # global currentlyOpenFile,currentlyOpenFileName
        # file,check = QFileDialog.getSaveFileName(None, "New File", directory=getcwd().replace("\\","/")+"/files/")
        # if check:
        #     text = open(file,"w")
        #     text.close()
        #     currentlyOpenFile = file
        #     currentlyOpenFileName = currentlyOpenFile.split("/")
        #     currentlyOpenFileName = currentlyOpenFileName[-1]
        #     self.setWindowTitle(f"AOS-GUI/editor - {currentlyOpenFileName}")

    def openFile(self):
        file,check = QFileDialog.getOpenFileName(None, "Open a file", getcwd().replace("\\","/")+"/files/", "All Files (*)")
        if check:
            text = open(file,"r")
            self.textEdit.setPlainText(text.read())
            text.close()

            global currentlyOpenFile,currentlyOpenFileName
            currentlyOpenFile = file
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
            self.setupHighlighting()
            self.updateStatus()
            self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
    
    def saveFile(self):
        global currentlyOpenFile,currentlyOpenFileName

        if currentlyOpenFileName == "Untitled":
            self.saveAsFile()
        else:
            text = open(currentlyOpenFile,"w")
            text.write(self.textEdit.toPlainText())
            text.close()
            self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")
    
    def saveAsFile(self):
        global currentlyOpenFile,currentlyOpenFileName

        file,check = QFileDialog.getSaveFileName(None, "Save", directory=getAOSdir())
        if check:
            text = open(file,"w")
            text.write(self.textEdit.toPlainText())
            text.close()
            currentlyOpenFile = file
            currentlyOpenFileName = currentlyOpenFile.split("/")
            currentlyOpenFileName = currentlyOpenFileName[-1]
        self.setWindowTitle(f"AOS-GUI/edit - {currentlyOpenFileName}")

    def setNewFontSize(self):
        global fontsize
        fontsize, done = QInputDialog.getDouble(self, "Font Size", "Enter the new font size: ",fontsize)

    def setupHighlighting(self):
        pyKeywords = [
        "and", "assert", "break", "class", "continue", "def",
        "del", "elif", "else", "except", "exec", "finally",
        "for", "from", "global", "if", "import", "in",
        "is", "lambda", "not", "or", "pass", "print",
        "raise", "return", "try", "while", "yield",
        "None", "True", "False", "match", "case"
        ]

        aoshKeywords = [
            "help","clear","echo","rm","dir","read","script",
            "ver","term","beep","mkdir","exec","restart","mkfile",
            "set","py","camel","dl"
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
            keywordFormat.setForeground(Qt.blue)
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

            # operatorFormat = QTextCharFormat()
            # operatorFormat.setForeground(Qt.green)

            # for i in operators:
            #     self.highlight.addMapping(fr'{i}', operatorFormat)

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
            numberFormat.setForeground(QColor("blue"))
            self.highlight.addMapping(r'\b[+-]?[0-9]+[lL]?\b', numberFormat)
            self.highlight.addMapping(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', numberFormat)
            self.highlight.addMapping(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', numberFormat)

            commentFormat = QTextCharFormat()
            commentFormat.setForeground(Qt.green)
            pattern = r"^\s*#.*$"
            self.highlight.addMapping(pattern, commentFormat)

            pattern = r"#.*$"
        elif currentlyOpenFileName.lower().endswith("md"):
            blueFormat = QTextCharFormat()
            blueFormat.setForeground(QColor("blue"))
            orangeFormat = QTextCharFormat()
            orangeFormat.setForeground(QColor("orange"))
            redFormat = QTextCharFormat()
            redFormat.setForeground(QColor("red"))

            for i in range(1,7):
                self.highlight.addMapping(r"(#{"+str(i)+"}\s)(.*)", blueFormat) # header

            self.highlight.addMapping("(\*|\_)+(\S+)(\*|\_)+", redFormat) # italic/bold text
            self.highlight.addMapping("(\[.*\])(\((http)(?:s)?(\:\/\/).*\))", blueFormat) # link, fix please
            # self.highlight.addMapping("(\!)(\[(?:.*)?\])(\(.*(\.(jpg|png|gif|tiff|bmp))(?:(\s\"|\')(\w|\W|\d)+(\"|\'))?\)", blueFormat) #img
            self.highlight.addMapping("(^(\s+)?(\W{1})(\s)(?:$)?)+", blueFormat) # ul
            self.highlight.addMapping("(^(\s+)?(\d+\.)(\s)(?:$)?)+", blueFormat) # ol
            self.highlight.addMapping("((^(\>{1})(\s)(.*)(?:$)?))+", orangeFormat) # block quote
            self.highlight.addMapping("(\\`{1})(.*)(\\`{1})", orangeFormat) # inline code
            self.highlight.addMapping("(\\`{3}\\n+)(.*)(\\n+\\`{3})", orangeFormat) # code block
            self.highlight.addMapping("(\={3}|\-{3}|\*{3})", redFormat) # horizontal line
            self.highlight.addMapping("(\<{1})(\S+@\S+)(\>{1})", blueFormat) #email
            self.highlight.addMapping("(((\|)([a-zA-Z\d+\s#!@'\"():;\\\/.\[\]\^<={$}>?(?!-))]+))+(\|))(?:\n)?((\|)(-+))+(\|)(\n)((\|)(\W+|\w+|\S+))+(\|$)", blueFormat) #table
        elif currentlyOpenFileName.lower().endswith("script") or currentlyOpenFileName.lower().endswith("aosh"):
            blueFormat = QTextCharFormat()
            blueFormat.setForeground(QColor("blue"))

            for i in aoshKeywords:
                pattern = fr"((?<=\s)|\A)({i}*?)(?=(\s|\:))"
                self.highlight.addMapping(pattern, blueFormat)
        else:
            self.highlight.clearMapping()

        self.highlight.setDocument(self.textEdit.document())


if __name__ == "__main__":
    app = QApplication(argv)
    edit = editApp()
    edit.setupUi(editApp)

    if getSettings()["inAppTheme"]["use"] == "True":
        app.setPalette(getPalette())

    edit.show()
    exit(app.exec_())