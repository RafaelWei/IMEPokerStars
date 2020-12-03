import socket
import traceback
import time
import sys
import pickle

from Mesa import Mesa
from Baralho import Baralho
from Jogador import Jogador
from GameState import GameState

mesa = Mesa()
baralho = Baralho()
pot = 0
qtd = 0
clientes = []
# maos_clientes = [[], [], []]
# perdas_da_rodada = [0, 0, 0]
# apostas_clientes = [0, 0, 0]
# fichas_clientes = [100, 100, 100]
# smallBlind = 5
# bigBlind = 10
# jogadorSmallBlind = 0
# jogadorBigBlind = 1
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

while qtd<3:
    conn, addr = s.accept()
    clientes.append(conn)
    name = conn.recv(32).decode()
    print("nome: ", name)
    mesa.adicionar_jogador(name)
    qtd+=1

for conn in clientes:
    conn.send(str.encode("Pronto para jogarEOL"))

"""
    PRE FLOP
    1)Distribuimos as cartas
    2)Jogadores smallBlind e bigBlind colocam as apostas iniciais na mesa
    3)So podemos passar para a proxima fase quando todas as apostas forem iguais
"""
mesa.distribuir_cartas()

time.sleep(2)

while True:
    #Checa se todas as apostas são iguais. Se não forem reenvio 
    if(mesa.fimTurno):
        break

    for i in range(0, n_jogadores):
        conn = clientes[i]
        currGameState = pickle.dumps(mesa.gameState)
        conn.send(currGameState)

    jogada = conn.recv(32).decode()
    if jogada == "check":
        mesa.gameState.jogadorDaVez += 1
    elif jogada=="call":
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].alterar_aposta((mesa.gameState.maior_aposta - mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].valor_aposta), mesa.gameState.maior_aposta)
        mesa.gameState.jogadorDaVez += 1
    elif jogada=="fold":
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].desistiu=True
        for i in range(0, len(mesa.gameState.jogadores_validos)):
            if( mesa.gameState.jogadores[mesa.gameState.jogadorDaVez] == mesa.gameState.jogadores_validos[i]):
                mesa.gameState.jogadores_validos.remove(mesa.gameState.jogadores_validos[i])
                break
    else:
        # o else vai tratar o caso em que acontece um raise
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].alterar_aposta(int(jogada), mesa.gameState.maior_aposta)


time.sleep(2)
    
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
mesa.colocar_cartas_mesa()

for i in range(0, n_jogadores):
    conn = clientes[i]
    currGameState = pickle.dumps(mesa.gameState)
    conn.send(currGameState)

time.sleep(1)

while True:
    #Checa se todas as apostas são iguais. Se não forem reenvio 
    if(mesa.fimTurno):
        break

    for i in range(0, n_jogadores):
        conn = clientes[i]
        currGameState = pickle.dumps(mesa.gameState)
        conn.send(currGameState)

    jogada = conn.recv(32).decode()
    if jogada == "check":
        mesa.gameState.jogadorDaVez += 1
    elif jogada=="call":
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].alterar_aposta((mesa.gameState.maior_aposta - mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].valor_aposta), mesa.gameState.maior_aposta)
        mesa.gameState.jogadorDaVez += 1
    elif jogada=="fold":
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].desistiu=True
        for i in range(0, len(mesa.gameState.jogadores_validos)):
            if( mesa.gameState.jogadores[mesa.gameState.jogadorDaVez] == mesa.gameState.jogadores_validos[i]):
                mesa.gameState.jogadores_validos.remove(mesa.gameState.jogadores_validos[i])
                break
    else:
        # o else vai tratar o caso em que acontece um raise
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].alterar_aposta(int(jogada), mesa.gameState.maior_aposta)

#Transição entre turnos. Tem que atualizar o gameState
mesa.prepareForNextPhase()

time.sleep(2)

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

mesa.adicionar_carta_mesa()

for i in range(0, n_jogadores):
    conn = clientes[i%n_jogadores]
    currGameState = pickle.dumps(mesa.gameState)
    conn.send(currGameState)

while True:
    #Checa se todas as apostas são iguais. Se não forem reenvio 
    if(mesa.fimTurno):
        break

    for i in range(0, n_jogadores):
        conn = clientes[i]
        currGameState = pickle.dumps(mesa.gameState)
        conn.send(currGameState)

    jogada = conn.recv(32).decode()
    if jogada == "check":
        mesa.gameState.jogadorDaVez += 1
    elif jogada=="call":
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].alterar_aposta((mesa.gameState.maior_aposta - mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].valor_aposta), mesa.gameState.maior_aposta)
        mesa.gameState.jogadorDaVez += 1
    elif jogada=="fold":
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].desistiu=True
        for i in range(0, len(mesa.gameState.jogadores_validos)):
            if( mesa.gameState.jogadores[mesa.gameState.jogadorDaVez] == mesa.gameState.jogadores_validos[i]):
                mesa.gameState.jogadores_validos.remove(mesa.gameState.jogadores_validos[i])
                break
    else:
        # o else vai tratar o caso em que acontece um raise
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].alterar_aposta(int(jogada), mesa.gameState.maior_aposta)

#Transição entre turnos. Tem que atualizar o gameState
mesa.prepareForNextPhase()
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

mesa.adicionar_carta_mesa()
# carta = baralho.sacar_carta()
# mesa.append(carta)

for i in range(0, n_jogadores):
    conn = clientes[i%n_jogadores]
    currGameState = pickle.dumps(mesa.gameState)
    conn.send(currGameState)

while True:
    #Checa se todas as apostas são iguais. Se não forem reenvio 
    if(mesa.fimTurno):
        break

    for i in range(0, n_jogadores):
        conn = clientes[i]
        currGameState = pickle.dumps(mesa.gameState)
        conn.send(currGameState)

    jogada = conn.recv(32).decode()
    if jogada == "check":
        mesa.gameState.jogadorDaVez += 1
    elif jogada=="call":
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].alterar_aposta((mesa.gameState.maior_aposta - mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].valor_aposta), mesa.gameState.maior_aposta)
        mesa.gameState.jogadorDaVez += 1
    elif jogada=="fold":
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].desistiu=True
        for i in range(0, len(mesa.gameState.jogadores_validos)):
            if( mesa.gameState.jogadores[mesa.gameState.jogadorDaVez] == mesa.gameState.jogadores_validos[i]):
                mesa.gameState.jogadores_validos.remove(mesa.gameState.jogadores_validos[i])
                break
    else:
        # o else vai tratar o caso em que acontece um raise
        mesa.gameState.jogadores[mesa.gameState.jogadorDaVez].alterar_aposta(int(jogada), mesa.gameState.maior_aposta)

"""
    SHOWDOWN
    1)Calculamos qual eh a melhor mao
    2)Damos o valor do pot para o jogador com a melhor mao
    3)Checa se algum jogador foi eliminado(dinheiro zerado)
    4)Retira os jogadores eliminados
    5)Reinicia todos os valores para que a proxima rodada possa comecar)
"""

# mesa.prepareForNextRound()
# print(maos_clientes)