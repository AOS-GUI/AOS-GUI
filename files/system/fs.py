from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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

        #self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.treeView.customContextMenuRequested.connect(self.menuContextTree)

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

    #def createFolder(self):
    #    index = self.treeView.currentIndex()
    #    if not self.model().isDir(index):
    #        index = index.parent()
    #    pathDir = self.model().filePath(index)
    #    mkdir(pathDir+"/New Folder")

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
        #action_2 = QAction()
        action_2 = menu.addAction("New Folder")
        action_3 = menu.addAction("3")
        action_2.triggered.connect(self.createFolder)

        menu.exec_(self.treeView.mapToGlobal(point))
