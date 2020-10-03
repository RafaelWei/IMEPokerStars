from Jogador import Jogador
from Baralho import Baralho

def ordenar_jogadores(jogador):
    return  jogador.checar_melhor_mao()[1]

class Mesa:
    def __init__(self,qtdJogadores):
        self.baralho = Baralho()
        self.qtdJogadores=qtdJogadores
        self.jogadores=[]
        self.pot=0
    def distribuir_cartas(self):
        for i in range(0,2):
            for jogador in self.jogadores:
                jogador.adicionar_carta(self.baralho.sacar_carta())

    #temos que dividir em pre flop, flop etc
    def colocar_cartas_mesa(self):
        for i in range(0,5):
            carta_da_vez=self.baralho.sacar_carta()
            for jogador in self.jogadores:
                jogador.adicionar_carta(carta_da_vez)

    def checa_vencedor(self):
        self.jogadores.sort(key=ordenar_jogadores, reverse=True)
        return self.jogadores
        #FALTA IMPLEMENTAR DESEMPATE

    def adicionar_jogador(self,jogador):
        self.jogadores.append(jogador)


