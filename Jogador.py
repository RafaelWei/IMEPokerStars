#vai ser o cliente do socket
from Regras_Poker import *
class Jogador:
    def __init__(self,nome):
        self.nome=nome
        self.mao=[]
        self.mao_objetos=[]
        self.qtdMoedas=500
        self.valor_mao=-1
        self.valor_aposta=0
        self.allin=False
        self.desistiu=False

    def __repr__(self):
        return "("+ str(self.mao)+","+str(self.valor_mao)+")"

    def adicionar_carta(self,carta):
        self.mao.append(carta)

    def checar_melhor_mao(self):
        tupla=jogar(self.mao)
        self.mao = tupla[0]
        self.valor_mao=tupla[1]
        return tupla

    def devolver_cartas(self):
        self.mao=[]
        self.mao_objetos=[]
        self.valor_mao=-1
        self.valor_aposta=0
        self.desistiu=False
        self.allin=False

    #Vamos implementar depois
    def alterar_aposta(self,valor,mesa):
        if valor>=self.qtdMoedas:
            self.allin=True
            self.qtdMoedas=0
        else:
            self.qtdMoedas-=valor
        self.valor_aposta+=valor

    def pronto_para_continuar(self,maior_aposta_mesa):
        return self.valor_aposta==maior_aposta_mesa or self.allin or self.desistiu


