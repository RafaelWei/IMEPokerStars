import pygame
from Mesa import Mesa
from Jogador import Jogador
from Botao import Botao
import sys
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
check=Botao("check",420,350,(119, 107, 181),30,80,40)
fold=Botao("fold",420,295,(119, 107, 181),30,80,40)
call=Botao("call",520,295,(119, 107, 181),30,80,40)
raise_botao=Botao("raise",520,350,(119, 107, 181),30,80,40)
prosseguir=Botao("Prosseguir",220,250,(119,107,181),20,110,20)
prox_rodada=Botao("Proxima rodada",650,350,(119,107,181),20,110,20)
voltar=Botao("Voltar",220,280,(119,107,181),20,110,20)
moeda_objeto=(pygame.image.load(f"./PokerStarsIME_imgs/Coin.png"))
moeda_objeto=(pygame.transform.scale(moeda_objeto,(51,75)))
resultados=['Carta alta','Par','Dois pares','Trinca','Sequencia','Flush','Full House','Quadra','Straight Flush','Royal Flush']
p=0

def redrawGameWindow(texto_nome,texto_fichas,cartas_visiveis,jogador):
    tela.fill((35,125,90))
    check.desenhar(tela)
    fold.desenhar(tela)
    call.desenhar(tela)
    raise_botao.desenhar(tela)
    tela.blit(texto_nome,(20,280))
    tela.blit(texto_fichas, (80, 375))
    tela.blit(moeda_objeto,(20,315))
    a=200
    b=300
    d=150
    for carta in cartas_visiveis:
        tela.blit(carta,(d,150))
        d+=100
    for carta in jogador.mao_objetos:
        tela.blit(carta,(a,b))
        a+=100
    pygame.display.update()

def resultado(resultado_jogo,clock):
    run=True
    cartas_resultado=[]

    if isinstance(resultado_jogo,Jogador):
        cartas=resultado_jogo.mao
        mao=resultado_jogo.valor_mao
        resultado_total=resultados[mao]
        vencedor_texto = fonte_grande.render(f"Vencedor:", 1, (4, 15, 133))
        vencedor = fonte.render(f"{resultado_jogo.nome}", 1, (4, 15, 133))
    else:
        cartas = resultado_jogo[0].mao
        mao = resultado_jogo[0].valor_mao
        resultado_total = resultados[mao]
        vencedores = []
        vencedor_texto = fonte_grande.render(f"Vencedores:", 1, (4, 15, 133))
        for jogadores in resultado_jogo:
            vencedor = fonte_grande.render(f"{jogadores.nome}", 1, (4, 15, 133))
            vencedores.append(vencedor)
    resultado_mao = fonte.render(resultado_total, 1, (4, 15, 133))
    for carta in cartas:
        cartas_resultado.append(pygame.image.load(f"./PokerStarsIME_imgs/{carta}.png"))
    while (run):
        d = 150
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posicao = pygame.mouse.get_pos()
                if prox_rodada.clicar(posicao):
                    run = False
        tela.fill((35, 125, 90))
        tela.blit(vencedor_texto,(150, 180))
        if isinstance(resultado_jogo,Jogador):
            tela.blit(vencedor,(150,245))
        else:
            b=245
            for jogador in vencedores:
                tela.blit(jogador,(150,b))
                b+=60
        for carta in cartas_resultado:
            tela.blit(carta, (d,15))
            d += 100
        tela.blit(resultado_mao,(150,120))
        prox_rodada.desenhar(tela)
        pygame.display.update()

def main(nomes,clock):
    while len(nomes)>1:
        fase=0
        p=0
        njogadores=len(nomes)
        mesa = Mesa()
        for nome in nomes:
            player=Jogador(nome)
            mesa.adicionar_jogador(player)
        mesa.distribuir_cartas()
        mesa.colocar_cartas_mesa()
        for i in range(0, 2):
            for jogador in mesa.jogadores:
                jogador.mao_objetos.append(pygame.image.load(f"./PokerStarsIME_imgs/{str(jogador.mao[i])}.png"))
        for j in range(0, 5):
            mesa.cartas_mesa_objeto.append(pygame.image.load(f"./PokerStarsIME_imgs/{str(mesa.jogadores[0].mao[j + 2])}.png"))
        cartas_visiveis=[mesa.cartas_mesa_objeto[0],mesa.cartas_mesa_objeto[1],mesa.cartas_mesa_objeto[2]]
        while fase!=3:
            jogador_atual=mesa.jogadores[p]
            texto_nome = fonte_pequena.render(jogador_atual.nome, 1, (4, 15, 1))
            texto_fichas = fonte_muito_pequena.render(str(jogador_atual.qtdFichas), 0, (4, 15, 133))
            run = True
            while(run):
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        posicao = pygame.mouse.get_pos()
                        if check.clicar(posicao):
                            run=False
                        elif raise_botao.clicar(posicao):
                            valor_raise=menu(1)
                            if valor_raise!=0:
                                jogador_atual.valor_aposta=valor_raise
                                #run=False
                redrawGameWindow(texto_nome,texto_fichas,cartas_visiveis,jogador_atual)
            p+=1
            if p==njogadores:
                p=0
                fase+=1
                if fase!=3:
                    cartas_visiveis.append(mesa.cartas_mesa_objeto[fase+2])
        resultado(mesa.checa_vencedor(),clock)
        for jogador in mesa.jogadores:
            jogador.devolver_cartas()
            mesa.nova_rodada()
#tipo = 0 para menu inicial, tipo = 1 para raise e tipo=2 para menu_numero_jogadores
def menu(tipo,njogadores=0):
    p=0
    nomes = []
    run=True
    clock = pygame.time.Clock()
    texto_usuario = ''
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
                    if tipo==1:
                        if voltar.clicar(posicao):
                            return 0
                if tipo==0:
                    if prosseguir.clicar(posicao):
                        p+=1
                        nomes.append(texto_usuario)
                        texto_usuario=''
                        if p==njogadores:
                            run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if tipo!=0:
                        run = False
                    if tipo==0:
                        p += 1
                        nomes.append(texto_usuario)
                        texto_usuario = ''
                        if p == njogadores:
                            run = False
                elif event.key == pygame.K_BACKSPACE:
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

        if tipo==2:
            texto_titulo = fonte.render("Digite o numero de jogadores:", 1, (4, 15, 133))
            tela.blit(texto_titulo, (80, 80))
            texto = fonte_pequena.render(texto_usuario, 1, (4, 15, 133))
            tela.blit(texto, (retangulo.x + 5, retangulo.y + 5))
            prosseguir.desenhar(tela)
            pygame.display.update()
    if tipo==0 and p==njogadores:
        print(nomes)
        main(nomes,clock)
    if tipo==1:
        try:
            valor = int(texto_usuario)
            return valor
        except:
            pygame.time.delay(2000)
            menu(1)
    if tipo==2:
        try:
            numero_players = int(texto_usuario)
        except:
            sys.exit('O numero deve ser inteiro')
        menu(0, numero_players)
menu(2)