from tkinter import messagebox

from aiofiles.threadpool import text
from banco import conn
from produto import Produto
import sys
import customtkinter as ctk


class Sistema:
    def __init__(self):
        self.conexao = conn()
        self.cursor = self.conexao.cursor()
        self.app = ctk.CTk()
        self.app.title("Controle de estoque")
        self.app.geometry("400x450")

        ctk.CTkButton(
            self.app,
            text="Cadastrar produto",
            command=self.cadastrar_produto
        ).pack(pady=10)
        ctk.CTkButton(
            self.app,
            text="Vender produto",
            command=self.vender_produto
        ).pack(pady=10)
        ctk.CTkButton(
            self.app,
            text="Buscar produto",
            command=self.buscar_produto
        ).pack(pady=10)
        ctk.CTkButton(
            self.app,
            text="Listar produto",
            command=self.listar_produtos
        ).pack(pady=10)
        ctk.CTkButton(
            self.app,
            text="Adicionar estoque",
            command=self.adicionar_estoque
        ).pack(pady=10)
        ctk.CTkButton(
            self.app,
            text="sair",
            command=self.sair
        ).pack(pady=10)


        self.app.mainloop()

    def interface(self):
        print("---------- Mercearia Boa Vista ----------\n")
        print("Escolha a opção que você deseja:")
        print(
            "1 - Cadastrar produto\n"
            "2 - Vender produto\n"
            "3 - Buscar produto\n"
            "4 - Listar produtos\n"
            "5 - Adicionar estoque\n"
            "6 - Sair\n"
        )

    def cadastrar_produto(self):
        janela = ctk.CTkToplevel(self.app)
        janela.title("Cadastrar produto - Controle de Estoque")
        janela.geometry("400x400")

        container = ctk.CTkFrame(janela)
        container.pack(fill="both", expand=True, padx=25, pady=25)

        ctk.CTkLabel(container, text="Nome do produto:").pack(anchor="w", padx=(20, 0), pady=(5, 8))
        nome = ctk.CTkEntry(container, width=300)
        nome.pack(anchor="w", padx=(20, 0), pady=(0, 10))

        ctk.CTkLabel(container, text="Marca:").pack(anchor="w", padx=(20, 0), pady=(0, 5))
        marca = ctk.CTkEntry(container, width=300)
        marca.pack(anchor="w", padx=(20, 0), pady=(0, 10))

        ctk.CTkLabel(container, text="Preço:").pack(anchor="w", padx=(20, 0), pady=(0, 5))
        preco = ctk.CTkEntry(container, width=300)
        preco.pack(anchor="w", padx=(20, 0), pady=(0, 10))

        ctk.CTkLabel(container, text="Quantidade:").pack(anchor="w", padx=(20, 0), pady=(0, 5))
        quantidade = ctk.CTkEntry(container, width=300)
        quantidade.pack(anchor="w", padx=(20, 0), pady=(0, 10))

        self.card_produto = ctk.CTkFrame(self.app)
        self.card_produto.pack(fill="x", padx=10, pady=10)

        def salvar():
            nome_produto = nome.get().strip()
            marca_produto = marca.get().strip()
            preco_produto = preco.get().strip()
            quantidade_produto = quantidade.get().strip()

            if not nome_produto or not marca_produto or not preco_produto or not quantidade_produto:
                print("Preencha todos os campos")
                return

            try:
                preco_valor = float(preco_produto.replace(',', '.'))
                quantidade_valor = int(quantidade_produto)
            except ValueError:
                print("Preço ou quantidade inválidos")
                return

            sql = 'INSERT INTO produtos (nome, marca, preco, quantidade) VALUES (%s, %s, %s, %s)'
            produto = Produto(nome_produto, marca_produto, preco_valor, quantidade_valor)

            try:
                self.cursor.execute(sql, (produto.nome, produto.marca, produto.preco, produto.quantidade))
                self.conexao.commit()
                messagebox.showinfo(
                    "Cadastrar Produto - Controle de Estoque",
                    "Produto cadastrado com sucesso!"
                )
                janela.destroy()
            except Exception as erro:
                self.conexao.rollback()
                messagebox.showinfo(
                    "Cadastrar Produto - Controle de Estoque",
                    "Erro ao cadastrar produto!"
                )

        ctk.CTkButton(container, text="Cadastrar", command=salvar).pack(pady=20)

    def vender_produto(self):
        janela = ctk.CTkToplevel(self.app)
        janela.title("Vender produto - Controle de Estoque")
        janela.geometry("400x550")

        container = ctk.CTkFrame(janela)
        container.pack(fill="both", expand=True, padx=25, pady=25)

        ctk.CTkLabel(container, text="Digite o ID do produto").pack(anchor="w", padx=(20, 0), pady=(10, 5))

        id = ctk.CTkEntry(container, width=300)
        id.pack(anchor="w", padx=(20, 0), pady=(10, 10))

        ctk.CTkLabel(container, text="Digite a quantidade do produto").pack(anchor="w", padx=(20, 0), pady=(10, 5))

        quantidade = ctk.CTkEntry(container, width=300)
        quantidade.pack(anchor="w", padx=(20, 0), pady=(10, 10))
        produtos = []

        painel_produtos = ctk.CTkScrollableFrame(container, width=310, height=150)
        painel_produtos.pack(pady=10)

        def adicionar_produto():
            codigo = id.get().strip()
            qtd = quantidade.get().strip()

            if not codigo or not qtd:
                messagebox.showwarning("Atenção","Preencha todos os campos.")
                return
            try:
                codigo_produto = int(codigo)
                quantidade_produto = int(qtd)
            except ValueError:
                messagebox.showwarning("Atenção","ID e quantidade devem ser números.")
                return
            produtos.append((codigo_produto, quantidade_produto))

            card = ctk.CTkFrame(painel_produtos)
            card.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(card, text=f"Produto: {codigo_produto}").pack(side="left", padx=10)
            ctk.CTkLabel(card, text=f"Quantidade: {quantidade_produto}").pack(side="right", padx=10)

            id.delete(0, "end")
            quantidade.delete(0, "end")

        def finalizar():
            if not produtos:
                messagebox.showwarning("Atenção", "Adicione pelo menos um produto.")
                return

            for produto in produtos:
                codigo_produto = produto[0]
                quantidade_produto = produto[1]
                self.cursor.execute(" UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s",(quantidade_produto, codigo_produto))
            self.conexao.commit()
            messagebox.showinfo("Sucesso","Venda finalizada com sucesso!")
            janela.destroy()
        ctk.CTkButton(container, text="Adicionar produto", command=adicionar_produto).pack(pady=10)
        ctk.CTkButton(container, text="Finalizar venda", command=finalizar).pack(pady=5)



    def buscar_produto(self):
        janela = ctk.CTkToplevel(self.app)
        janela.title("Vender produto - Controle de Estoque")
        janela.geometry("400x500")

        container = ctk.CTkFrame(janela)
        container.pack(fill="both", expand=True, padx=25, pady=25)

        ctk.CTkLabel(container, text="Digite o ID do produto à buscar:").pack(anchor="w", padx=(20, 0), pady=(0, 10))
        id_produto = ctk.CTkEntry(container, width=300)
        id_produto.pack(anchor="w", padx=(20, 0), pady=(0, 10))

        ctk.CTkLabel(container, text="Digite o nome do produto à buscar:").pack(anchor="w", padx=(20, 0), pady=(0, 10))
        nome_produto = ctk.CTkEntry(container, width=300)
        nome_produto.pack(anchor="w", padx=(20, 0), pady=(0, 10))

        def buscar():

            id = id_produto.get().strip()
            nome = nome_produto.get().strip()

            if not nome and id:
                self.cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
                resultado = self.cursor.fetchone()

                messagebox.showwarning("Busca de Produtos - Controle de Estoque", f"Nome: {resultado[1]} \nMarca: {resultado[2]} \nPreço: {resultado[3]} \nQuantidade em estoque: {resultado[4]}")
            elif not id and nome:
                self.cursor.execute("SELECT * FROM produtos WHERE nome LIKE %s", (f"%{nome}%",))
                resultado = self.cursor.fetchall()

                card = ctk.CTkToplevel(container)
                card.title("Busca de Produtos - Controle de Estoque")
                card.geometry("300x300")

                for produto in resultado:
                    ctk.CTkLabel(card, text=f"Nome: {produto[1]} \nMarca: {produto[2]} \nPreço: {produto[3]} \nQuantidade em estoque: {produto[4]}").pack()
            elif not id and not nome:
                messagebox.showwarning("Busca de Produtos - Controle de Estoque", "Você deve digitar algo!")

        ctk.CTkButton(container, text="Buscar", command=buscar).pack()

    def listar_produtos(self):
        janela = ctk.CTkToplevel(self.app)
        janela.title("Listagem de produtos - Controle de Estoque")
        janela.geometry("400x500")

        self.cursor.execute("SELECT * FROM produtos")
        resultado = self.cursor.fetchall()

        container = ctk.CTkScrollableFrame(janela, width=350, height=450)
        container.pack(pady=20)

        for produto in resultado:
            ctk.CTkLabel(container, text=f"Nome: {produto[1]} \nMarca: {produto[2]} \nPreço: {produto[3]} \nEstoque: {produto[4]}").pack(pady=5)

    def adicionar_estoque(self):
        janela = ctk.CTkToplevel(self.app)
        janela.title("Adicionar Estoque - Controle de Estoque")
        janela.geometry("350x400")

        ctk.CTkLabel(janela, text="Digite o ID do produto:").pack(pady=10)
        id_produto = ctk.CTkEntry(janela, width=300)
        id_produto.pack(pady=10)

        ctk.CTkLabel(janela, text="Digite a quantidade a ser adicionada:").pack(pady=10)
        quantidade_produto = ctk.CTkEntry(janela, width=300)
        quantidade_produto.pack(pady=10)

        def adicionar():
            id = int(id_produto.get().strip())
            quantidade = int(quantidade_produto.get().strip())

            if not id and not quantidade:
                messagebox.showwarning("Adicionar Estoque - Controle de Estoque", "Preencha todos os campos!")
            elif not id and quantidade:
                messagebox.showwarning("Adicionar Estoque - Controle de Estoque", "Preencha todos os campos!")
            elif not quantidade and id:
                messagebox.showwarning("Adicionar Estoque - Controle de Estoque", "Preencha todos os campos!")
            else:
                self.cursor.execute("UPDATE produtos SET quantidade = quantidade + %s WHERE id = %s", (quantidade, id,))
                self.conexao.commit()
                messagebox.showwarning("Adicionar Estoque - Controle de Estoque", "Estoque adicionado com sucesso!")
                janela.destroy()

        ctk.CTkButton(janela, text="Adicionar estoque", command=adicionar).pack()

    def sair(self):
        self.app.destroy()


sistema = Sistema()