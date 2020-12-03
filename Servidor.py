import socket
import traceback
import time
import sys

from Baralho import Baralho
from Carta import Carta

baralho = Baralho()
pot = 0
qtd = 0
clientes = []
maos_clientes = [[], [], []]
mesa = []
perdas_da_rodada = [0, 0, 0]
apostas_clientes = [0, 0, 0]
fichas_clientes = [100, 100, 100]
smallBlind = 5
bigBlind = 10
jogadorSmallBlind = 0
jogadorBigBlind = 1
n_jogadores = 3
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

valores=['2','3','4','5','6','7','8','9','10','J','Q','K','A']
naipes=["♥","♦","♠","♣"]
resultados=['Carta alta','Par','Dois pares','Trinca','Sequencia','Flush','Full House','Quadra','Straight Flush','Royal Flush']
cartas_resultados=[[],[],[],[],[],[],[],[],[],[]]

port = 8080
host = 'localhost'

#Registra o a porta do processo ao qual o socket vai fazer a interface
s.bind(('', port))
print("Socket binded to ", port)

#Coloca o socket em estado de listen, esperando requisicoes externas
s.listen(5)
print("Socket listening")

def ordenar_cartas(e):
    return valores.index(e.valor)

def ordenar_grupo_de_cartas(e):
    return valores.index(e[0].valor)

def Par_Trinca_Quadra(cartas):  # funcao para determinar se ha trinca, par ou quadra
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
        resultado.sort(reverse=True, key=ordenar_cartas)
        cartas_resultados[numero_resultado].append(resultado[0])
        return numero_resultado
    # Verificar se ha uma ou mais duplas e uma tripla (Full House)
    if (len(par_trinca_quadra[1]) == 1 and len(par_trinca_quadra[0]) > 0):
        numero_resultado = 6
        for carta_trinca in par_trinca_quadra[1][0]:
            cartas_resultados[numero_resultado].append(carta_trinca)
        par_trinca_quadra[0].sort(reverse=True, key=ordenar_grupo_de_cartas)
        for carta_par in par_trinca_quadra[0][0]:
            cartas_resultados[numero_resultado].append(carta_par)
        return numero_resultado
    # Verificar se ha duas trincas (Full House)
    if (len(par_trinca_quadra[1]) == 2):
        numero_resultado = 6
        par_trinca_quadra[1].sort(reverse=True, key=ordenar_grupo_de_cartas)
        for carta_trinca in par_trinca_quadra[1][0]:
            cartas_resultados[numero_resultado].append(carta_trinca)
        for i in range(0, 2):
            cartas_resultados[numero_resultado].append(par_trinca_quadra[1][1][i])
        return numero_resultado
    # Verificar se ha uma trinca
    if (len(par_trinca_quadra[1]) == 1):
        numero_resultado = 3
        resultado = cartas.copy()
        par_trinca_quadra[1].sort(reverse=True, key=ordenar_grupo_de_cartas)
        for carta_trinca in par_trinca_quadra[1][0]:
            cartas_resultados[numero_resultado].append(carta_trinca)
            resultado.remove(carta_trinca)
        resultado.sort(reverse=True, key=ordenar_cartas)
        for k in range(0, 2):
            cartas_resultados[numero_resultado].append(resultado[k])
            resultado.remove(resultado[k])
        return numero_resultado
    # Verificar se ha dois ou mais pares (nesse caso o resultado vai ser dois pares pois nao existe mao de tres pares)
    if (len(par_trinca_quadra[0]) >= 2):
        numero_resultado = 2
        resultado = cartas.copy()
        par_trinca_quadra[0].sort(reverse=True, key=ordenar_grupo_de_cartas)
        for carta_par in par_trinca_quadra[0][0]:
            cartas_resultados[numero_resultado].append(carta_par)
            resultado.remove(carta_par)
        for carta_par in par_trinca_quadra[0][1]:
            cartas_resultados[numero_resultado].append(carta_par)
            resultado.remove(carta_par)
        resultado.sort(reverse=True, key=ordenar_cartas)
        cartas_resultados[numero_resultado].append(resultado[0])
        return numero_resultado
    # Verificar se ha um par
    if (len(par_trinca_quadra[0]) == 1):
        numero_resultado = 1
        resultado = cartas.copy()
        for carta_par in par_trinca_quadra[0][0]:
            cartas_resultados[numero_resultado].append(carta_par)
            resultado.remove(carta_par)
        resultado.sort(reverse=True, key=ordenar_cartas)
        for k in range(0, 3):
            cartas_resultados[numero_resultado].append(resultado[k])
            resultado.remove(resultado[k])
        return numero_resultado
    # Retorna zero caso nao haja nenhuma das opcoes anteriores
    return 0

# Funcao para verificar se ha Flush, Straight Flush ou Royal Straight Flush
def Flush(cartas):
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
                if sequencia(naipes_flush[i]) == 4:
                    numero_resultado = 8
                    cartas_resultados[numero_resultado] = cartas_resultados[4].copy()
                # verificar se ha apenas flush
                else:
                    numero_resultado = 5
                    naipes_flush[i].sort(reverse=True, key=ordenar_cartas)
                    for j in range(0, 5):
                        cartas_resultados[numero_resultado].append(naipes_flush[i][j])
            return numero_resultado
    # retorna zero se nao houver nenhuma das opcoes anteriores
    return 0

# funcao para verificar se ha frequencia
def sequencia(cartas):
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

def carta_alta(cartas):
        numero_resultado = 0
        resultado = cartas.copy()
        resultado.sort(reverse=True, key=ordenar_cartas)
        for i in range(0, 5):
            cartas_resultados[numero_resultado].append(resultado[i])
        return numero_resultado


while qtd<3:
    conn, addr = s.accept()
    clientes.append(conn)
    qtd+=1
    #conn.send(str.encode("Aguardando demais jogadores"))

for conn in clientes:
    conn.send(str.encode("Pronto para jogarEOL"))

"""
    PRE FLOP
    1)Distribuimos as cartas
    2)Jogadores smallBlind e bigBlind colocam as apostas iniciais na mesa
    3)So podemos passar para a proxima fase quando todas as apostas forem iguais
"""
time.sleep(1)

for i in range(0, 2*n_jogadores):
    conn = clientes[i%n_jogadores]
    carta = baralho.sacar_carta()
    print("Carta sacada: ", carta)
    maos_clientes[i%n_jogadores].append(carta)
    conn.send(str.encode(str(carta) + "EOL"))

time.sleep(1)

print("Passou")
    
"""
    FLOP
    1)Viramos as 3 primeiras cartas na
    2)Adicionamos as cartas nas maos dos clientes tambem(somente no servidor) para facilitar a verificacao das maos posteriormente
    3)Enviamos as cartas para o cliente
    4)Passamos a aposta da rodada como sendo -1 para saber que nao tem nenhuma aposta no inicio
    5)O primeiro jogador agora eh o que fez o smallBlind no inicio
    6)Zeramos o array de perdas da rodada 
    7)Zeramos o array de apostas da rodada somente para os jogadores que nao deram fold em rodadas anteriores. Os que deram tem valor -1 no array
    8)So podemos passar para a proxima fase quando todas as apostas forem iguais
"""

#3 primeiras cartas na mesa
for j in range(0, 3):
    carta = baralho.sacar_carta()
    for i in range(0, n_jogadores):
        conn = clientes[i]
        maos_clientes[i].append(carta)
        conn.send(str.encode(str(carta) + "EOL"))

time.sleep(1)

apostaDaRodada = bigBlind
apostas_clientes[jogadorSmallBlind]=smallBlind
perdas_da_rodada[jogadorBigBlind]=smallBlind
apostas_clientes[jogadorBigBlind]=bigBlind
perdas_da_rodada[jogadorBigBlind]=bigBlind
jogadorDaVez = (jogadorBigBlind+1)%n_jogadores

while True:
    if apostas_clientes[jogadorDaVez]==apostaDaRodada:
        break
    if apostas_clientes[jogadorDaVez]<0:
        jogadorDaVez = (jogadorDaVez+1)%n_jogadores
        continue
    conn = clientes[jogadorDaVez]
    conn.send(str.encode("Escolha a jogadaEOL"))
    jogada = conn.recv(512).decode()
    if jogada=="call":
        apostas_clientes[jogadorDaVez] = apostaDaRodada
        perdas_da_rodada[jogadorDaVez] = apostaDaRodada
        jogadorDaVez = (jogadorDaVez+1)%n_jogadores
        pot+=apostaDaRodada
    elif jogada=="raise":
        conn.send(str.encode("raiseEOL"))
        valorRaise = conn.recv(512)
        while(valorRaise<=apostaDaRodada):
            conn.send(str.encode("wrongRaiseEOL"))
            valorRaise = conn.recv(512).decode()
        apostaDaRodada = valorRaise
        pot+=apostaDaRodada
        perdas_da_rodada[jogadorDaVez] = apostaDaRodada
        jogadorDaVez = (jogadorDaVez+1)%n_jogadores
    elif jogada=="fold":
        apostas_clientes[jogadorDaVez]=-1
        jogadorDaVez = (jogadorDaVez+1)%n_jogadores
    else:
        conn.send(str.encode("Jogada invalidaEOL"))

#Descontando as apostas da rodada
for i in range(0, 3):
    conn = clientes[i]
    conn.send(str.encode("Fim da rodadaEOL"))
    perda = str(perdas_da_rodada[i])
    conn.send(str.encode(perda + "EOL"))


"""
    TURN
    1)Sacamos mais uma carta para ser mostrada na mesa
    2)Adicionamos a carta nas maos dos clientes tambem(somente no servidor) para facilitar a verificacao das maos posteriormente
    3)Enviamos a carta para o cliente
    4)Passamos a aposta da rodada como sendo -1 para saber que nao tem nenhuma aposta no inicio
    5)O primeiro jogador agora eh o que fez o smallBlind no inicio
    6)Zeramos o array de perdas da rodada 
    7)Zeramos o array de apostas da rodada somente para os jogadores que nao deram fold em rodadas anteriores. Os que deram tem valor -1 no array
    8)So podemos passar para a proxima fase quando todas as apostas forem iguais
"""
carta = baralho.sacar_carta()
mesa.append(carta)
for i in range(0, n_jogadores):
    maos_clientes[i].append(carta)

for conn in clientes:
    conn.send(str.encode(str(carta) + "EOL"))

apostaDaRodada = -1
jogadorDaVez = jogadorSmallBlind
for i in range(0,n_jogadores):
    perdas_da_rodada[i] = 0
    if apostas_clientes[i]!=-1:
        apostas_clientes[i]=0

while True:
    if apostas_clientes[jogadorDaVez]==apostaDaRodada:
        break
    if apostas_clientes[jogadorDaVez]<0:
        jogadorDaVez = (jogadorDaVez+1)%n_jogadores
        continue
    conn = clientes[jogadorDaVez]
    conn.send(str.encode("Escolha a jogadaEOL"))
    jogada = conn.recv(512).decode()
    if jogada=="bet":
        if apostaDaRodada==-1:
            apostaDaRodada = bigBlind
            apostas_clientes[jogadorDaVez] = apostaDaRodada
            perdas_da_rodada[jogadorDaVez] = apostaDaRodada
            jogadorDaVez = (jogadorDaVez+1)%n_jogadores
            pot+=apostaDaRodada
        else:
            conn.send(str.encode("wrongBetEOL"))
    elif jogada=="call":
        if apostaDaRodada==-1:
            conn.send(str.encode("wrongCallEOL"))
        else:
            apostas_clientes[jogadorDaVez] = apostaDaRodada
            jogadorDaVez = (jogadorDaVez+1)%n_jogadores
            pot+=apostaDaRodada
            perdas_da_rodada[jogadorDaVez] = apostaDaRodada
    elif jogada=="raise":
        if apostaDaRodada==-1:
            conn.send(str.encode("wrongRaiseEOL"))
        else:
            conn.send(str.encode("raiseEOL"))
            valorRaise = conn.recv(512)
            while(valorRaise<=apostaDaRodada):
                conn.send(str.encode("wrongRaiseEOL"))
                valorRaise = conn.recv(512).decode()
            apostaDaRodada = valorRaise
            pot+=apostaDaRodada
            perdas_da_rodada[jogadorDaVez] = apostaDaRodada
            jogadorDaVez = (jogadorDaVez+1)%n_jogadores
    elif jogada=="fold":
        apostas_clientes[jogadorDaVez]=-1
        jogadorDaVez = (jogadorDaVez+1)%n_jogadores
    else:
        conn.send(str.encode("Jogada invalidaEOL"))

#Descontando as apostas da rodada
for i in range(0, 3):
    conn = clientes[i]
    conn.send(str.encode("Fim da rodadaEOL"))
    perda = str(perdas_da_rodada[i])
    conn.send(str.encode(perda + "EOL"))

"""
    RIVER
    1)Sacamos mais uma carta para ser mostrada na mesa
    2)Adicionamos a carta nas maos dos clientes tambem(somente no servidor) para facilitar a verificacao das maos posteriormente
    3)Enviamos a carta para o cliente
    4)Passamos a aposta da rodada como sendo -1 para saber que nao tem nenhuma aposta no inicio
    5)O primeiro jogador agora eh o que fez o smallBlind no inicio
    6)Zeramos o array de perdas da rodada 
    7)Zeramos o array de apostas da rodada somente para os jogadores que nao deram fold em rodadas anteriores. Os que deram tem valor -1 no array
    8)So podemos passar para a proxima fase quando todas as apostas forem iguais
"""
carta = baralho.sacar_carta()
mesa.append(carta)
for i in range(0, n_jogadores):
    maos_clientes[i].append(carta)

for conn in clientes:
    conn.send(str.encode(str(carta) + "EOL"))

apostaDaRodada = -1
jogadorDaVez = jogadorSmallBlind
for i in range(0,n_jogadores):
    perdas_da_rodada[i] = 0
    if apostas_clientes[i]!=-1:
        apostas_clientes[i]=0

print(maos_clientes)

while True:
    if apostas_clientes[jogadorDaVez]==apostaDaRodada:
        break
    if apostas_clientes[jogadorDaVez]<0:
        jogadorDaVez = (jogadorDaVez+1)%n_jogadores
        continue
    conn = clientes[jogadorDaVez]
    conn.send(str.encode("Escolha a jogadaEOL"))
    jogada = conn.recv(512).decode()
    if jogada=="bet":
        if apostaDaRodada==-1:
            apostaDaRodada = bigBlind
            apostas_clientes[jogadorDaVez] = apostaDaRodada
            jogadorDaVez = (jogadorDaVez+1)%n_jogadores
            pot+=apostaDaRodada
            perdas_da_rodada[jogadorDaVez] = apostaDaRodada
        else:
            conn.send(str.encode("wrongBetEOL"))
    elif jogada=="call":
        if apostaDaRodada==-1:
            conn.send(str.encode("wrongCallEOL"))
        else:
            apostas_clientes[jogadorDaVez] = apostaDaRodada
            jogadorDaVez = (jogadorDaVez+1)%n_jogadores
            pot+=apostaDaRodada
            perdas_da_rodada[jogadorDaVez] = apostaDaRodada
    elif jogada=="raise":
        if apostaDaRodada==-1:
            conn.send(str.encode("wrongRaiseEOL"))
        else:
            conn.send(str.encode("raiseEOL"))
            valorRaise = conn.recv(512)
            while(valorRaise<=apostaDaRodada):
                conn.send(str.encode("wrongRaiseEOL"))
                valorRaise = conn.recv(512).decode()
            apostaDaRodada = valorRaise
            pot+=apostaDaRodada
            perdas_da_rodada[jogadorDaVez] = apostaDaRodada
            jogadorDaVez = (jogadorDaVez+1)%n_jogadores
    elif jogada=="fold":
        apostas_clientes[jogadorDaVez]=-1
        jogadorDaVez = (jogadorDaVez+1)%n_jogadores
    else:
        conn.send(str.encode("Jogada invalidaEOL"))

#Descontando as apostas da rodada
for i in range(0, 3):
    conn = clientes[i]
    conn.send(str.encode("Fim da rodadaEOL"))
    perda = str(perdas_da_rodada[i])
    conn.send(str.encode(perda + "EOL"))

"""
    SHOWDOWN
    1)Calculamos qual eh a melhor mao
    2)Damos o valor do pot para o jogador com a melhor mao
    3)Checa se algum jogador foi eliminado(dinheiro zerado)
    4)Retira os jogadores eliminados
    5)Reinicia todos os valores para que a proxima rodada possa comecar)
"""
vencedor = -1
maximo = -1
for i in range(0, len(maos_clientes)):
    aux = max(Par_Trinca_Quadra(maos_clientes[i]), Flush(maos_clientes[i]), sequencia(maos_clientes[i]), carta_alta(maos_clientes[i]))
    if(aux>maximo):
        maximo=aux
        vencedor = i

for i in range(0,len(clientes)):
    conn = clientes[i]
    conn.send(str.encode(str(vencedor)+"EOL"))

print(maos_clientes)

