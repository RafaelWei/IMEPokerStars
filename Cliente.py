import socket 
import traceback
import pyfiglet 
from Carta import Carta

mao = []
mesa = []
buf = ""

endFlag = "EOL"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8080
host = 'localhost'
  
result = pyfiglet.figlet_format("Fyre Poker Stars") 
print(result) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


def receiveCard(s, buf, cardSet):
    if buf.find(endFlag) == -1:
        aux = s.recv(64).decode()
        buf += str(aux)
    
    pos = buf.find(endFlag)
    carta = buf[:pos]
    cardSet.append(carta)
    buf = buf[pos+3:]
    return buf

try:
    data = s.recv(22).decode()
    buf += str(data)
    pos = buf.find(endFlag)
    data = buf[:pos]
    buf = buf[pos+3:]
    # print("Received: ", data)
    if data=="Pronto para jogar":
        print("Comecando o jogo.")
        #Aqui começa o jogo
        while True:
            """
            PRE-FLOP
            1)Distribuimos as cartas
            2)Jogadores smallBlind e bigBlind colocam as apostas iniciais na mesa
            3)So podemos passar para a proxima fase quando todas as apostas forem iguais
            """
            buf = receiveCard(s, buf, mao)
            buf = receiveCard(s, buf, mao)

            print("Cartas na mao: ", mao)
            """
            FLOP
            1)Viramos as 3 primeiras cartas na
            2)Recebemos as cartas
            4)So podemos passar para a proxima fase quando todas as apostas forem iguais
            """
            buf = receiveCard(s, buf, mesa)
            buf = receiveCard(s, buf, mesa)
            buf = receiveCard(s, buf, mesa)

            print("Cartas na mao: ", mao)
            print("Cartas na mesa: ", mesa)

            while True:
                if buf.find(endFlag) == -1:
                    aux = s.recv(64).decode()
                    buf += str(aux)
                pos = buf.find(endFlag)
                situacao = buf[:pos]
                buf = buf[pos+3:]
                if situacao=="Escolha a jogada":
                    jogada = input("Escolha qual acao deseja realizar: (digite call, raise ou fold) ")
                    s.send(str.encode(jogada))
                elif situacao=="Jogada invalida":
                    print("Jogada invalida.")
                elif situacao=="raise":
                    n_fichas = input("Para quantas fichas deseja aumentar a aposta: ")
                    s.send(str.encode(n_fichas))
                elif situacao=="wrongRaise":
                    jogada = input("Nao pode colocar menos fichas do que a aposta atual. Para quantas fichas deseja aumentar a aposta: ")
                    s.send(str.encode(jogada))
                elif situacao=="Fim da rodada":
                    break

            if buf.find(endFlag) == -1:
                aux = s.recv(64).decode()
                buf += str(aux)
            pos = buf.find(endFlag)
            perda_da_rodada = buf[:pos]
            buf = buf[pos+3:]
            #get the num
            #num = int(perda_da_rodada)
            print("Perda da rodada:", str(perda_da_rodada))

            """
            TURN
            1)Recebmos mais uma carta que foi virada na mesa
            2)Temos que mandar a aposta desejada
            3)So podemos passar para a proxima fase quando todas as apostas forem iguais
            """

            print(buf)

            buf = receiveCard(s, buf, mesa)
            print("Cartas na mesa: ", mesa)

            while True:
                if buf.find(endFlag) == -1:
                    aux = s.recv(64).decode()
                    print(aux)
                    buf += str(aux)
                pos = buf.find(endFlag)
                situacao = buf[:pos]
                buf = buf[pos+3:]

                if situacao=="Escolha a jogada":
                    jogada = input("Escolha qual acao deseja realizar: (digite bet, call, raise ou fold)")
                    s.send(str.encode(jogada))
                elif situacao=="Jogada invalida":
                    print("Jogada invalida.")
                elif situacao=="raise":
                    n_fichas = input("Para quantas fichas deseja aumentar a aposta: ")
                    s.send(str.encode(n_fichas))
                elif situacao=="wrongRaise":
                    jogada = input("Nao pode colocar menos fichas do que a aposta atual. Para quantas fichas deseja aumentar a aposta: ")
                    s.send(str.encode(jogada))
                elif situacao=="wrongBet":
                    print("Ja existe uma aposta na mesa. Bet nao eh mais valido.")
                elif situacao=="wrongCall":
                    print("Ainda nao ha uma aposta na mesa. Call nao eh valido.")
                elif situacao=="Fim da rodada":
                    break

            if buf.find(endFlag) == -1:
                aux = s.recv(64).decode()
                buf += str(aux)
            pos = buf.find(endFlag)
            perda_da_rodada = buf[:pos]
            buf = buf[pos+3:]
            #get the num
            #num = int(perda_da_rodada)
            print("Perda da rodada:", str(perda_da_rodada))

            """
            RIVER
            1)Recebmos mais uma carta que foi virada na mesa
            2)Temos que mandar a aposta desejada
            3)So podemos passar para a proxima fase quando todas as apostas forem iguais
            """
            buf = receiveCard(s, buf, mesa)
            print("Cartas na mesa: ", mesa)

            while True:
                if buf.find(endFlag) == -1:
                    aux = s.recv(64).decode()
                    print(aux)
                    buf += str(aux)
                pos = buf.find(endFlag)
                situacao = buf[:pos]
                buf = buf[pos+3:]
                if situacao=="Escolha a jogada":
                    jogada = input("Escolha qual acao deseja realizar: (digite bet, call, raise ou fold)")
                    s.send(str.encode(jogada))
                elif situacao=="Jogada invalida":
                    print("Jogada invalida.")
                elif situacao=="raise":
                    n_fichas = input("Para quantas fichas deseja aumentar a aposta: ")
                    s.send(str.encode(n_fichas))
                elif situacao=="wrongRaise":
                    jogada = input("Nao pode colocar menos fichas do que a aposta atual. Para quantas fichas deseja aumentar a aposta: ")
                    s.send(str.encode(jogada))
                elif situacao=="wrongBet":
                    print("Ja existe uma aposta na mesa. Bet nao eh mais valido.")
                elif situacao=="wrongCall":
                    print("Ainda nao ha uma aposta na mesa. Call nao eh valido.")
                elif situacao=="Fim da rodada":
                    break

            if buf.find(endFlag) == -1:
                aux = s.recv(64).decode()
                buf += str(aux)
            pos = buf.find(endFlag)
            perda_da_rodada = buf[:pos]
            buf = buf[pos+3:]
            #get the num
            #num = int(perda_da_rodada)
            print("Perda da rodada:", str(perda_da_rodada))

            """
            SHOWDOWN
            1)Recebemos as cartas dos jogadores que ainda estao no jogo
            2)Recebemos as pontuações do servidor
            """
            if buf.find(endFlag) == -1:
                aux = s.recv(64).decode()
                buf += str(aux)
            pos = buf.find(endFlag)
            vencedor = buf[:pos]
            buf = buf[pos+3:]

            print("Vencedor: ", vencedor)

            break

    # if data=="Desconectando":
        # break
except Exception as e:
    traceback.print_exc()
    print(str(e))
    s.close()

print("Ending connection")
s.close()   