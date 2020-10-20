from Carta import Carta
valores=['2','3','4','5','6','7','8','9','10','J','Q','K','A']
naipes=["♥","♦","♠","♣"]
resultados=['Carta alta','Par','Dois pares','Trinca','Sequencia','Flush','Full House','Quadra','Straight Flush','Royal Flush']
cartas_resultados=[[],[],[],[],[],[],[],[],[],[]]
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
        tupla=self.jogar(self.mao)
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

    ####################################################
    #####FUNCOES USADAS PARA ENCONTRAR A MELHOR MAO#####
    ####################################################

    def Par_Trinca_Quadra(self,cartas):  # funcao para determinar se ha trinca, par ou quadra
        par_trinca_quadra = [[], [],[]]  # lista para armazenar os pares(posicao 0), as tricas(posicao 1) e as quadras(posicao 2)
        valores_jogo = [[], [], [], [], [], [], [], [], [], [], [], [],[]]  # lista que vai separar as cartas por valores (posicao 0 para cartas 'A', posicao 1 para cartas '2' e assim por diante)
        for i in cartas:
            valores_jogo[valores.index(i.valor)].append(i)  # separar as cartas por valores
        # alocar as tricas, quadras e pares
        for n in range(0, 3):
            for m in range(0, 13):
                if (len(valores_jogo[m]) == n + 2):
                    jogo = []
                    for i in valores_jogo[m]:
                        jogo.append(i)
                    par_trinca_quadra[n].append(jogo)
        # Verificar se ha quadra
        if (len(par_trinca_quadra[2]) > 0):
            numero_resultado = 7
            resultado = cartas.copy()
            for carta_quadra in par_trinca_quadra[2][0]:
                cartas_resultados[numero_resultado].append(carta_quadra)
                resultado.remove(carta_quadra)
            resultado.sort(reverse=True, key=self.ordenar_cartas)
            cartas_resultados[numero_resultado].append(resultado[0])
            return numero_resultado
        # Verificar se ha uma ou mais duplas e uma tripla (Full House)
        if (len(par_trinca_quadra[1]) == 1 and len(par_trinca_quadra[0]) > 0):
            numero_resultado = 6
            for carta_trinca in par_trinca_quadra[1][0]:
                cartas_resultados[numero_resultado].append(carta_trinca)
            par_trinca_quadra[0].sort(reverse=True, key=self.ordenar_grupo_de_cartas)
            for carta_par in par_trinca_quadra[0][0]:
                cartas_resultados[numero_resultado].append(carta_par)
            return numero_resultado
        # Verificar se ha duas trincas (Full House)
        if (len(par_trinca_quadra[1]) == 2):
            numero_resultado = 6
            par_trinca_quadra[1].sort(reverse=True, key=self.ordenar_grupo_de_cartas)
            for carta_trinca in par_trinca_quadra[1][0]:
                cartas_resultados[numero_resultado].append(carta_trinca)
            for i in range(0, 2):
                cartas_resultados[numero_resultado].append(par_trinca_quadra[1][1][i])
            return numero_resultado
        # Verificar se ha uma trinca
        if (len(par_trinca_quadra[1]) == 1):
            numero_resultado = 3
            resultado = cartas.copy()
            par_trinca_quadra[1].sort(reverse=True, key=self.ordenar_grupo_de_cartas)
            for carta_trinca in par_trinca_quadra[1][0]:
                cartas_resultados[numero_resultado].append(carta_trinca)
                resultado.remove(carta_trinca)
            resultado.sort(reverse=True, key=self.ordenar_cartas)
            for k in range(0, 2):
                cartas_resultados[numero_resultado].append(resultado[k])
                resultado.remove(resultado[k])
            return numero_resultado
        # Verificar se ha dois ou mais pares (nesse caso o resultado vai ser dois pares pois nao existe mao de tres pares)
        if (len(par_trinca_quadra[0]) >= 2):
            numero_resultado = 2
            resultado = cartas.copy()
            par_trinca_quadra[0].sort(reverse=True, key=self.ordenar_grupo_de_cartas)
            for carta_par in par_trinca_quadra[0][0]:
                cartas_resultados[numero_resultado].append(carta_par)
                resultado.remove(carta_par)
            for carta_par in par_trinca_quadra[0][1]:
                cartas_resultados[numero_resultado].append(carta_par)
                resultado.remove(carta_par)
            resultado.sort(reverse=True, key=self.ordenar_cartas)
            cartas_resultados[numero_resultado].append(resultado[0])
            return numero_resultado
        # Verificar se ha um par
        if (len(par_trinca_quadra[0]) == 1):
            numero_resultado = 1
            resultado = cartas.copy()
            for carta_par in par_trinca_quadra[0][0]:
                cartas_resultados[numero_resultado].append(carta_par)
                resultado.remove(carta_par)
            resultado.sort(reverse=True, key=self.ordenar_cartas)
            for k in range(0, 3):
                cartas_resultados[numero_resultado].append(resultado[k])
                resultado.remove(resultado[k])
            return numero_resultado
        # Retorna zero caso nao haja nenhuma das opcoes anteriores
        return 0

    # Funcao para verificar se ha Flush, Straight Flush ou Royal Straight Flush
    def Flush(self,cartas):
        naipes_flush = [[], [], [], []]  # separar por naipes
        for i in cartas:
            naipes_flush[naipes.index(i.naipe)].append(i)
        for i in range(0, 4):
            if len(naipes_flush[i]) >= 5:
                # verifica se ha royal flush
                royal = 0
                cartas_royal = [Carta(valores[12], naipes[i]), Carta(valores[11], naipes[i]),
                                Carta(valores[10], naipes[i]), \
                                Carta(valores[9], naipes[i]), Carta(valores[8], naipes[i])]
                for carta in cartas_royal:
                    for carta_baralho in naipes_flush[i]:
                        if carta == carta_baralho:
                            royal += 1
                            continue
                if royal == 5:
                    numero_resultado = 9
                    cartas_resultados[numero_resultado] = cartas_royal.copy()
                else:
                    # verificar se ha stright flush
                    if self.sequencia(naipes_flush[i]) == 4:
                        numero_resultado = 8
                        cartas_resultados[numero_resultado] = cartas_resultados[4].copy()
                    # verificar se ha apenas flush
                    else:
                        numero_resultado = 5
                        naipes_flush[i].sort(reverse=True, key=self.ordenar_cartas)
                        for j in range(0, 5):
                            cartas_resultados[numero_resultado].append(naipes_flush[i][j])
                return numero_resultado
        # retorna zero se nao houver nenhuma das opcoes anteriores
        return 0

    # funcao para verificar se ha frequencia
    def sequencia(self,cartas):
        valores_jogo = [[], [], [], [], [], [], [], [], [], [], [], [], [],
                        []]  # divide o baralho por valores, lembrando que o 'A' pode ficar na primeira ou na ultima opcao na sequencia
        sequencia_corrente = 0
        for i in cartas:
            valores_jogo[(valores.index(i.valor)) + 1].append(i)
            if (valores.index(i.valor) == 12):  # se for 'A' adicionar na primeira e na ultima opcao
                valores_jogo[0].append(i)
        for i in range(13, -1, -1):
            if len(valores_jogo[i]) >= 1:
                sequencia_corrente += 1
            if len(valores_jogo[i]) == 0:
                sequencia_corrente = 0
            if sequencia_corrente == 5:
                numero_resultado = 4
                for j in range(i, i + 5):
                    cartas_resultados[numero_resultado].append(valores_jogo[j][0])
                return numero_resultado
        return 0

    # funcao que ordena duas cartas por valor
    def ordenar_cartas(self,e):
        return valores.index(e.valor)

    # funcao que ordena dois grupos de cartas do mesmo valor(Ex: (Carta(J,Copas),Carta(J,Ouros))>)(Carta(5,Paus),Carta(5,Ouros)))
    def ordenar_grupo_de_cartas(self,e):
        return valores.index(e[0].valor)

    # funcao que gera a mao de uma carta alta
    def carta_alta(self,cartas):
        numero_resultado = 0
        resultado = cartas.copy()
        resultado.sort(reverse=True, key=self.ordenar_cartas)
        for i in range(0, 5):
            cartas_resultados[numero_resultado].append(resultado[i])
        return numero_resultado

    # funcao que aponta o resultado de um conjunto de cartas
    def jogar(self,cartas):
        jogo = max(self.Par_Trinca_Quadra(cartas), self.Flush(cartas), self.sequencia(cartas), self.carta_alta(cartas))
        aux1 = cartas_resultados[jogo].copy()
        aux2 = resultados.index(resultados[jogo])
        for lista in cartas_resultados:
            lista.clear()
        return (aux1, aux2)