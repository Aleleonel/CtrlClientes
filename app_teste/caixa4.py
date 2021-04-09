# -*- coding: utf-8 -*-
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


class ComboItens(QComboBox):
    def __init__(self, parent):
        super(ComboItens, self).__init__(parent)
        self.setStyleSheet('font-size: 25px')
        self.addItems(['Produto_1', 'Produto_2', 'Produto_03', 'Produto_04'])
        self.currentIndexChanged.connect(self.getComboValue)

    def getComboValue(self):
        print(self.currentText())


class TableWidget(QTableWidget):
    def __init__(self):
        super(TableWidget, self).__init__(1, 4)

        self.setHorizontalHeaderLabels(("Código", "Itens", "Quantidade", "Preço"))
        self.setColumnWidth(4, 200)
        self.verticalHeader().setDefaultSectionSize(30)
        self.horizontalHeader().setDefaultSectionSize(250)

        combo = ComboItens(self)
        self.setCellWidget(0, 0, combo)


class Caixa(QWidget):
    def __init__(self):
        super(Caixa, self).__init__()
        self.resize(1600, 600)

        mainLayout = QHBoxLayout()
        table = TableWidget()
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = Caixa()
    dlg.show()
    sys.exit(app.exec_())
