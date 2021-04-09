# -*- coding: utf-8 -*-
import csv
import sys

from PyQt5.Qt import *
from PyQt5.QtGui import *
# from PyQt5.QtQtchart import *


class DataEntryForm(QWidget):
    def __init__(self):
        super().__init__()
        self.items = 0

        self.total = list()
        self._data = {"Phone bill": 50.5, "Gas": 30.0, "Rent": 1850.0,
                      "Car Payment": 420.0, "Comcast": 105.0,
                      "Public transportation": 60.0, "Coffee": 90.5}

        # left side
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(('Descrição', 'Preço'))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layoutRight = QVBoxLayout()


        # chart widget
        # self.chartView = QChartView()
        # self.chartView.setRenderHint(QPainter.Antialiasing)

        self.layoutRight.setSpacing(20)

        self.lbl_titulo = QLabel("Caixa")
        self.lbl_titulo.setFont(QFont("Times", 42, QFont.Bold))

        # self.lbl_titulo.setPixmap(QPixmap('Icones/add.png'))

        self.lbl_titulo.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.layoutRight.addWidget(self.lbl_titulo)


        self.lineEditCliente = QLineEdit()
        self.lineEditCliente.setPlaceholderText('Nome / Razão')
        self.layoutRight.addWidget(self.lineEditCliente)

        self.lineEditDescription = QLineEdit()
        self.lineEditDescription.setPlaceholderText('Descrição')
        self.layoutRight.addWidget(self.lineEditDescription)

        self.lineEditPrice = QLineEdit()
        self.lineEditPrice.setPlaceholderText('R$: Preço')
        self.layoutRight.addWidget(self.lineEditPrice)

        self.lbl_total = QLabel()
        self.lbl_total.setText('R$ 0.00')
        self.lbl_total.setFont(QFont("Times", 42, QFont.Bold))
        self.lbl_total.setAlignment(Qt.AlignCenter)
        self.lbl_total.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.layoutRight.addWidget(self.lbl_total)

        self.buttonAdd = QPushButton("Adicionar", self)
        self.buttonAdd.setIcon(QIcon("Icones/add.png"))
        self.buttonAdd.setIconSize(QSize(40, 40))
        self.buttonAdd.setMinimumHeight(40)

        self.buttonClear = QPushButton("Cancelar", self)
        self.buttonClear.setIcon(QIcon("Icones/clear.png"))
        self.buttonClear.setIconSize(QSize(40, 40))
        self.buttonClear.setMinimumHeight(40)

        self.buttonefetivar = QPushButton("Efetivar", self)
        self.buttonefetivar.setIcon(QIcon("Icones/dollars.png"))
        self.buttonefetivar.setIconSize(QSize(40, 40))
        self.buttonefetivar.setMinimumHeight(40)

        self.butotnPlot = QPushButton("Cupon", self)
        self.butotnPlot.setIcon(QIcon("Icones/impressora.png"))
        self.butotnPlot.setIconSize(QSize(40, 40))
        self.butotnPlot.setMinimumHeight(40)

        self.buttonQuit = QPushButton("Sair", self)
        self.buttonQuit.setIcon(QIcon("Icones/sair.png"))
        self.buttonQuit.setIconSize(QSize(40, 40))
        self.buttonQuit.setMinimumHeight(40)

        self.buttonAdd.setEnabled(False)

        self.layoutRight.addWidget(self.buttonAdd)
        self.layoutRight.addWidget(self.butotnPlot)
        self.layoutRight.addWidget(self.buttonefetivar)
        self.layoutRight.addWidget(self.buttonClear)
        self.layoutRight.addWidget(self.buttonQuit)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table, 0)
        self.layout.addLayout(self.layoutRight, 0)

        self.setLayout(self.layout)

        self.buttonQuit.clicked.connect(lambda: app.quit())
        self.buttonClear.clicked.connect(self.reset_table)
        self.butotnPlot.clicked.connect(self.graph_chart)
        self.buttonAdd.clicked.connect(self.add_entry)

        self.lineEditDescription.textChanged[str].connect(self.check_disable)
        self.lineEditPrice.textChanged[str].connect(self.check_disable)

        self.fill_table()

    def fill_table(self, data=None):
        data = self._data if not data else data

        for desc, price in data.items():
            descItem = QTableWidgetItem(desc)
            priceItem = QTableWidgetItem('${0:.2f}'.format(price))
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, descItem)
            self.table.setItem(self.items, 1, priceItem)
            self.items += 1

    def add_entry(self):
        desc = self.lineEditDescription.text()
        price = self.lineEditPrice.text()

        self.total.append(int(price))


        try:
            descItem = QTableWidgetItem(desc)
            priceItem = QTableWidgetItem('${0:.2f}'.format(float(price)))
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, descItem)
            self.table.setItem(self.items, 1, priceItem)
            self.items += 1

            ttotal = 0
            ttotal += sum(self.total)
            tot_format = ('R${0:.2f} '.format(float(ttotal)))
            self.lbl_total.setText(str(tot_format))

            self.lineEditDescription.setText('')
            self.lineEditPrice.setText('')
        except ValueError:
            pass

    def check_disable(self):
        if self.lineEditDescription.text() and self.lineEditPrice.text():
            self.buttonAdd.setEnabled(True)
        else:
            self.buttonAdd.setEnabled(False)

    def reset_table(self):
        self.table.setRowCount(0)
        self.items = 0
        self.lbl_total.setText('R$ 0.00')

        # chart = QChart()
        # self.chartView.setChart(chart)

    def graph_chart(self):
        # series = QPieSeries()

        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            val = float(self.table.item(i, 1).text().replace('$', ''))
            # series.append(text, val)

        # chart = QChart()
        # chart.addSeries(series)
        # chart.legend().setAlignment(Qt.AlignTop)
        # self.chartView.setChart(chart)


class MainWindow(QMainWindow):
    def __init__(self, w):
        super().__init__()
        self.setWindowTitle('Controle de Caixa')
        self.setWindowIcon(QIcon(r"ControleClientes/Icones/dollars.png"))
        self.resize(1200, 600)

        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('File')

        # export to csv file action
        exportAction = QAction('Export to CSV', self)
        exportAction.setShortcut('Ctrl+E')
        exportAction.triggered.connect(self.export_to_csv)

        # exit action
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(lambda: app.quit())

        self.fileMenu.addAction(exportAction)
        self.fileMenu.addAction(exitAction)

        self.setCentralWidget(w)

    def export_to_csv(self):
        try:
            with open('Expense Report.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow((w.table.horizontalHeaderItem(0).text(), w.table.horizontalHeaderItem(1).text()))
                for rowNumber in range(w.table.rowCount()):
                    writer.writerow([w.table.item(rowNumber, 0).text(), w.table.item(rowNumber, 1).text()])
                print('CSV file exported.')
            file.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = DataEntryForm()

    demo = MainWindow(w)
    demo.show()

    sys.exit(app.exec_())