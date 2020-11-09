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
voltar=Botao("Voltar",220,280,(119,107,181),20,110,20)
moeda_objeto=(pygame.image.load(f"./PokerStarsIME_imgs/Coin.png"))
moeda_objeto=(pygame.transform.scale(moeda_objeto,(51,75)))
cartas_mao = []
cartas_mesa = []
resultados=['Carta alta','Par','Dois pares','Trinca','Sequencia','Flush','Full House','Quadra','Straight Flush','Royal Flush']
p=0

def redrawGameWindow(texto_nome,texto_fichas):
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
    for carta in cartas_mao:
        tela.blit(carta,(a,b))
        a+=100
    for i in range(0,5):
        tela.blit(cartas_mesa[i],pos[i])
    pygame.display.update()

def resultado(resultado_jogo):
    clock = pygame.time.Clock()
    run=True
    cartas_resultado=[]
    if isinstance(resultado_jogo,Jogador):
        cartas=resultado_jogo.mao
        mao=resultado_jogo.valor_mao
        resultado_total=resultados[mao]
    else:
        cartas = resultado_jogo[0].mao
        mao = resultado_jogo[0].valor_mao
        resultado_total = resultados[mao]
    parabens = fonte_grande.render("Parabéns!", 1, (4, 15, 133))
    o_seu_resultado = fonte.render("O seu resultado foi:", 1, (4, 15, 133))
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
        tela.fill((35, 125, 90))
        tela.blit(parabens, (265, 15))
        tela.blit(o_seu_resultado, (200, 70))
        for carta in cartas_resultado:
            tela.blit(carta, (d,150))
            d += 100
        tela.blit(resultado_mao,(150,265))

        pygame.display.update()

def main(nome,clock):
    mesa = Mesa(1)
    player1=Jogador(nome)
    mesa.adicionar_jogador(player1)
    texto_nome=fonte_pequena.render(nome,1,(4, 15, 1))
    texto_fichas=fonte_muito_pequena.render(str(player1.qtdFichas),0,(4, 15, 133))
    mesa.distribuir_cartas()
    mesa.colocar_cartas_mesa()
    run = True
    k = 0
    ncartas = 3
    for i in range(0, 2):
        for jogador in mesa.jogadores:
            cartas_mao.append(pygame.image.load(f"./PokerStarsIME_imgs/{str(jogador.mao[i])}.png"))
    for j in range(0, 5):
        for jogador in mesa.jogadores:
            cartas_mesa.append(pygame.image.load(f"./PokerStarsIME_imgs/{str(jogador.mao[j + 2])}.png"))
    while(run):
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posicao = pygame.mouse.get_pos()
                if check.clicar(posicao):
                    if k==5:
                        ncartas+=1
                    elif pos[k-1][i]==150 and pos[k][i]==-100:
                        ncartas+=1
                    if ncartas==6:
                        run=False
                elif raise_botao.clicar(posicao):
                    valor_raise=menu(1)
                    if valor_raise!=0:
                        jogador.valor_aposta=valor_raise
                        #run=False
        if ncartas<6:
            if k<ncartas:
                pos[k][1]+=10
                if pos[k][1]==150:
                    k+=1
        redrawGameWindow(texto_nome,texto_fichas)
    resultado(mesa.checa_vencedor())
#tipo = 0 para menu inicial e tipo = 1 para raise
def menu(tipo):
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
                if prosseguir.clicar(posicao):
                    run=False
                if voltar.clicar(posicao):
                    return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
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
        if tipo==1:
            texto_titulo = fonte.render("Digite o valor que deseja apostar:", 1, (4, 15, 133))
            tela.blit(texto_titulo, (80, 80))
            voltar.desenhar(tela)
        texto=fonte_pequena.render(texto_usuario,1,(4, 15, 133))
        tela.blit(texto,(retangulo.x+5,retangulo.y+5))
        prosseguir.desenhar(tela)
        pygame.display.update()
    if tipo==0:
        main(texto_usuario,clock)
    if tipo==1:
        try:
            valor = int(texto_usuario)
            return valor
        except:
            pygame.time.delay(2000)
            menu(1)

menu(0)