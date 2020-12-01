import socket
import traceback
import time
import sys

from Baralho import Baralho

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
print("Socket successfully created!")

port = 8080
host = 'localhost'

#Registra o a porta do processo ao qual o socket vai fazer a interface
s.bind(('', port))
print("Socket binded to ", port)

#Coloca o socket em estado de listen, esperando requisicoes externas
s.listen(5)
print("Socket listening")

def acceptClients(s):
    global clientes, qtd
    while True:
        conn, addr = s.accept()
        clientes.append(conn)
        qtd+=1
        #conn.send(str.encode("Aguardando demais jogadores"))
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

print(maos_clientes)
