#classe de uma carta
class Carta():
    def __init__(self,valor,naipe): #construtor
        self.valor=valor
        self.naipe=naipe
    def __str__(self): #para poder printar uma carta
        return self.valor +self.naipe
    def __repr__(self): #para poder gerar uma string que representa uma carta
        return self.valor +self.naipe
    def __eq__(self, other): #para poder comparar cartas
        return self.valor==other.valor and self.naipe==other.naipe