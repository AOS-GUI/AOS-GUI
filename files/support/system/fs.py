from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from files.support.system import editor

class FsWindow(QWidget):
     def __init__(self):
          super(FsWindow, self).__init__()
          self.setWindowTitle("AOS-GUI/fs")
          self.resize(600, 400)

          self.treeView = QTreeView()
          self.treeView.resize(600,500)
          self.fileSystemModel = QFileSystemModel(self.treeView)
          self.fileSystemModel.setReadOnly(False)
          root = self.fileSystemModel.setRootPath("files")
          self.treeView.setModel(self.fileSystemModel)
          self.treeView.setRootIndex(root)
          self.fileSystemModel
          
          # self.treeView.doubleClicked.connect(self.openInEditor)

          Layout = QVBoxLayout(self)
          Layout.addWidget(self.treeView)
          self.setLayout(Layout)

     # def openInEditor(self, signal):
     #      file_path=self.treeView.model().filePath(signal)
     #      editor.openFileAtPath(file_path)