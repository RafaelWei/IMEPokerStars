#vai ser o cliente do socket
from Regras_Poker import *
class Jogador:
    def __init__(self,nome,qtdFichas):
        self.nome=nome
        self.mao=[]
        self.qtdFichas=qtdFichas
        self.valor_mao=-1

    def __repr__(self):
        return "("+ str(self.mao)+","+str(self.valor_mao)+")"

    def adicionar_carta(self,carta):
        self.mao.append(carta)

    def checar_melhor_mao(self):
        tupla=jogar(self.mao)
        self.mao = tupla[0]
        self.valor_mao=tupla[1]
        return tupla

    #Vamos implementar depois
    def check(self):
        pass

    def call(self):
        pass

    def aumentar(self):
        pass

    def allin(self):
        pass



