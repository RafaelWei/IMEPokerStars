from Poker import *
class Jogador:
    def __init__(self,nome,qtdFichas):
        self.nome=nome
        self.mao=[]
        self.qtdFichas=qtdFichas

    def __repr__(self):
        return "("+ str(self.checar_melhor_mao()[0])+","+str(self.checar_melhor_mao()[1])+")"

    def adicionar_carta(self,carta):
        self.mao.append(carta)

    def checar_melhor_mao(self):
        tupla=jogar(self.mao)
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

