from banco import conn
from produto import Produto
import sys

conexao = conn()
class Sistema:
    def __init__(self):
        self.cursor = conexao.cursor()

    def interface(self):
        print("---------- Mercearia Boa Vista ----------\n")
        print("Escolha a opção que você deseja: ")
        print("1 - Cadastrar produto \n2 - Vender produto \n3 - Buscar produto \n4 - Listar produtos \n5 - Adicionar estoque \n6 - Sair\n")

    def cadastrar_produto(self):
        nome = input("Digite o nome do produto: ")
        marca = input("Digite a marca do produto: ")
        preco = float(input("Digite o preço do produto: "))
        quantidade = int(input("Digite a quantidade do produto: "))
        produto = Produto(nome, marca, preco, quantidade)
        sql = "INSERT INTO produtos (nome, marca, preco, quantidade) VALUES(%s, %s, %s, %s)"

        self.cursor.execute(sql, (produto.nome, produto.marca, produto.preco, produto.quantidade))

        conexao.commit()
        print("Produto cadastrado com sucesso!\n")

    def vender_produto(self):
        produto_id = int(input("Digite o id do produto: "))
        quantidade = int(input("Digite a quantidade desejada: "))
        sql = "UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s AND quantidade >= %s"
        self.cursor.execute(sql, (quantidade, produto_id, quantidade))

        if self.cursor.rowcount == 0:
            print("Produto não encontrado ou estoque insuficiente.\n")
        else:
            conexao.commit()
            print("Venda realizada com sucesso!")

    def buscar_produto(self):
        produto_id = int(input("Digite o ID do produto: "))

        sql = "SELECT * FROM produtos WHERE id = %s"

        self.cursor.execute(sql, (produto_id,))

        resultado = self.cursor.fetchone()

        if not resultado:
            print("Produto não encontrado.\n")
        else:
            print(f"\nProduto: {resultado[1]} {resultado[2]} \nPreço: {resultado[3]} Quantidade: {resultado[4]}\n")

    def listar_produtos(self):
        sql = "SELECT * FROM produtos"

        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()

        if not resultado:
            print("Nenhum produto registrado!\n")
        else:
            for produto in resultado:
                print(f"\nProduto: {produto[1]} {produto[2]} \nPreço: {produto[3]} \nQuantidade em estoque: {produto[4]}\n")

    def adicionar_estoque(self):
        produto_id = int(input("Digite o ID do produto: "))
        quantidade = int(input("Digite a quantidade a ser adicionado: "))

        sql = "UPDATE produtos SET quantidade = quantidade + %s WHERE id = %s"

        self.cursor.execute(sql, (quantidade, produto_id))

        conexao.commit()
        print(f"{quantidade} unidade(s) adicionado ao estoque.\n")

    def sair(self):
        sys.exit()

sistema = Sistema()

while True:
    sistema.interface()
    opcao = int(input("Digite a opção desejada: "))
    match(opcao):
        case 1:
            sistema.cadastrar_produto()
        case 2:
            sistema.vender_produto()
        case 3:
            sistema.buscar_produto()
        case 4:
            sistema.listar_produtos()
        case 5:
            sistema.adicionar_estoque()
        case 6:
            sistema.sair()
        case _:
            print("Opção inválida")