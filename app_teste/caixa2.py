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

        self.createLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

        self.show()

    def createLayout(self):

        self.groupBox = QGroupBox("Escolha o que deseja Fazer")
        vboxlayout = QVBoxLayout()

        self.groupBoxh = QGroupBox("Escolha o que deseja Fazer")

        lineEdit_username = QLineEdit()
        lineEdit_username.setPlaceholderText('Nome Cliente')
        vboxlayout.addWidget(lineEdit_username, 1)

        lineEdit_endereco = QLineEdit()
        lineEdit_endereco.setPlaceholderText('Endereço do Cliente')
        vboxlayout.addWidget(lineEdit_endereco, 1)

        lineEdit_produto = QLineEdit()
        lineEdit_produto.setPlaceholderText('Endereço do Cliente')
        vboxlayout.addWidget(lineEdit_produto, 1)

        lineEdit_itens = QTextEdit()
        vboxlayout.addWidget(lineEdit_itens, 3)

        button_efetiva = QPushButton("Efetiva", self)
        # button.setGeometry(QRect(100, 100, 150, 50))
        button_efetiva.setIcon(QIcon("Icones/dollars.png"))
        button_efetiva.setIconSize(QSize(40, 40))
        button_efetiva.setMinimumHeight(40)
        vboxlayout.addWidget(button_efetiva)

        button_imprime = QPushButton("Imprime", self)
        # button.setGeometry(QRect(100, 100, 150, 50))
        button_imprime.setIcon(QIcon("Icones/dollars.png"))
        button_imprime.setIconSize(QSize(40, 40))
        button_imprime.setMinimumHeight(40)
        vboxlayout.addWidget(button_imprime)

        button_cancela = QPushButton("Cancela", self)
        # button.setGeometry(QRect(100, 100, 150, 50))
        button_cancela.setIcon(QIcon("Icones/dollars.png"))
        button_cancela.setIconSize(QSize(40, 40))
        button_cancela.setMinimumHeight(40)
        vboxlayout.addWidget(button_cancela)

        self.groupBox.setLayout(vboxlayout)


        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = CaixaForm()
    form.show()

    sys.exit(app.exec_())