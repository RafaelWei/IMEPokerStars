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
p=0

def resultado_final(jogador,clock):
    vencedor_texto = fonte_grande.render('Vencedor:', 1, (4, 5, 133))
    nome_vencedor = fonte_grande.render(jogador.nome, 1, (4, 5, 133))
    dinheiro_vencedor=fonte.render('Saldo final: '+str(jogador.qtdMoedas)+' moedas',1,(4,5,133))
    run=True
    while (run):
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        tela.fill((35, 125, 90))
        tela.blit(vencedor_texto, (250, 50))
        tela.blit(nome_vencedor, (300, 150))
        tela.blit(dinheiro_vencedor,(150,250))
        pygame.display.update()

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
    tela.blit(dealer_objeto, (590, (c+delta*(mesa.dealer))))
    for player in mesa.jogadores:
        nome_aposta=fonte_muito_pequena.render(player.nome,1,(0,0,0))
        tela.blit(nome_aposta,(620,c))
        aposta=fonte_muito_pequena.render(str(player.valor_aposta),1,(0,0,0))
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

def resultado(resultado_jogo,clock,mesa):
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
        if len(mesa.jogadores_validos)!=1:
            for carta in cartas_resultado:
                tela.blit(carta, (d,15))
                d += 100
            tela.blit(resultado_mao,(150,120))
        prox_rodada.desenhar(tela)
        pygame.display.update()

def main(nomes,clock):
    mesa = Mesa()
    for nome in nomes:
        player = Jogador(nome)
        mesa.adicionar_jogador(player)
    while len(mesa.jogadores)>1:
        p=0
        fase=0
        mesa.distribuir_cartas()
        mesa.colocar_cartas_mesa()
        mesa.definir_blinds()
        for i in range(0, 2):
            for jogador in mesa.jogadores:
                jogador.mao_objetos.append(pygame.image.load(f"./PokerStarsIME_imgs/{str(jogador.mao[i])}.png"))
        for j in range(0, 5):
            mesa.cartas_mesa_objeto.append(pygame.image.load(f"./PokerStarsIME_imgs/{str(mesa.jogadores[0].mao[j + 2])}.png"))
        cartas_visiveis=[]
        while fase!=4:
            if fase==0:
                jogador_atual=mesa.jogadores[(p+mesa.dealer+3)%len(mesa.jogadores)]
            else:
                jogador_atual = mesa.jogadores[(p + mesa.dealer + 1) % len(mesa.jogadores)]
            if len(mesa.jogadores_validos)==1:
                break
            if jogador_atual.desistiu==False and jogador_atual.allin==False:
                texto_nome = fonte_pequena.render(jogador_atual.nome, 1, (4, 15, 1))
                texto_fichas = fonte_muito_pequena.render(str(jogador_atual.qtdMoedas), 0, (4, 15, 133))
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
                                valor_raise = menu(1)
                                if valor_raise.isnumeric():
                                    if jogador_atual.valor_aposta+int(valor_raise)>=mesa.maior_aposta:
                                        jogador_atual.alterar_aposta(int(valor_raise),mesa)
                                        run=False
                            elif call.clicar(posicao):
                                jogador_atual.alterar_aposta((mesa.maior_aposta-jogador_atual.valor_aposta), mesa)
                                run=False
                            elif fold.clicar(posicao):
                                jogador_atual.desistiu=True
                                mesa.jogadores_validos.remove(jogador_atual)
                                run=False
                    redesenhar_tela(texto_nome,texto_fichas,cartas_visiveis,jogador_atual,mesa)
            p+=1
            if all((pla.valor_aposta==mesa.maior_aposta or pla.allin) for pla in mesa.jogadores_validos) and p>=len(mesa.jogadores):
                p = 0
                num_allin=0
                for jogador in mesa.jogadores:
                    if jogador.allin:
                        num_allin+=1
                    mesa.pot+=jogador.valor_aposta
                    mesa.maior_aposta=0
                    jogador.valor_aposta=0
                if len(mesa.jogadores_validos)==1:
                    break
                elif num_allin>=len(mesa.jogadores_validos)-1:
                    break
                fase+=1
                if fase==1:
                    cartas_visiveis = [mesa.cartas_mesa_objeto[0], mesa.cartas_mesa_objeto[1],mesa.cartas_mesa_objeto[2]]
                elif fase!=4:
                    cartas_visiveis.append(mesa.cartas_mesa_objeto[fase+1])
        vencedor=mesa.checa_vencedor()
        resultado(vencedor,clock,mesa)
        if isinstance(vencedor, Jogador):
            vencedor.qtdMoedas+=mesa.pot
        else:
            for jogador in vencedor:
                jogador.qtdMoedas += mesa.pot // len(vencedor)
        mesa.jogadores=[x for x in mesa.jogadores if x.qtdMoedas>0]
        for jogador in mesa.jogadores:
            jogador.devolver_cartas()
        mesa.nova_rodada()
    resultado_final(mesa.jogadores[0],clock)

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
                    if voltar.clicar(posicao):
                        if tipo == 1:
                            return 'voltou'
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
        main(nomes,clock)
    if tipo==1:
        if texto_usuario.isnumeric():
            return texto_usuario
        else:
            pygame.time.delay(2000)
            menu(1)
    if tipo==2:
        numero_players =texto_usuario
        if numero_players.isnumeric():
            if int(numero_players)>8:
                sys.exit('O numero de jogadores deve ser menor ou igual a 8')
        else:
            sys.exit('O numero deve ser inteiro')
        menu(0,int(numero_players))
menu(2)