# required imports

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# from sdk.sdk import * # import AOS SDK (for QMainWindow)
from files.apps.sdk.sdk import * # (for QWidget) 

# next line is the project description, format is '#(tilde){name}|{desc}|{ver}'
#~template|template project|v0.1

# class name can be anything

class template(QWidget): # can be QMainWindow as well
    # this can be your normal PyQt5 code, go crazy!
    def __init__(self):
        super(template, self).__init__()
        self.setFixedSize(500, 500) # doesn't have to be fixed size!
        self.setWindowTitle("template!")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint) # this line is needed for the program to stay on top of desktop

# if your app is a QMainWindow, you can use the two lines below to set the palette if the user has enabled app theming.

#if getSettings()["inAppTheme"]["use"] == "True":
    #window.setPalette(getPalette())

# these last lines must be included for the app to launch.

# for QWidget
window = template()
window.show()

# for QMainWindow

# if __name__ == "__main__":
#     app = QApplication([])
#     window = template()

#     if getSettings()["inAppTheme"]["use"] == "True":
#         app.setPalette(getPalette())

#     window.show()
#     exit(app.exec_())