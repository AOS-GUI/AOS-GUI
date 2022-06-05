from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os.path import exists

titleText = u"welcome to AOS-GUI!"
endButtonText = u"Setup AOS-GUI"

class installform(QMainWindow):
    def __init__(self):
        super(installform, self).__init__()

        self.resize(571, 447)
        global titleText,endButtonText

        self.welcome = QLabel(self)
        self.welcome.setObjectName(u"welcome")
        self.welcome.setGeometry(QRect(140, 20, 281, 31))
        self.welcome.setStyleSheet(u"")
        self.welcome.setTextFormat(Qt.MarkdownText)
        self.welcome.setScaledContents(False)
        self.welcome.setAlignment(Qt.AlignCenter)
        self.welcomeThx = QLabel(self)
        self.welcomeThx.setObjectName(u"welcomeThx")
        self.welcomeThx.setGeometry(QRect(50, 50, 481, 51))
        self.welcomeThx.setAlignment(Qt.AlignCenter)
        self.welcomeThx.setWordWrap(True)

        self.generaInfo = QGroupBox(self)
        self.generaInfo.setObjectName(u"generaInfo")
        self.generaInfo.setGeometry(QRect(20, 120, 261, 101))
        self.unameLabel = QLabel(self.generaInfo)
        self.unameLabel.setObjectName(u"unameLabel")
        self.unameLabel.setGeometry(QRect(20, 30, 60, 16))
        self.username = QLineEdit(self.generaInfo)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(85, 30, 156, 20))
        self.passLabel = QLabel(self.generaInfo)
        self.passLabel.setObjectName(u"passLabel")
        self.passLabel.setGeometry(QRect(20, 60, 60, 16))
        self.password = QLineEdit(self.generaInfo)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(85, 60, 156, 20))
        self.password.setEchoMode(QLineEdit.Password)
        # self.otherconfig = QGroupBox(self)
        # self.otherconfig.setObjectName(u"otherconfig")
        # self.otherconfig.setGeometry(QRect(290, 230, 261, 131))
        self.install = QPushButton(self)
        self.install.setObjectName(u"install")
        self.install.setGeometry(QRect(230, 380, 111, 41))
        self.install.setAutoFillBackground(False)
        self.install.setAutoDefault(False)
        self.install.setFlat(False)
        self.install.clicked.connect(self.getmeout)
        self.customization = QGroupBox(self)
        self.customization.setObjectName(u"customization")
        self.customization.setGeometry(QRect(290, 120, 261, 241))
        self.labeltext = QLabel(self.customization)
        self.labeltext.setObjectName(u"labeltext")
        self.labeltext.setGeometry(QRect(20, 30, 101, 21))
        self.textColor = QLineEdit(self.customization)
        self.textColor.setObjectName(u"textColor")
        self.textColor.setGeometry(QRect(150, 30, 71, 22))
        self.labelbg = QLabel(self.customization)
        self.labelbg.setObjectName(u"labelbg")
        self.labelbg.setGeometry(QRect(20, 60, 101, 21))
        self.bgColor = QLineEdit(self.customization)
        self.bgColor.setObjectName(u"bgColor")
        self.bgColor.setGeometry(QRect(150, 60, 71, 21))
        self.labeltbg = QLabel(self.customization)
        self.labeltbg.setObjectName(u"labeltbg")
        self.labeltbg.setGeometry(QRect(20, 90, 101, 21))
        self.tColor = QLineEdit(self.customization)
        self.tColor.setObjectName(u"tColor")
        self.tColor.setGeometry(QRect(150, 90, 71, 21))
        self.tTextColor = QLineEdit(self.customization)
        self.tTextColor.setObjectName(u"tTextColor")
        self.tTextColor.setGeometry(QRect(150, 120, 71, 21))
        self.labelttc = QLabel(self.customization)
        self.labelttc.setObjectName(u"labelttc")
        self.labelttc.setGeometry(QRect(20, 120, 120, 21))
        self.labelbc = QLabel(self.customization)
        self.labelbc.setObjectName(u"labelbc")
        self.labelbc.setGeometry(QRect(20, 150, 101, 21))
        self.bColor = QLineEdit(self.customization)
        self.bColor.setObjectName(u"bColor")
        self.bColor.setGeometry(QRect(150, 150, 71, 21))
        self.labelbbg = QLabel(self.customization)
        self.labelbbg.setObjectName(u"labelbbg")
        self.labelbbg.setGeometry(QRect(20, 180, 131, 21))
        self.bTextColor = QLineEdit(self.customization)
        self.bTextColor.setObjectName(u"bTextColor")
        self.bTextColor.setGeometry(QRect(150, 180, 71, 21))
        self.labeltc = QLabel(self.customization)
        self.labeltc.setObjectName(u"labeltc")
        self.labeltc.setGeometry(QRect(20, 120, 101, 21))
        self.showondesktop = QGroupBox(self)
        self.showondesktop.setObjectName(u"showondesktop")
        self.showondesktop.setGeometry(QRect(20, 230, 261, 131))
        self.aos_settings = QCheckBox(self.showondesktop)
        self.aos_settings.setObjectName(u"aos_settings")
        self.aos_settings.setGeometry(QRect(20, 60, 100, 17))
        self.rndr = QCheckBox(self.showondesktop)
        self.rndr.setObjectName(u"rndr")
        self.rndr.setGeometry(QRect(20, 40, 100, 17))
        self.fs = QCheckBox(self.showondesktop)
        self.fs.setObjectName(u"fs")
        self.fs.setGeometry(QRect(20, 20, 100, 17))
        self.camelInstall = QCheckBox(self.showondesktop)
        self.camelInstall.setObjectName(u"camelInstall")
        self.camelInstall.setGeometry(QRect(20, 80, 100, 17))
        self.editor = QCheckBox(self.showondesktop)
        self.editor.setObjectName(u"editor")
        self.editor.setGeometry(QRect(20, 100, 100, 17))
        # self.aos_settings.setGeometry(QRect(20, 60, 81, 17))

        # self.retranslateUi(self)

        self.install.setDefault(False)


        QMetaObject.connectSlotsByName(self)
    # setupUi

        self.setWindowTitle(QCoreApplication.translate("installform", titleText, None))
        self.welcome.setText(QCoreApplication.translate("installform", u"# welcome to AOS-GUI", None))
        self.welcomeThx.setText(QCoreApplication.translate("installform", u"thank you for downloading AOS! please fill out the information below and we'll set up AOS for you. (don't worry; you can change all of these settings later if you want!)", None))
        self.generaInfo.setTitle(QCoreApplication.translate("installform", u"General Information", None))
        self.unameLabel.setText(QCoreApplication.translate("installform", u"Username:", None))
        self.passLabel.setText(QCoreApplication.translate("installform", u"Password:", None))
        # self.otherconfig.setTitle(QCoreApplication.translate("installform", u"Additional Configuration Options", None))

        self.install.setText(QCoreApplication.translate("installform", endButtonText, None))
        self.customization.setTitle(QCoreApplication.translate("installform", u"Customization", None))
        self.labeltext.setText(QCoreApplication.translate("installform", u"Text Color:", None))
        self.labelbg.setText(QCoreApplication.translate("installform", u"Background Color:", None))

        self.labeltbg.setText(QCoreApplication.translate("installform", u"Taskbar Color:", None))

        self.labelttc.setText(QCoreApplication.translate("installform", u"Taskbar Text Color:", None))
        self.labelbc.setText(QCoreApplication.translate("installform", u"Button Color:", None))

        self.labelbbg.setText(QCoreApplication.translate("installform", u"Button Text Color:", None))

        self.camelInstall.setText((QCoreApplication.translate("installform", u"camelInstall", None)))
        self.showondesktop.setTitle(QCoreApplication.translate("installform", u"Desktop Apps", None))
        self.fs.setText(QCoreApplication.translate("installform", u"FileSystem", None))
        self.rndr.setText(QCoreApplication.translate("installform", u".rndr loader", None))
        self.aos_settings.setText(QCoreApplication.translate("installform", u"AOS Settings", None))
        self.editor.setText(QCoreApplication.translate("installform", u"Editor", None))

        # self.getCurrentSettings()
    # retranslateUi
    def getCurrentSettings(self):
        f = open("files/support/data/user/data.aos","r")
        content = f.read()
        content = content.split("\n")
        self.username.setText(content[0])
        self.password.setText(content[1])
        self.textColor.setText(content[2])
        self.bgColor.setText(content[3])
        self.tTextColor.setText(content[4])
        self.tColor.setText(content[5])
        self.bTextColor.setText(content[6])
        self.bColor.setText(content[7])
        if content[8] == "True":
            self.fs.setChecked(True)
        else:
            self.fs.setChecked(False)
        
        if content[9] == "True":
            self.rndr.setChecked(True)
        else:
            self.rndr.setChecked(False)

        if content[10] == "True":
            self.aos_settings.setChecked(True)
        else:
            self.aos_settings.setChecked(False)

        if content[11] == "True":
            self.camelInstall.setChecked(True)
        else:
            self.camelInstall.setChecked(False)

        if content[12] == "True":
            self.editor.setChecked(True)
        else:
            self.editor.setChecked(False)

        f.close()

    def getmeout(self):
        f = open("files/support/data/user/data.aos","w")
        f.write(self.username.text()+"\n")
        f.write(self.password.text()+"\n")
        f.write(self.textColor.text()+"\n")
        f.write(self.bgColor.text()+"\n")
        f.write(self.tTextColor.text()+"\n")
        f.write(self.tColor.text()+"\n")
        f.write(self.bTextColor.text()+"\n")
        f.write(self.bColor.text()+"\n")
        f.write(str(self.fs.isChecked())+"\n")
        f.write(str(self.rndr.isChecked())+"\n")
        f.write(str(self.aos_settings.isChecked())+"\n")
        f.write(str(self.camelInstall.isChecked())+"\n")
        f.write(str(self.editor.isChecked()))

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Your settings have been applied! Please reopen AOS-GUI.")
        msg.setWindowTitle("Settings set!")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        self.close()
