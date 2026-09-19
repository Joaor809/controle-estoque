import customtkinter as ctk
from tkinter import messagebox
from banco import conn
from models.produto import Produto
from components.button import Button
from components.input import Input
from components.window import Window, SecondaryWindow

class Sistema:
    def __init__(self):
        self.conexao = conn()
        self.cursor = self.conexao.cursor()
        self.app = Window("Controle de Estoque", 400, 450)
        self.menu()
        self.app.mainloop()

    def menu(self):
        Button(self.app, "Cadastrar Produto", self.cadastrar).pack(pady=10)
        Button(self.app, "Vender Produto", self.vender).pack(pady=10)
        Button(self.app, "Buscar Produto", self.buscar).pack(pady=10)
        Button(self.app, "Listar Produtos", self.listar).pack(pady=10)
        Button(self.app, "Adicionar Estoque", self.adicionar_estoque).pack(pady=10)
        Button(self.app, "Sair", self.sair).pack(pady=10)

    def cadastrar(self):
        window = SecondaryWindow(self.app, "Cadastrar Produto", 400, 400)
        nome = Input(window, "Nome")
        nome.pack(pady=10)

        marca = Input(window, "Marca")
        marca.pack(pady=10)

        preco = Input(window, "Preço")
        preco.pack(pady=10)

        quantidade = Input(window, "Quantidade")
        quantidade.pack(pady=10)

        def salvar():
            try:
                produto = Produto(nome.get().strip(), marca.get().strip(), float(preco.get().replace(",", ".")), int(quantidade.get()))
                sql = """
                    INSERT INTO produtos
                    (nome, marca, preco, quantidade)
                    VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(sql, (produto.get_nome(), produto.get_marca(), produto.get_preco(), produto.get_quantidade()))
                self.conexao.commit()
                messagebox.showinfo("Sucesso", "Produto cadastrado!")
                window.destroy()
            except ValueError:
                messagebox.showwarning("Erro", "Digite valores válidos.")

        Button(window, "Cadastrar", salvar).pack(pady=20)

    def vender(self):
        window = SecondaryWindow(self.app, "Vender Produto", 400, 300)
        id_produto = Input(window, "ID do produto")
        id_produto.pack(pady=10)
        quantidade = Input(window, "Quantidade")
        quantidade.pack(pady=10)

        def realizar_venda():
            try:
                codigo = int(id_produto.get())
                qtd = int(quantidade.get())
                self.cursor.execute("SELECT quantidade FROM produtos WHERE id = %s", (codigo,))
                resultado = self.cursor.fetchone()

                if resultado is None:
                    messagebox.showwarning("Erro", "Produto não encontrado.")
                    return

                estoque = resultado[0]

                if qtd > estoque:
                    messagebox.showwarning("Erro", "Estoque insuficiente.")
                    return

                self.cursor.execute("UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s", (qtd, codigo))
                self.conexao.commit()
                messagebox.showinfo("Sucesso", "Venda realizada!")
                window.destroy()
            except ValueError:
                messagebox.showwarning("Erro", "Digite números válidos.")

        Button(window, "Vender", realizar_venda).pack(pady=20)

    def buscar(self):
        window = SecondaryWindow(self.app, "Buscar Produto", 400, 300)
        nome = Input(window, "Nome do produto")
        nome.pack(pady=10)

        def pesquisar():
            self.cursor.execute("SELECT * FROM produtos WHERE nome LIKE %s", (f"%{nome.get()}%",))
            produtos = self.cursor.fetchall()

            if not produtos:
                messagebox.showinfo("Busca", "Nenhum produto encontrado.")
                return

            resultado = SecondaryWindow(self.app, "Resultados", 400, 400)
            frame = ctk.CTkScrollableFrame(resultado)
            frame.pack(fill="both", expand=True, padx=20, pady=20)

            for dados in produtos:
                produto = Produto(dados[1], dados[2], dados[3], dados[4])
                ctk.CTkLabel(frame, text=produto.mostrar() + "\n\nProduto pesquisado").pack(pady=10)

        Button(window, "Buscar", pesquisar).pack(pady=20)

    def listar(self):
        window = SecondaryWindow(self.app, "Produtos", 400, 500)
        frame = ctk.CTkScrollableFrame(window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.cursor.execute("SELECT * FROM produtos")
        produtos = self.cursor.fetchall()

        for dados in produtos:
            produto = Produto(dados[1], dados[2], dados[3], dados[4])
            ctk.CTkLabel(frame, text=produto.mostrar()).pack(pady=10)

    def adicionar_estoque(self):
        window = SecondaryWindow(self.app, "Adicionar Estoque", 400, 300)
        id_produto = Input(window, "ID do produto")
        id_produto.pack(pady=10)
        quantidade = Input(window, "Quantidade")
        quantidade.pack(pady=10)

        def adicionar():
            try:
                codigo = int(id_produto.get())
                qtd = int(quantidade.get())
                self.cursor.execute("UPDATE produtos SET quantidade = quantidade + %s WHERE id = %s", (qtd, codigo))

                if self.cursor.rowcount == 0:
                    messagebox.showwarning("Erro", "Produto não encontrado.")
                    return

                self.conexao.commit()
                messagebox.showinfo("Sucesso", "Estoque atualizado!")
                window.destroy()
            except ValueError:
                messagebox.showwarning("Erro", "Digite números válidos.")

        Button(window, "Adicionar", adicionar).pack(pady=20)

    def sair(self):
        self.cursor.close()
        self.conexao.close()
        self.app.destroy()

Sistema()