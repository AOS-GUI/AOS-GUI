import typing as ty
import string

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QPushButton, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt


class calculator(QWidget):
    def __init__(self):
        super(calculator, self).__init__()
        self.setWindowTitle("AOS-GUI/calc")
        self.setFixedSize(270, 340)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setLayout(QVBoxLayout())
        self.ui()

    def ui(self):
        self.layout().setContentsMargins(10, 5, 10, 20)
        self.layout().setSpacing(20)

        # Input text Box...
        self.ans = QLineEdit(self)
        self.ans.setReadOnly(True)
        self.ans.setFont(QFont('Arial', 15))
        self.ans.setAlignment(Qt.AlignRight)
        self.ans.setFixedHeight(50)
        self.layout().addWidget(self.ans)

        # Special_buttons Layout
        top_btn_layout = QHBoxLayout()
        top_btn_layout.addWidget(QPushButton('Clear', clicked=self.ans.clear))
        top_btn_layout.addWidget(QPushButton('Del', clicked=self.ans.backspace))
        self.layout().addLayout(top_btn_layout)

        # Grid Pad numbers and operators
        pad_layout = QGridLayout()
        pad_layout.setSpacing(5)
        max_coluns = 4
        curr_row = -1

        equal_btn = QPushButton('=', clicked=self.evaluate_expr)
        equal_btn.setStyleSheet('background-color:darkred;')
        buttons = [
            '1', '2', '3', '+',
            '4', '5', '6', '-',
            '7', '8', '9', '*',
            '.', '0', None, equal_btn
        ]

        for index, btn in enumerate(buttons):
            widget = self.create_widget(
                btn, (index % max_coluns == max_coluns - 1), pad_layout
            )
            if not widget:
                continue
            if index % max_coluns == 0:
                curr_row += 1
            pad_layout.addWidget(widget, curr_row, int(index % max_coluns))

        self.layout().addLayout(pad_layout)

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
