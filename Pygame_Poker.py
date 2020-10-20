import pygame
from Mesa import Mesa
from Jogador import Jogador
pygame.init()
pygame.font.init()
comprimento=800
altura=400
tela=pygame.display.set_mode((comprimento,altura))
k=0
pygame.display.set_caption("IME PokerStars")
clock=pygame.time.Clock()
run=True
mesa=Mesa(1)
p=0
nome=str(input('Escreva o nome do jogador '+ str(p+1)+": "))
mesa.adicionar_jogador(Jogador(nome,500))
mesa.distribuir_cartas()
mesa.colocar_cartas_mesa()
fonte = pygame.font.SysFont("comicsans", 60)
cartas_mao=[]
cartas_mesa=[]
nomes=[]
for i in range(0,2):
    for jogador in mesa.jogadores:
        cartas_mao.append(pygame.image.load(f"{str(jogador.mao[i])}.png"))
for j in range(0,5):
    for jogador in mesa.jogadores:
        cartas_mesa.append(pygame.image.load(f"{str(jogador.mao[j+2])}.png"))
for jogador in mesa.jogadores:
    nomes.append(fonte.render(jogador.nome, 1, (4, 15, 133), True))
pos=[[50,-100],[150,-100],[250,-100],[350,-100],[450,-100]]

def redrawGameWindow(pos):
    tela.fill((35,125,90))
    tela.blit(nomes[0],(20,350))
    a=200
    b=300
    for carta in cartas_mao:
        tela.blit(carta,(a,b))
        a+=100
    for i in range(0,5):
        tela.blit(cartas_mesa[i],pos[i])
    pygame.display.update()

while(run):
    clock.tick(20)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    if k<5:
        pos[k][1]+=10
        if pos[k][1]==150:
            k+=1
    redrawGameWindow(pos)


pygame.quit()