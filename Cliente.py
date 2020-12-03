import pygame
import socket 
import traceback
import sys
import pickle

from Carta import Carta
from Botao import Botao
from GameState import GameState
from Jogador import Jogador

pygame.init()
pygame.font.init()
comprimento=800
altura=400
tela=pygame.display.set_mode((comprimento,altura))
pygame.display.set_caption("IME PokerStars")
fonte = pygame.font.SysFont("comicsans", 60)
fonte_grande = pygame.font.SysFont("comicsans", 80)
fonte_pequena = pygame.font.SysFont("comicsans", 40)
fonte_muito_pequena = pygame.font.SysFont("comicsans", 30)
pos=[[50,-100],[150,-100],[250,-100],[350,-100],[450,-100]]
check=Botao("check",400,350,(119, 107, 181),30,80,40)
fold=Botao("fold",400,295,(119, 107, 181),30,80,40)
call=Botao("call",500,350,(119, 107, 181),30,80,40)
bet=Botao("bet",500,295,(119, 107, 181),30,80,40)
raise_botao=Botao("raise",500,295,(119, 107, 181),30,80,40)
prosseguir=Botao("Prosseguir",220,250,(119,107,181),20,110,20)
prox_rodada=Botao("Proxima rodada",650,350,(119,107,181),20,110,20)
voltar=Botao("Voltar",220,280,(119,107,181),20,110,20)
moeda_objeto=(pygame.image.load(f"./PokerStarsIME_imgs/Coin.png"))
moeda_objeto=(pygame.transform.scale(moeda_objeto,(51,75)))
dealer_objeto=(pygame.image.load(f'./PokerStarsIME_imgs/dealer.png'))
dealer_objeto=(pygame.transform.scale(dealer_objeto,(36,30)))
resultados=['Carta alta','Par','Dois pares','Trinca','Sequencia','Flush','Full House','Quadra','Straight Flush','Royal Flush']

mao = []
mesa = []
buf = ""
nome = ""
myPlayer = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

endFlag = "EOL"
port = 8080
host = 'localhost'

#Maior aposta, pot, dealer e os jogadores
def redesenhar_tela(texto_nome,texto_fichas,cartas_visiveis,jogador,mesa):
    tela.fill((35,125,90))
    if jogador.valor_aposta==mesa.maior_aposta:
        check.desenhar(tela)
        bet.desenhar(tela)
    fold.desenhar(tela)
    if mesa.maior_aposta > jogador.valor_aposta:
        raise_botao.desenhar(tela)
        call.desenhar(tela)
    tela.blit(texto_nome,(20,280))
    tela.blit(texto_fichas, (80, 375))
    tela.blit(moeda_objeto,(20,315))
    mesa_texto=fonte.render('Mesa:',1,(4,5,133))
    tela.blit(mesa_texto,(5,5))
    pote=fonte.render(str(mesa.pot), 1, (4, 15, 133))
    tela.blit(pote,(135,8))
    c=5
    delta=50
    # tela.blit(dealer_objeto, (590, (c+delta*(mesa.dealer))))
    for player in mesa.jogadores:
        if player.desistiu==False:
            nome_aposta=fonte_muito_pequena.render(player.nome,1,(0,0,0))
            aposta = fonte_muito_pequena.render(str(player.valor_aposta), 1, (0, 0, 0))
        else:
            nome_aposta = fonte_muito_pequena.render(player.nome, 1, (192, 192, 204))
            aposta = fonte_muito_pequena.render(str(player.valor_aposta), 1, (192, 192, 204))
        tela.blit(nome_aposta,(620,c))
        tela.blit(aposta,(620,c+5*delta//12))
        c+=delta
    a=200
    b=300
    d=100
    for carta in cartas_visiveis:
        tela.blit(carta,(d,100))
        d+=100
    for carta in jogador.mao_objetos:
        tela.blit(carta,(a,b))
        a+=100
    pygame.display.update()

def menu(tipo,njogadores=3):
    run=True
    global nome
    global buf
    global endFlag
    global port
    global host
    clock = pygame.time.Clock()
    texto_usuario = ""
    retangulo =pygame.Rect(220,200,300,32)
    cor_retangulo=(255,255,255)
    while(run):
        clock.tick(20)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posicao = pygame.mouse.get_pos()
                if tipo != 0:
                    if prosseguir.clicar(posicao):
                        run=False
                    if voltar.clicar(posicao):
                        if tipo == 1:
                            return 'voltou'
                if tipo==0:
                    if prosseguir.clicar(posicao):
                        s.connect((host, port))
                        nome = texto_usuario
                        print("PASSANDO O SOCKET")
                        try:
                            s.send(str.encode(nome))
                            data = s.recv(22).decode()
                            buf += str(data)
                            pos = buf.find(endFlag)
                            data = buf[:pos]
                            buf = buf[pos+3:]
                            if data=="Pronto para jogar":
                                run=False
                        except Exception as e:
                            traceback.print_exc()
                            print(str(e))
                            s.close()    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    texto_usuario=texto_usuario[0:-1]
                else:
                    if len(texto_usuario)<=10 and event.key != pygame.K_RETURN:
                        texto_usuario += event.unicode
        tela.fill((35,125,90))
        pygame.draw.rect(tela,cor_retangulo,retangulo)
        if tipo==0:
            texto_titulo = fonte_grande.render("Digite o seu nome:", 1, (4, 15, 133))
            tela.blit(texto_titulo, (125, 50))
            texto = fonte_pequena.render(texto_usuario, 1, (4, 15, 133))
            tela.blit(texto, (retangulo.x + 5, retangulo.y + 5))
            prosseguir.desenhar(tela)
            pygame.display.update()

        if tipo==1:
            texto_titulo = fonte.render("Digite o valor que deseja apostar:", 1, (4, 15, 133))
            tela.blit(texto_titulo, (80, 80))
            voltar.desenhar(tela)
            texto = fonte_pequena.render(texto_usuario, 1, (4, 15, 133))
            tela.blit(texto, (retangulo.x + 5, retangulo.y + 5))
            prosseguir.desenhar(tela)
            pygame.display.update()

    if tipo==0:
        main(clock)
    if tipo==1:
        if texto_usuario.isnumeric():
            return texto_usuario
        else:
            pygame.time.delay(2000)
            menu(1)

def main(clock):
    """
    PRE-FLOP
    1)Distribuimos as cartas
    2)Jogadores smallBlind e bigBlind colocam as apostas iniciais na mesa
    3)So podemos passar para a proxima fase quando todas as apostas forem iguais
    """
    #Aqui a gente ta recebendo o jogador inteiro!!!
    
    # msg = s.recv(1024)
    # player = pickle.loads(msg)
    
    while True:
        msg = s.recv(4096)
        currGameState = pickle.loads(msg)
        for jogador in currGameState.jogadores:
            if(jogador.nome==nome):
                myPlayer = jogador
        texto_nome = fonte_pequena.render(nome, 1, (4, 15, 1))
        texto_fichas = fonte_muito_pequena.render(str(myPlayer.qtdMoedas), 0, (4, 15, 133))
        
        clock.tick(60)
        redesenhar_tela(texto_nome, texto_fichas, [], myPlayer, currGameState)

        if(currGameState.jogadores[currGameState.jogadorDaVez].nome == nome):
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #apertou o X da janela
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posicao = pygame.mouse.get_pos()
                    if check.clicar(posicao): #apertou no check
                        s.send(str.encode("check"))
                    elif raise_botao.clicar(posicao): #apertou no raise
                        valor_raise = menu(1)
                        if valor_raise.isnumeric():
                            if valor_raise >= currGameState.maior_aposta:
                                valor=str(valor_raise)
                                s.send(str.encode(valor))
                    elif call.clicar(posicao): #apertou call
                        s.send(str.encode("call"))
                    elif fold.clicar(posicao): #apertou o fold
                        s.send(str.encode("fold"))

    # print("Cartas na mao: ", mao)

    """
    FLOP
    1)Viramos as 3 primeiras cartas na mesa
    2)Recebemos as cartas
    4)So podemos passar para a proxima fase quando todas as apostas forem iguais
    """

    while True:
        msg = s.recv(4096)
        currGameState = pickle.loads(msg)
        for jogador in currGameState.jogadores:
            if(jogador.nome==nome):
                myPlayer = jogador
        texto_nome = fonte_pequena.render(nome, 1, (4, 15, 1))
        texto_fichas = fonte_muito_pequena.render(str(myPlayer.qtdMoedas), 0, (4, 15, 133))
        
        clock.tick(60)
        redesenhar_tela(texto_nome, texto_fichas, [], myPlayer, currGameState)
        if(currGameState.nomesJogadores[currGameState.jogadorDaVez] == nome):
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #apertou o X da janela
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posicao = pygame.mouse.get_pos()
                    if check.clicar(posicao): #apertou no check
                        s.send(str.encode("check"))
                    elif raise_botao.clicar(posicao): #apertou no raise
                        valor_raise = menu(1)
                        if valor_raise.isnumeric():
                            if valor_raise >= currGameState.maior_aposta:
                                s.send("raise")
                                valor=str(valor_raise)
                                s.send(str.encode(valor))
                    elif call.clicar(posicao): #apertou call
                        s.send(str.encode("call"))
                        # jogador_atual.alterar_aposta((mesa.maior_aposta-jogador_atual.valor_aposta), mesa) #iguala a maior aposta da mesa
                        # run=False
                    elif fold.clicar(posicao): #apertou o fold
                        s.send(str.encode("fold"))
                        # jogador_atual.desistiu=True
                        # mesa.jogadores_validos.remove(jogador_atual)
                        # run=False

    #Transicao entre turnos

    
    msg = s.recv(16)
    mesa = pickle.loads(msg)

    print("Cartas na mao: ", mao)
    print("Cartas na mesa: ", mesa)
    # redesenhar_tela()

    while True:
        msg = s.recv(128)
        currGameState = pickle.loads(msg)
        clock.tick(60)
        if(currGameState.nomesJogadores[currGameState.jogadorDaVez] == nome):
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #apertou o X da janela
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posicao = pygame.mouse.get_pos()
                    if check.clicar(posicao): #apertou no check
                        s.send(str.encode("check"))
                    elif raise_botao.clicar(posicao): #apertou no raise
                        valor_raise = menu(1)
                        if valor_raise.isnumeric():
                            if valor_raise >= currGameState.maior_aposta:
                                s.send("raise")
                                valor=str(valor_raise)
                                s.send(str.encode(valor))
                    elif call.clicar(posicao): #apertou call
                        s.send(str.encode("call"))
                        # jogador_atual.alterar_aposta((mesa.maior_aposta-jogador_atual.valor_aposta), mesa) #iguala a maior aposta da mesa
                        # run=False
                    elif fold.clicar(posicao): #apertou o fold
                        s.send(str.encode("fold"))
                        # jogador_atual.desistiu=True
                        # mesa.jogadores_validos.remove(jogador_atual)
                        # run=False

    """
    TURN
    1)Recebmos mais uma carta que foi virada na mesa
    2)Temos que mandar a aposta desejada
    3)So podemos passar para a proxima fase quando todas as apostas forem iguais
    """

menu(0)


# def receiveCard(s, buf, cardSet):
#     if buf.find(endFlag) == -1:
#         aux = s.recv(64).decode()
#         print(aux)
#         buf += str(aux)
    
#     pos = buf.find(endFlag)
#     carta = buf[:pos]
#     print(carta)
#     cardSet.append(carta)
#     buf = buf[pos+3:]
#     print(buf)
#     return buf

# try:
#     data = s.recv(22).decode()
#     buf += str(data)
#     pos = buf.find(endFlag)
#     data = buf[:pos]
#     buf = buf[pos+3:]
#     print("Received: ", data)
#     if data=="Pronto para jogar":
#         print("Comecando o jogo.")
#         #Aqui começa o jogo
#         while True:
#             """
#             PRE-FLOP
#             1)Distribuimos as cartas
#             2)Jogadores smallBlind e bigBlind colocam as apostas iniciais na mesa
#             3)So podemos passar para a proxima fase quando todas as apostas forem iguais
#             """
#             buf = receiveCard(s, buf, mao)
#             print(buf)
#             buf = receiveCard(s, buf, mao)


#             print("Cartas na mao: ", mao)
#             """
#             FLOP
#             1)Viramos as 3 primeiras cartas na
#             2)Recebemos as cartas
#             4)So podemos passar para a proxima fase quando todas as apostas forem iguais
#             """
#             buf = receiveCard(s, buf, mesa)
#             buf = receiveCard(s, buf, mesa)
#             buf = receiveCard(s, buf, mesa)

#             print("Cartas na mao: ", mao)
#             print("Cartas na mesa: ", mesa)

#             while True:
#                 if buf.find(endFlag) == -1:
#                     aux = s.recv(64).decode()
#                     buf += str(aux)
#                 pos = buf.find(endFlag)
#                 situacao = buf[:pos]
#                 buf = buf[pos+3:]
#                 if situacao=="Escolha a jogada":
#                     jogada = input("Escolha qual acao deseja realizar: (digite call, raise ou fold) ")
#                     s.send(str.encode(jogada))
#                 elif situacao=="Jogada invalida":
#                     print("Jogada invalida.")
#                 elif situacao=="raise":
#                     n_fichas = input("Para quantas fichas deseja aumentar a aposta: ")
#                     s.send(str.encode(n_fichas))
#                 elif situacao=="wrongRaise":
#                     jogada = input("Nao pode colocar menos fichas do que a aposta atual. Para quantas fichas deseja aumentar a aposta: ")
#                     s.send(str.encode(jogada))
#                 elif situacao=="Fim da rodada":
#                     break

#             if buf.find(endFlag) == -1:
#                 aux = s.recv(64).decode()
#                 buf += str(aux)
#             pos = buf.find(endFlag)
#             perda_da_rodada = buf[:pos]
#             buf = buf[pos+3:]
#             #get the num
#             #num = int(perda_da_rodada)
#             print("Perda da rodada:", str(perda_da_rodada))

#             """
#             TURN
#             1)Recebmos mais uma carta que foi virada na mesa
#             2)Temos que mandar a aposta desejada
#             3)So podemos passar para a proxima fase quando todas as apostas forem iguais
#             """

#             print(buf)

#             buf = receiveCard(s, buf, mesa)
#             print("Cartas na mesa: ", mesa)

#             while True:
#                 if buf.find(endFlag) == -1:
#                     aux = s.recv(64).decode()
#                     print(aux)
#                     buf += str(aux)
#                 pos = buf.find(endFlag)
#                 situacao = buf[:pos]
#                 buf = buf[pos+3:]

#                 if situacao=="Escolha a jogada":
#                     jogada = input("Escolha qual acao deseja realizar: (digite bet, call, raise ou fold)")
#                     s.send(str.encode(jogada))
#                 elif situacao=="Jogada invalida":
#                     print("Jogada invalida.")
#                 elif situacao=="raise":
#                     n_fichas = input("Para quantas fichas deseja aumentar a aposta: ")
#                     s.send(str.encode(n_fichas))
#                 elif situacao=="wrongRaise":
#                     jogada = input("Nao pode colocar menos fichas do que a aposta atual. Para quantas fichas deseja aumentar a aposta: ")
#                     s.send(str.encode(jogada))
#                 elif situacao=="wrongBet":
#                     print("Ja existe uma aposta na mesa. Bet nao eh mais valido.")
#                 elif situacao=="wrongCall":
#                     print("Ainda nao ha uma aposta na mesa. Call nao eh valido.")
#                 elif situacao=="Fim da rodada":
#                     break

#             if buf.find(endFlag) == -1:
#                 aux = s.recv(64).decode()
#                 buf += str(aux)
#             pos = buf.find(endFlag)
#             perda_da_rodada = buf[:pos]
#             buf = buf[pos+3:]
#             #get the num
#             #num = int(perda_da_rodada)
#             print("Perda da rodada:", str(perda_da_rodada))

#             """
#             RIVER
#             1)Recebmos mais uma carta que foi virada na mesa
#             2)Temos que mandar a aposta desejada
#             3)So podemos passar para a proxima fase quando todas as apostas forem iguais
#             """
#             buf = receiveCard(s, buf, mesa)
#             print("Cartas na mesa: ", mesa)

#             while True:
#                 if buf.find(endFlag) == -1:
#                     aux = s.recv(64).decode()
#                     print(aux)
#                     buf += str(aux)
#                 pos = buf.find(endFlag)
#                 situacao = buf[:pos]
#                 buf = buf[pos+3:]
#                 if situacao=="Escolha a jogada":
#                     jogada = input("Escolha qual acao deseja realizar: ")
#                     s.send(str.encode(jogada))
#                 elif situacao=="Jogada invalida":
#                     print("Jogada invalida.")
#                 elif situacao=="raise":
#                     n_fichas = input("Para quantas fichas deseja aumentar a aposta: ")
#                     s.send(str.encode(n_fichas))
#                 elif situacao=="wrongRaise":
#                     jogada = input("Nao pode colocar menos fichas do que a aposta atual. Para quantas fichas deseja aumentar a aposta: ")
#                     s.send(str.encode(jogada))
#                 elif situacao=="wrongBet":
#                     print("Ja existe uma aposta na mesa. Bet nao eh mais valido.")
#                 elif situacao=="wrongCall":
#                     print("Ainda nao ha uma aposta na mesa. Call nao eh valido.")
#                 elif situacao=="Fim da rodada":
#                     break

#             if buf.find(endFlag) == -1:
#                 aux = s.recv(64).decode()
#                 buf += str(aux)
#             pos = buf.find(endFlag)
#             perda_da_rodada = buf[:pos]
#             buf = buf[pos+3:]
#             #get the num
#             #num = int(perda_da_rodada)
#             print("Perda da rodada:", str(perda_da_rodada))

#             """
#             SHOWDOWN
#             1)Recebemos as cartas dos jogadores que ainda estao no jogo
#             2)Recebemos as pontuações do servidor
#             """


#     # if data=="Desconectando":
#         # break
# except Exception as e:
#     traceback.print_exc()
#     print(str(e))
#     s.close()

print("Connection lost")
s.close()