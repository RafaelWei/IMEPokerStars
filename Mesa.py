from Baralho import Baralho
valores=['2','3','4','5','6','7','8','9','10','J','Q','K','A']
naipes=["C","O","E","P"]
def ordenar_jogadores(jogador):
    return jogador.valor_mao

class Mesa:
    def __init__(self):
        self.baralho = Baralho()
        self.jogadores=[]
        self.jogadores_validos=[]
        self.pot=0
        self.cartas_mesa=[]
        self.cartas_mesa_objeto=[]
        self.maior_aposta=0
        self.dealer=0
        self.aposta_big=40

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
            self.cartas_mesa.append(carta_da_vez)

    def definir_blinds(self):
        if len(self.jogadores)==2:
            self.small_blind=self.dealer
            self.big_blind=(self.dealer+1)%2
        else:
            self.small_blind=(self.dealer+1)%len(self.jogadores)
            self.big_blind=(self.dealer+2)%len(self.jogadores)
        self.jogadores[self.small_blind].alterar_aposta(self.aposta_big // 2, self)
        self.jogadores[self.big_blind].alterar_aposta(self.aposta_big,self)


    def checa_vencedor(self):
        for jogador in self.jogadores_validos:
            jogador.checar_melhor_mao()
        self.jogadores_validos.sort(key=ordenar_jogadores, reverse=True)
        resultado=(self.jogadores_validos[0]).valor_mao
        empatados=[]
        for jogador in self.jogadores_validos:
            if jogador.valor_mao==resultado:
                empatados.append(jogador)
            else:
                break
        if(len(empatados)>1):
            vencedor=self.desempatar(empatados)
        else:
            vencedor=empatados[0]
        return vencedor

    def adicionar_jogador(self,jogador):
        self.jogadores.append(jogador)
        self.jogadores_validos.append(jogador)

    def desempatar(self,empatados):
        for i in range (0,5):
            valores_desempate=[]
            for jogador in empatados:
                valores_desempate.append(valores.index(jogador.mao[i].valor))
            maximo=max(valores_desempate)
            for jogador in empatados:
                if valores.index(jogador.mao[i].valor)!=maximo:
                    empatados.remove(jogador)
            if len(empatados)==1:
                return empatados[0]
        return empatados

    def nova_rodada(self):
        self.baralho=Baralho()
        self.pot=0
        self.cartas_mesa = []
        self.cartas_mesa_objeto = []
        self.maior_aposta=0
        self.jogadores_validos=self.jogadores.copy()
        self.dealer+=1
        if self.dealer==len(self.jogadores):
            self.dealer=0

