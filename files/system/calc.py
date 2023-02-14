import string

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

num = 0
waitingForNum = False

class calculator(QWidget):
    def __init__(self):
        super(calculator, self).__init__()
        self.setWindowTitle("AOS-GUI/calc")
        self.setFixedSize(270, 340)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.ui()

    def ui(self):
        self.ans = QLineEdit(self)
        self.ans.setObjectName(u"ans")
        self.ans.setGeometry(QRect(9, 10, 251, 40))
        self.ans.setReadOnly(True)
        self.ans.setAlignment(Qt.AlignRight)
        self.ans.setFont(QFont('Arial', 15))
        self.push1 = QPushButton(self)
        self.push1.setObjectName(u"push1")
        self.push1.setGeometry(QRect(10, 100, 51, 51))
        self.push1.setText(u"1")
        self.push2 = QPushButton(self)
        self.push2.setObjectName(u"push2")
        self.push2.setGeometry(QRect(70, 100, 51, 51))
        self.push2.setText(u"2")
        self.push3 = QPushButton(self)
        self.push3.setObjectName(u"push3")
        self.push3.setGeometry(QRect(130, 100, 51, 51))
        self.push3.setText(u"3")
        self.push_plus = QPushButton(self)
        self.push_plus.setObjectName(u"add")
        self.push_plus.setGeometry(QRect(210, 60, 51, 51))
        self.push_plus.setText(u"+")
        self.push4 = QPushButton(self)
        self.push4.setObjectName(u"push4")
        self.push4.setGeometry(QRect(10, 160, 51, 51))
        self.push4.setText(u"4")
        self.push5 = QPushButton(self)
        self.push5.setObjectName(u"push5")
        self.push5.setGeometry(QRect(70, 160, 51, 51))
        self.push5.setText(u"5")
        self.push6 = QPushButton(self)
        self.push6.setObjectName(u"push6")
        self.push6.setGeometry(QRect(130, 160, 51, 51))
        self.push6.setText(u"6")
        self.push_minus = QPushButton(self)
        self.push_minus.setObjectName(u"push_minus")
        self.push_minus.setGeometry(QRect(210, 120, 51, 51))
        self.push_minus.setText(u"-")
        self.push_mul = QPushButton(self)
        self.push_mul.setObjectName(u"mult")
        self.push_mul.setGeometry(QRect(210, 180, 51, 51))
        self.push_mul.setText(u"*")
        self.push_div = QPushButton(self)
        self.push_div.setObjectName(u"div")
        self.push_div.setGeometry(QRect(210, 240, 51, 51))
        self.push_div.setText(u"/")
        self.push_equal = QPushButton(self)
        self.push_equal.setObjectName(u"equ")
        self.push_equal.setGeometry(QRect(210, 300, 51, 31))
        self.push_equal.setText(u"=")
        self.push_equal.setStyleSheet("background-color:darkred;")
        self.push7 = QPushButton(self)
        self.push7.setObjectName(u"push7")
        self.push7.setGeometry(QRect(10, 220, 51, 51))
        self.push7.setText(u"7")
        self.push8 = QPushButton(self)
        self.push8.setObjectName(u"push8")
        self.push8.setGeometry(QRect(70, 220, 51, 51))
        self.push8.setText(u"8")
        self.push9 = QPushButton(self)
        self.push9.setObjectName(u"push9")
        self.push9.setGeometry(QRect(130, 220, 51, 51))
        self.push9.setText(u"9")
        self.push0 = QPushButton(self)
        self.push0.setObjectName(u"push0")
        self.push0.setGeometry(QRect(70, 280, 51, 51))
        self.push0.setText(u"0")
        self.push_del = QPushButton(self)
        self.push_del.setObjectName(u"push_del")
        self.push_del.setGeometry(QRect(100, 60, 81, 23))
        self.push_del.setText(u"Del")
        self.push_clear = QPushButton(self)
        self.push_clear.setObjectName(u"push_clear")
        self.push_clear.setGeometry(QRect(10, 60, 75, 23))
        self.push_clear.setText(u"Clear")
        self.push_point = QPushButton(self)
        self.push_point.setObjectName(u"push_point")
        self.push_point.setGeometry(QRect(10, 280, 51, 51))
        self.push_point.setText(u".")
        self.push_minus.clicked.connect(self.action_minus)
        self.push_equal.clicked.connect(self.action_equal)
        self.push0.clicked.connect(self.action0)
        self.push1.clicked.connect(self.action1)
        self.push2.clicked.connect(self.action2)
        self.push3.clicked.connect(self.action3)
        self.push4.clicked.connect(self.action4)
        self.push5.clicked.connect(self.action5)
        self.push6.clicked.connect(self.action6)
        self.push7.clicked.connect(self.action7)
        self.push8.clicked.connect(self.action8)
        self.push9.clicked.connect(self.action9)
        self.push_div.clicked.connect(self.action_div)
        self.push_mul.clicked.connect(self.action_mul)
        self.push_plus.clicked.connect(self.action_plus)
        self.push_point.clicked.connect(self.action_point)
        self.push_clear.clicked.connect(self.action_clear)
        self.push_del.clicked.connect(self.action_del)


    def action_equal(self):
        equation = self.ans.text()

        try:
            ans = eval(equation)
            self.ans.setText(str(ans))

        except:
            self.ans.setText("NaN")

    def action_plus(self):
        text = self.ans.text()
        self.ans.setText(text + " + ")

    def action_minus(self):
        text = self.ans.text()
        self.ans.setText(text + " - ")

    def action_div(self):
        text = self.ans.text()
        self.ans.setText(text + " / ")

    def action_mul(self):
        text = self.ans.text()
        self.ans.setText(text + " * ")

    def action_point(self):
        text = self.ans.text()
        self.ans.setText(text + ".")

    def action0(self):
        text = self.ans.text()
        self.ans.setText(text + "0")

    def action1(self):
        text = self.ans.text()
        self.ans.setText(text + "1")

    def action2(self):
        text = self.ans.text()
        self.ans.setText(text + "2")

    def action3(self):
        text = self.ans.text()
        self.ans.setText(text + "3")

    def action4(self):
        text = self.ans.text()
        self.ans.setText(text + "4")

    def action5(self):
        text = self.ans.text()
        self.ans.setText(text + "5")

    def action6(self):
        text = self.ans.text()
        self.ans.setText(text + "6")

    def action7(self):
        text = self.ans.text()
        self.ans.setText(text + "7")

    def action8(self):
        text = self.ans.text()
        self.ans.setText(text + "8")

    def action9(self):
        text = self.ans.text()
        self.ans.setText(text + "9")

    def action_clear(self):
        self.ans.setText("")

    def action_del(self):
        text = self.ans.text()
        self.ans.setText(text[:len(text)-1])

    def keyPressEvent(self, event):
        """Handle key events on the Calculator."""
        special_cases = {
            Qt.Key_Return: self.action_equal,
            Qt.Key_Enter: self.action_equal,
            Qt.Key_Backspace: self.action_del,
            Qt.Key_Delete: self.action_del,
            Qt.Key_Escape: self.action_clear,
        }

        # Redirect execution flow for special characters...
        if special_cases.get(event.key(), None):
            special_cases[event.key()]()
        # Only digits and operators ara vaild inputs...
        elif event.text() in string.digits + '+-*/':
            self.ans.setText(
                self.ans.text() + event.text()
            )
