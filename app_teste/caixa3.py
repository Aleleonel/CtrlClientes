from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *

import time
import os
import sys

import mysql.connector
from mysql.connector import OperationalError

import conexao


class CaixaForm(QWidget):
    def __init__(self):
        super(CaixaForm, self).__init__()

        self.title = "Controle de Caixa"
        self.left = 300
        self.top = 100
        self.width = 800
        self.heigth = 600
        self.iconName = "Icones/dollars.png"

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.heigth)
        dlgLayout = QVBoxLayout()

        # Create a form layout and add widgets
        formLayout = QFormLayout()
        formLayout.addRow("Name:", QLineEdit())
        formLayout.addRow("Job:", QLineEdit())
        formLayout.addRow("Email:", QLineEdit())
        formLayout.addRow("Itens:", QTextEdit())


        # Add a button box
        btnBox = QDialogButtonBox()
        btnBox2 = QDialogButtonBox()

        btnBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        )
        btnBox2.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        )
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(btnBox)
        dlgLayout.addWidget(btnBox2)
        self.setLayout(dlgLayout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = CaixaForm()
    dlg.show()
    sys.exit(app.exec_())