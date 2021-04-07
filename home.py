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

global loginok


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


class CadastroEstoque(QDialog):
    """
        Define uma nova janela onde cadastramos os clientes
    """

    def __init__(self, *args, **kwargs):
        super(CadastroEstoque, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        # Configurações do titulo da Janela
        self.setWindowTitle("Add Estoque :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Descição do Produto :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.cursor = conexao.banco.cursor()
        consulta_sql = "SELECT * FROM produtos"
        self.cursor.execute(consulta_sql)
        result = self.cursor.fetchall()

        # conexao.banco.commit()
        # self.cursor.close()

        self.QBtn.clicked.connect(self.addproduto)

        layout = QVBoxLayout()

        # Insere o ramo ou tipo /
        self.codigoinput = QComboBox()
        busca = []
        for row in range(len(result)):
            busca.append(str(result[row][0]))
        for i in range(len(busca)):
            self.codigoinput.addItem(str(busca[i]))

        layout.addWidget(self.codigoinput)

        self.statusinput = QLineEdit()
        self.statusinput.setPlaceholderText("E")
        layout.addWidget(self.statusinput)

        # Insere o ramo ou tipo /

        self.descricaoinput = QLineEdit()
        self.descricaoinput.setPlaceholderText("Descrição")
        layout.addWidget(self.descricaoinput)

        self.precoinput = QLineEdit()
        self.precoinput.setPlaceholderText("Preço de Compra")
        layout.addWidget(self.precoinput)

        self.qtdinput = QLineEdit()
        self.qtdinput.setPlaceholderText("Quantidade")
        layout.addWidget(self.qtdinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addproduto(self):
        """
        captura as informações digitadas
        no lineedit e armazena nas variaveis
        :return:
        """
        self.cursor = conexao.banco.cursor()
        consulta_sql = ("SELECT * FROM produtos WHERE codigo =" + str(self.codigoinput.itemText(
            self.codigoinput.currentIndex())))
        self.cursor.execute(consulta_sql)
        valor_codigo = self.cursor.fetchall()

        for i in range(len(valor_codigo)):
            dados_lidos = valor_codigo[i][1]

        print(dados_lidos)

        codigo = ""
        quantidade = ""
        preco = ""
        status = "E"

        codigo = self.codigoinput.itemText(self.codigoinput.currentIndex())
        self.descricaoinput.setText(dados_lidos)

        preco = self.precoinput.text()
        quantidade = self.qtdinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "INSERT INTO estoque (idproduto, estoque, status)" \
                          "VALUES (%s, %s, %s)"
            dados = codigo, quantidade, status
            self.cursor.execute(comando_sql, dados)

            consulta_sql_preco = "INSERT INTO precos (idprecos, preco) VALUES (%s, %s)"
            dados_preco = codigo, preco
            self.cursor.execute(consulta_sql_preco, dados_preco)
            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Cadastro', 'Dados inseridos com sucesso!')
            self.close()

        except Exception:

            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A inserção falhou!')


class ListEstoque(QMainWindow):
    def __init__(self):
        super(ListEstoque, self).__init__()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE ESTOQUE")
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
        self.tableWidget.setHorizontalHeaderLabels(
            ("Codigo", "Descrição", "Preço de Compra", "Quantidade", "Atualização",))

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT a.codigo, a.descricao, b.preco, e.estoque, e.ultupdate FROM controle_clientes.produtos" \
                      " as a" \
                      " LEFT JOIN controle_clientes.precos as b on b.idprecos = a.codigo" \
                      " LEFT JOIN controle_clientes.estoque as e ON e.idproduto = a.codigo;"
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
        btn_ac_adduser = QAction(QIcon("Icones/add.png"), "Cadastro Estoque morto", self)
        btn_ac_adduser.triggered.connect(self.cadEstoque)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(QIcon("Icones/atualizar.png"), "Atualizar dados do Cliente", self)
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(QIcon("Icones/pesquisa.png"), "Pesquisar dados por Cliente", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("Icones/deletar.png"), "Deletar o Cliente", self)
        # btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        self.show()

    def loaddata(self):

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT a.codigo, a.descricao, b.preco, e.estoque, e.ultupdate FROM controle_clientes.produtos" \
                      " as a" \
                      " LEFT JOIN controle_clientes.precos as b on b.idprecos = a.codigo" \
                      " LEFT JOIN controle_clientes.estoque as e ON e.idproduto = a.codigo;"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadEstoque(self):
        dlg = CadastroEstoque()
        dlg.exec()
        self.loaddata()

    def search(self):
        dlg = SearchEstoque()
        dlg.exec_()

    # def delete(self):
    #     dlg = DeleteEstoque()
    #     dlg.exec_()


class SearchEstoque(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(SearchEstoque, self).__init__(*args, **kwargs)

        self.cursor = conexao.banco.cursor()
        self.QBtn = QPushButton()
        self.QBtn.setText("Procurar")

        self.setWindowTitle("Pesquisar Produto em Estoque")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de busca
        self.QBtn.clicked.connect(self.searchProdEstoque)

        layout = QVBoxLayout()

        # Cria as caixas de digitaçãoe e
        # verifica se é um numero
        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Codigo do Produto - somente número")
        layout.addWidget(self.searchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    # busca o produto pelo codigo
    def searchProdEstoque(self):
        searchroll = ""
        searchroll = self.searchinput.text()

        try:
            consulta_estoque = "SELECT * FROM controle_clientes.estoque WHERE idproduto=" + str(searchroll)
            self.cursor.execute(consulta_estoque)
            result_estoque = self.cursor.fetchall()
            for row in range(len(result_estoque)):
                searchresult1 = "Codigo : " + str(result_estoque[0][0]) + '\n'

            consulta_produto = "SELECT * FROM controle_clientes.produtos WHERE codigo=" + str(searchroll)
            self.cursor.execute(consulta_produto)
            result_produto = self.cursor.fetchall()
            for row in range(len(result_produto)):
                searchresult2 = "Descrição : " + str(result_produto[0][1])

            mostra = searchresult1 + searchresult2

            QMessageBox.information(QMessageBox(), 'Pesquisa realizada com sucesso!', mostra)

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A pesquisa falhou!')


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
        self.tableWidget.setColumnCount(6)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Codigo", "Descrição", "NCM", "UN", "Preço", "Estoque",))

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT a.codigo, a.descricao, a.ncm, a.un, a.preco, e.estoque FROM " \
                      "controle_clientes.produtos " \
                      "as a LEFT JOIN controle_clientes.precos as b on b.idprecos = a.codigo LEFT JOIN " \
                      "controle_clientes.estoque as e ON e.idproduto = a.codigo; "
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(6)

        for i in range(0, len(result)):
            for j in range(0, 6):
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

        btn_ac_delete = QAction(QIcon("Icones/deletar.png"), "Deletar o Produto", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        btn_ac_search = QAction(QIcon("Icones/pesquisa.png"), "Pesquisar dados por produto", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        self.show()

    def loaddata(self):

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT a.codigo, a.descricao, a.ncm, a.un, a.preco, e.estoque FROM " \
                      "controle_clientes.produtos " \
                      "as a LEFT JOIN controle_clientes.precos as b on b.idprecos = a.codigo LEFT JOIN " \
                      "controle_clientes.estoque as e ON e.idproduto = a.codigo; "
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(6)

        for i in range(0, len(result)):
            for j in range(0, 6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadProdutos(self):
        dlg = CadastroProdutos()
        dlg.exec()
        self.loaddata()

    def search(self):
        dlg = SearchProdutos()
        dlg.exec_()

    def delete(self):
        dlg = DeleteProduto()
        dlg.exec_()
        self.loaddata()


class SearchProdutos(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(SearchProdutos, self).__init__(*args, **kwargs)

        self.cursor = conexao.banco.cursor()
        self.QBtn = QPushButton()
        self.QBtn.setText("Procurar")

        self.setWindowTitle("Pesquisar Produto")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de busca
        self.QBtn.clicked.connect(self.searchcliente)

        layout = QVBoxLayout()

        # Cria as caixas de digitaçãoe e
        # verifica se é um numero
        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Codigo do Produto - somente número")
        layout.addWidget(self.searchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    # busca o cliente pelo codigo
    def searchcliente(self):
        searchroll = ""
        searchroll = self.searchinput.text()

        try:
            consulta_sql = "SELECT * FROM produtos WHERE codigo = " + str(searchroll)
            self.cursor.execute(consulta_sql)
            result = self.cursor.fetchall()

            for row in range(len(result)):
                searchresult = "Codigo : " + str(result[0][0]) \
                               + '\n' + "Descrição : " + str(result[0][1]) \
                               + '\n' + "NCM : " + str(result[0][2]) \
                               + '\n' + "UN : " + str(result[0][3]) \
                               + '\n' + "Preço : " + str(result[0][4])

            QMessageBox.information(QMessageBox(), 'Pesquisa realizada com sucesso!', searchresult)

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A pesquisa falhou!')


class DeleteProduto(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteProduto, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        self.setWindowTitle("Deletar Produto")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de deletar
        self.QBtn.clicked.connect(self.deleteproduto)

        layout = QVBoxLayout()

        # Cria as caixas de digitação e
        # verifica se é um numero
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Codigo do produto - somente número")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteproduto(self):
        delroll = ""
        delroll = self.deleteinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql = "DELETE FROM produtos WHERE codigo = " + str(delroll)
            self.cursor.execute(consulta_sql)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(QMessageBox(), 'Deleção realizada com sucesso!', 'PRODUTO DELETADO COM SUCESSO!')
            self.close()

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A Deleção falhou!')


class ListClientes(QMainWindow):
    def __init__(self):
        super(ListClientes, self).__init__()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(7)
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
        btn_ac_adduser = QAction(QIcon("Icones/add.png"), "Cadastro de Cliente", self)
        btn_ac_adduser.triggered.connect(self.cadClientes)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(QIcon("Icones/atualizar.png"), "Atualizar dados do Cliente", self)
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(QIcon("Icones/pesquisa.png"), "Pesquisar dados por Cliente", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("Icones/deletar.png"), "Deletar o Cliente", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        btn_ac_sair = QAction(QIcon("Icones/sair.png"), "Sair", self)
        # btn_ac_sair.triggered.connect(self.fechaTela)
        btn_ac_sair.setStatusTip("Sair ")
        toolbar.addAction(btn_ac_sair)

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
        self.loaddata()

    def search(self):
        dlg = SearchClientes()
        dlg.exec_()

    def delete(self):
        dlg = DeleteCliente()
        dlg.exec_()
        self.loaddata()


class SearchClientes(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(SearchClientes, self).__init__(*args, **kwargs)

        self.cursor = conexao.banco.cursor()
        self.QBtn = QPushButton()
        self.QBtn.setText("Procurar")

        self.setWindowTitle("Pesquisar Cliente")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de busca
        self.QBtn.clicked.connect(self.searchcliente)

        layout = QVBoxLayout()

        # Cria as caixas de digitaçãoe e
        # verifica se é um numero
        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Codigo do cliente - somente número")
        layout.addWidget(self.searchinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    # busca o cliente pelo codigo
    def searchcliente(self):
        searchroll = ""
        searchroll = self.searchinput.text()

        try:
            consulta_sql = "SELECT * FROM clientes WHERE codigo = " + str(searchroll)
            self.cursor.execute(consulta_sql)
            result = self.cursor.fetchall()

            for row in range(len(result)):
                searchresult = "Codigo : " + str(result[0][0]) \
                               + '\n' + "Tipo : " + str(result[0][1]) \
                               + '\n' + "Nome : " + str(result[0][2]) \
                               + '\n' + "CPF : " + str(result[0][3]) \
                               + '\n' + "R.G : " + str(result[0][4]) \
                               + '\n' + "Tel : " + str(result[0][5]) \
                               + '\n' + "Ender. : " + str(result[0][6])

            QMessageBox.information(QMessageBox(), 'Pesquisa realizada com sucesso!', searchresult)

        except Exception:
            QMessageBox.warning(QMessageBox(), 'aleleonel@gmail.com', 'A pesquisa falhou!')

        # finally:
        #     if conexao.banco.is_connected():
        #         conexao.banco.close()
        #         self.cursor.close()
        #         print("Conexão ao MySQL encerrada")


class DeleteCliente(QDialog):
    """
        Define uma nova janela onde executaremos
        a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteCliente, self).__init__(*args, **kwargs)

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

        btn_ac_estoque = QAction(QIcon("Icones/estoque.png"), "Lista/Cadastro Estoque", self)
        btn_ac_estoque.triggered.connect(self.listEstoque)
        btn_ac_estoque.setStatusTip("Estoque")
        toolbar.addAction(btn_ac_estoque)

        btn_ac_caixa = QAction(QIcon("Icones/dollars.png"), "Caixa - abre o Caixa", self)
        # btn_ac_caixa.triggered.connect(self.listClientes)
        btn_ac_caixa.setStatusTip("Caixa")
        toolbar.addAction(btn_ac_caixa)

        btn_ac_fechar = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_fechar.triggered.connect(self.fechaTela)
        btn_ac_fechar.setStatusTip("Sair")
        toolbar.addAction(btn_ac_fechar)

        # Arquivo >> Adicionar
        adduser_action = QAction(QIcon("Icones/clientes.png"), "Listar/Cadastrar de Cliente", self)
        adduser_action.triggered.connect(self.listClientes)
        file_menu.addAction(adduser_action)

        btn_ac_produto = QAction(QIcon("Icones/produtos2.png"), "Listar/Cadastrar Produtos", self)
        btn_ac_produto.triggered.connect(self.listProdutos)
        file_menu.addAction(btn_ac_produto)

        btn_ac_estoque = QAction(QIcon("Icones/estoque.png"), "Lista/Cadastro Estoque", self)
        btn_ac_estoque.triggered.connect(self.listEstoque)
        file_menu.addAction(btn_ac_estoque)

        btn_ac_caixa = QAction(QIcon("Icones/dollars.png"), "Caixa", self)
        # btn_ac_caixa.triggered.connect(self.caixa)
        file_menu.addAction(btn_ac_caixa)

        btn_ac_fechar = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_fechar.triggered.connect(self.fechaTela)
        file_menu.addAction(btn_ac_fechar)

        about_action = QAction(QIcon("Icones/sobre-nos.png"), "Desenvolvedores", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        # self.show()
        self.showFullScreen()

    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    def listClientes(self):
        dlg = ListClientes()
        dlg.exec()

    def listProdutos(self):
        dlg = ListProdutos()
        dlg.exec()

    def listEstoque(self):
        dlg = ListEstoque()
        dlg.exec()

    def fechaTela(self, event):
        replay = QMessageBox.question(self, 'Window close', 'Tem certeza de que deseja sair?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            sys.exit()

        else:
            event.ignore()


def telaprincipal():
    dlg = MainWindow()
    dlg.exec_()


class LoginForm(QWidget):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setWindowTitle('Login')
        self.resize(500, 120)

        layout = QGridLayout()

        label_nome = QLabel('<font size="4"> Usuário </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Nome de Usuário')
        layout.addWidget(label_nome, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_senha = QLabel('<font size="4"> Senha </font>')
        self.lineEdit_senha = QLineEdit()
        self.lineEdit_senha.setPlaceholderText('sua senha aqui')
        layout.addWidget(label_senha, 1, 0)
        layout.addWidget(self.lineEdit_senha, 1, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_senha)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

    def check_senha(self):

        msg = QMessageBox()

        usuario = self.lineEdit_username.text()
        senha = self.lineEdit_senha.text()
        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT senha FROM usuarios WHERE nome ='{}' ".format(usuario)

        try:
            self.cursor.execute(comando_sql)
            senha_bd = self.cursor.fetchall()

        except Exception as e:
            msg.setText("Credenciais Incorretas")
            msg.exec_()

        if senha == senha_bd[0][0]:
            self.hide()
            telaprincipal()
            msg.setText("Sucesso")
            msg.exec_()
            conexao.banco.close()
        else:
            msg.setText("Credenciais Incorretas")
            msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

if QDialog.Accepted:
    form = LoginForm()
    form.show()

sys.exit((app.exec_()))
