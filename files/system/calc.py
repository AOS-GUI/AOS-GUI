import typing as ty
import string

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QPushButton, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt, QRect


class calculator(QWidget):
    def __init__(self):
        super(calculator, self).__init__()
        self.setWindowTitle("AOS-GUI/calc")
        self.setFixedSize(270, 340)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setLayout(QVBoxLayout())
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

        # Overwrite some special cases...
        self.push_equal.clicked.connect(self.evaluate_expr)
        self.push_clear.clicked.connect(self.ans.clear)
        self.push_del.clicked.connect(self.ans.backspace)

        special_cases = [
            self.push_equal, self.push_clear, self.push_del
        ]

        # Grabbing all buttons in the calculator instance.
        buttons = filter(
            lambda attr: isinstance(attr, QPushButton),
            vars(self).values()
        )

        # Connect all buttons, except for the special_cases...
        for btn in buttons:
            if btn in special_cases:
                continue
            btn.clicked.connect(self._push_text(btn.text()))

    def create_widget(
        self, btn: ty.Union[str, None, QPushButton], operator: bool,
        pad_layout: QGridLayout
    ) -> ty.Optional[QPushButton]:
        """Create QPushButton for PadLayout dynamically."""

        if not btn:
            return None

        if isinstance(btn, QPushButton):
            widget = btn
        else:
            widget = QPushButton(
                btn, clicked=self._push_text(btn)
            )
            widget.setMinimumHeight(int(widget.sizeHint().height() * 1.70))

        if operator:
            widget.setMinimumHeight(int(widget.sizeHint().height() * 1.95))
            # Custom style for the Operators buttons, if needed...
            #  if not widget.styleSheet():
            #      widget.setStyleSheet(
            #          'background-color:#020202;'
            #          'border-color: white;'
            #          'border-style: solid;'
            #          'border-width: 1px;'
            #          'color: white;'
            #      )
        return widget

    def _push_text(self, text):
        """Cloujure for buttons click action.

        Returns a function that will append a given text to the ans input box.
        """
        ans = self.ans

        def inner(*args, **kwargs):
            ans.setText(ans.text() + text)

        return inner

    def evaluate_expr(self):
        try:
            self.ans.setText(
                str(eval(self.ans.text()))
            )
        except:
            # TODO: Report the error in a log message, that the OS will handle.
            self.ans.setText("NaN")

    def keyPressEvent(self, event):
        """Handle key events on the Calculator."""
        special_cases = {
            Qt.Key.Key_Return: self.evaluate_expr,
            Qt.Key.Key_Enter: self.evaluate_expr,
            Qt.Key.Key_Backspace: self.ans.backspace,
            Qt.Key.Key_Delete: self.ans.backspace,
            Qt.Key.Key_Escape: self.ans.clear,
        }

        # Redirect execution flow for special characters...
        if special_cases.get(event.key(), None):
            special_cases[event.key()]()
        # Only digits and operators ara vaild inputs...
        elif event.text() in string.digits + '+-*/':
            self.ans.setText(
                self.ans.text() + event.text()
            )
