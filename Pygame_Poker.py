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
fonte_muito_pequena = pygame.font.SysFont("comicsans", 20)
pos=[[50,-100],[150,-100],[250,-100],[350,-100],[450,-100]]
check=Botao("check",600,300,(119, 107, 181),40,100,50)
prosseguir=Botao("Entrar na partida",220,250,(119,107,181),20,110,20)
cartas_mao = []
cartas_mesa = []
resultados=['Carta alta','Par','Dois pares','Trinca','Sequencia','Flush','Full House','Quadra','Straight Flush','Royal Flush']
p=0

def redrawGameWindow(texto_nome):
    tela.fill((35,125,90))
    check.desenhar(tela)
    tela.blit(texto_nome,(20,350))
    a=200
    b=300
    for carta in cartas_mao:
        tela.blit(carta,(a,b))
        a+=100
    for i in range(0,5):
        tela.blit(cartas_mesa[i],pos[i])
    pygame.display.update()
#linha de comentario
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

def main(nome):
    mesa = Mesa(1)
    mesa.adicionar_jogador(Jogador(nome, 500))
    texto_nome=fonte_pequena.render(nome,1,(4, 15, 133))
    mesa.distribuir_cartas()
    mesa.colocar_cartas_mesa()
    clock = pygame.time.Clock()
    run = True
    k = 0
    ncartas = 3
    clique=0
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
        if ncartas<6:
            if k<ncartas:
                pos[k][1]+=10
                if pos[k][1]==150:
                    k+=1
        redrawGameWindow(texto_nome)
    resultado(mesa.checa_vencedor())

def menu():
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    texto_usuario=texto_usuario[0:-1]
                else:
                    if len(texto_usuario)<=10:
                        texto_usuario += event.unicode
        tela.fill((35,125,90))
        pygame.draw.rect(tela,cor_retangulo,retangulo)
        texto_titulo = fonte_grande.render("Digite o seu nome:", 1, (4, 15, 133))
        tela.blit(texto_titulo,(125,50))
        texto=fonte_pequena.render(texto_usuario,1,(4, 15, 133))
        tela.blit(texto,(retangulo.x+5,retangulo.y+5))
        prosseguir.desenhar(tela)
        pygame.display.update()
    main(texto_usuario)
menu()