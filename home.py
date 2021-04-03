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


class AboutDialog(QDialog):
    """
        Define uma nova janela onde mostra as informações
        do botão sobre
    """

    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(500)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Configurações do titulo da Janela
        layout = QVBoxLayout()

        self.setWindowTitle("Sobre")
        title = QLabel("SCC - Sistema de Controle de Clientes")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        # Configurações de atribuição de imagem
        labelpic = QLabel()
        pixmap = QPixmap('Icones/perfil.png')
        # pixmap = pixmap.scaledToWidth(400)
        pixmap = pixmap.scaled(QSize(500, 500))
        labelpic.setPixmap(pixmap)
        # labelpic.setFixedHeight(400)
        layout.addWidget(title)
        layout.addWidget(labelpic)

        layout.addWidget(QLabel("Versão:V1.0"))
        layout.addWidget(QLabel("Nome: Alexandre Leonel de Oliveira"))
        layout.addWidget(QLabel("Nascido em: São Paulo em 26 de Junho de 1974"))
        layout.addWidget(QLabel("Profissão: Bacharel em Sistemas de Informação"))
        layout.addWidget(QLabel("Copyright Bi-Black-info 2021"))

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


class CadastroClientes(QDialog):
    """
        Define uma nova janela onde cadastramos os clientes
    """

    def __init__(self, *args, **kwargs):
        super(CadastroClientes, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        # Configurações do titulo da Janela
        self.setWindowTitle("Add Cliente :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Dados do Cliente :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.addcliente)

        layout = QVBoxLayout()

        # Insere o ramo ou tipo /
        self.branchinput = QComboBox()
        self.branchinput.addItem("Pessoa Física")
        self.branchinput.addItem("Empresa")
        layout.addWidget(self.branchinput)

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Nome / Razão")
        layout.addWidget(self.nameinput)

        self.cpfinput = QLineEdit()
        self.cpfinput.setPlaceholderText("Cpf")
        layout.addWidget(self.cpfinput)

        self.rginput = QLineEdit()
        self.rginput.setPlaceholderText("R.G")
        layout.addWidget(self.rginput)

        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Telefone NO.")
        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Endereço")
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addcliente(self):
        """
        captura as informações digitadas
        no lineedit e armazena nas variaveis
        :return:
        """
        nome = ""
        tipo = ""
        cpf = ""
        rg = ""
        tel = ""
        endereco = ""

        nome = self.nameinput.text()
        tipo = self.branchinput.itemText(self.branchinput.currentIndex())
        cpf = self.cpfinput.text()
        rg = self.rginput.text()
        # sem = -self.seminput.itemText(self.seminput.currentIndex())
        tel = self.mobileinput.text()
        endereco = self.addressinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "INSERT INTO clientes (tipo, nome, cpf, rg, telefone, endereco)" \
                          "VALUES (%s,%s,%s,%s,%s,%s)"
            dados = tipo, nome, cpf, rg, tel, endereco
            self.cursor.execute(comando_sql, dados)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Cadastro', 'Dados inseridos com sucesso!')
            self.close()

        except Exception:

            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A inserção falhou!')


class DeleteClientes(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteClientes, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        self.setWindowTitle("Deletar Cliente")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de deletar
        self.QBtn.clicked.connect(self.deletecliente)

        layout = QVBoxLayout()

        # Cria as caixas de digitação e
        # verifica se é um numero
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Codigo do cliente - somente número")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletecliente(self):
        delroll = ""
        delroll = self.deleteinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql = "DELETE FROM clientes WHERE codigo = " + str(delroll)
            self.cursor.execute(consulta_sql)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Deleção realizada com sucesso!', 'DELETADO COM SUCESSO!')
            self.close()

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A Deleção falhou!')


class ComboPreco(QComboBox):
    def __init__(self, parent):
        super(ComboPreco, self).__init__(parent)

        self.cursor = conexao.banco.cursor()
        consulta_sql = "SELECT * FROM clientes"
        self.cursor.execute(consulta_sql)
        result = self.cursor.fetchall()

        busca = []
        for row in range(len(result)):
            busca.append(str(result[row][0]))

        print(busca)
        self.setStyleSheet('font-size: 25px')
        self.addItems(busca)
        self.currentIndexChanged.connect(self.getComboValue)

    def getComboValue(self):

        return self.currentText()


class CadastroProdutos(QDialog):
    """
        Define uma nova janela onde cadastramos os clientes
    """

    def __init__(self, *args, **kwargs):
        super(CadastroProdutos, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        # Configurações do titulo da Janela
        self.setWindowTitle("Add Produto :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Descição do Produto :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.addproduto)

        layout = QVBoxLayout()

        # Insere o ramo ou tipo /
        self.uninput = QComboBox()
        self.uninput.addItem("UN")
        self.uninput.addItem("PÇ")
        self.uninput.addItem("KG")
        self.uninput.addItem("LT")
        self.uninput.addItem("PT")
        self.uninput.addItem("CX")
        layout.addWidget(self.uninput)

        self.descricaoinput = QLineEdit()
        self.descricaoinput.setPlaceholderText("Descrição")
        layout.addWidget(self.descricaoinput)

        self.ncminput = QLineEdit()
        self.ncminput.setPlaceholderText("NCM")
        layout.addWidget(self.ncminput)

        self.precoinput = QLineEdit()
        self.precoinput.setPlaceholderText("Preço.")
        layout.addWidget(self.precoinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addproduto(self):
        """
        captura as informações digitadas
        no lineedit e armazena nas variaveis
        :return:
        """
        descricao = ""
        ncm = ""
        un = ""
        preco = ""

        descricao = self.descricaoinput.text()
        ncm = self.ncminput.text()
        un = self.uninput.itemText(self.uninput.currentIndex())
        preco = self.precoinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "INSERT INTO produtos (descricao, ncm, un, preco)" \
                          "VALUES (%s,%s,%s,%s)"
            dados = descricao, ncm, un, str(preco)
            self.cursor.execute(comando_sql, dados)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Cadastro', 'Dados inseridos com sucesso!')
            self.close()

        except Exception:

            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A inserção falhou!')


class ListProdutos(QMainWindow):
    def __init__(self):
        super(ListProdutos, self).__init__()
        self.setWindowIcon(QIcon('Icones/produtos2.png'))

        # cria banco de dados se ele não existir
        self.cursor = conexao.banco.cursor()
        self.comando_sql = "CREATE TABLE IF NOT EXISTS produtos(\
                                    codigo INT PRIMARY KEY AUTO_INCREMENT,\
                                    descricao VARCHAR(60),\
                                    ncm VARCHAR(20),\
                                    un VARCHAR(2),\
                                    preco FLOAT)"
        self.cursor.execute(self.comando_sql)
        self.cursor.close()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PRODUTOS")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(5)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Codigo", "Descrição", "NCM", "UN", "Preço",))

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM produtos"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("Icones/add.png"), "Add Produto", self)
        btn_ac_adduser.triggered.connect(self.cadProdutos)
        btn_ac_adduser.setStatusTip("Add Produto")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(QIcon("Icones/atualizar.png"), "Atualizar dados do produto", self)
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(QIcon("Icones/pesquisa.png"), "Pesquisar dados por produto", self)
        # btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        self.show()

    def loaddata(self):

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM produtos"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadProdutos(self):
        dlg = CadastroProdutos()
        dlg.exec()


class ListClientes(QMainWindow):
    def __init__(self):
        super(ListClientes, self).__init__()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # self.setHorizontalHeaderLabels(list(''))
        # self.setColumnWidth(4, 200)
        # self.verticalHeader().setDefaultSectionSize(25)
        # self.horizontalHeader().setDefaultSectionSize(250)
        #
        # combo = ComboPreco(self)
        # self.setCellWidget(0, 0, combo)

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(6)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Codigo", "Tipo", "Nome", "CPF", "RG", "Tel", "Endereco",))

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM clientes"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)

        for i in range(0, len(result)):
            for j in range(0, 7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("Icones/clientes.png"), "Cadastro de Cliente", self)
        btn_ac_adduser.triggered.connect(self.cadClientes)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(QIcon("Icones/atualizar.png"), "Atualizar dados do Cliente", self)
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(QIcon("Icones/pesquisa.png"), "Pesquisar dados por Cliente", self)
        # btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("Icones/deletar.png"), "Deletar o Cliente", self)
        # btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        self.show()

    def loaddata(self):

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM clientes"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)

        for i in range(0, len(result)):
            for j in range(0, 7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadClientes(self):
        dlg = CadastroClientes()
        dlg.exec()

# Tela principal onde eu chamo as telas de
# cadastro de clientes
# cadastro de Produtos


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('Icones/perfil.png'))

        # cria um menu
        file_menu = self.menuBar().addMenu("&Arquivo")
        help_menu = self.menuBar().addMenu("&Ajuda")

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE")
        self.setMinimumSize(800, 600)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("Icones/clientes.png"), "Listar/Cadastrar de Cliente", self)
        btn_ac_adduser.triggered.connect(self.listClientes)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_produto = QAction(QIcon("Icones/produtos2.png"), "Lista/Cadastrar Produtos", self)
        btn_ac_produto.triggered.connect(self.listProdutos)
        btn_ac_produto.setStatusTip("Produtos")
        toolbar.addAction(btn_ac_produto)

        btn_ac_estoque = QAction(QIcon("Icones/estoque.png"), "Lista/Cadastraro Estoque", self)
        btn_ac_estoque.setStatusTip("Estoque")
        toolbar.addAction(btn_ac_estoque)

        btn_ac_caixa = QAction(QIcon("Icones/dollars.png"), "Caixa - abre o Caixa", self)
        # btn_ac_caixa.triggered.connect(self.listClientes)
        btn_ac_caixa.setStatusTip("Caixa")
        toolbar.addAction(btn_ac_caixa)

        # Arquivo >> Adicionar
        adduser_action = QAction(QIcon("Icones/clientes.png"), "Listar/Cadastrar de Cliente", self)
        adduser_action.triggered.connect(self.listClientes)
        file_menu.addAction(adduser_action)

        btn_ac_produto = QAction(QIcon("Icones/produtos2.png"), "Listar/Cadastrar Produtos", self)
        btn_ac_produto.triggered.connect(self.listProdutos)
        file_menu.addAction(btn_ac_produto)

        btn_ac_estoque = QAction(QIcon("Icones/estoque.png"), "Lista/Cadastraro Estoque", self)
        # btn_ac_produto.triggered.connect(self.listEstoque)
        file_menu.addAction(btn_ac_estoque)

        btn_ac_caixa = QAction(QIcon("Icones/dollars.png"), "Caixa", self)
        # btn_ac_caixa.triggered.connect(self.listClientes)
        file_menu.addAction(btn_ac_caixa)

        about_action = QAction(QIcon("Icones/sobre-nos.png"), "Desenvolvedores", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    def listClientes(self):
        dlg = ListClientes()
        dlg.exec()

    def listProdutos(self):
        dlg = ListProdutos()
        dlg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
if QDialog.Accepted:
    window = MainWindow()
    window.show()
    # window.loaddata()
sys.exit((app.exec_()))
