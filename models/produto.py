# conceito de abstração, porque a classe Produto representa um produto do mundo real dentro do sistema reunindo seus dados e comportamentos em uma única classe e ocultando seus detalhes internos
class Produto:
    def __init__(self, nome, marca, preco, quantidade):
        # conceito de encapsulamento, pois deixamos todos os dados do produto como privados
        self.__nome = nome
        self.__marca = marca
        self.__preco = preco
        self.__quantidade = quantidade

    def get_nome(self):
        return self.__nome
    def get_marca(self):
        return self.__marca
    def get_preco(self):
        return self.__preco
    def get_quantidade(self):
        return self.__quantidade
    def adicionar_estoque(self, quantidade):
        self.__quantidade += quantidade
    def vender(self, quantidade):
        if quantidade > self.__quantidade:
            return False
        self.__quantidade -= quantidade
        return True

    # conceito de poliformismo, o método mostrar() pode ser reescrito por subclasses
    def mostrar(self):
        return (f"Nome: {self.__nome}\n" f"Marca: {self.__marca}\n" f"Preço: R$ {self.__preco:.2f}\n" f"Estoque: {self.__quantidade}")
