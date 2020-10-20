import pygame
class Botao():
    def __init__(self, texto, x, y, cor):
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.comprimento = 100
        self.altura = 50

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.comprimento, self.altura))
        font = pygame.font.SysFont("comicsans", 40)
        texto = font.render(self.texto, 1, (255, 255, 255))
        tela.blit(texto, (self.x + round(self.comprimento / 2) - round(texto.get_width() / 2),
                        self.y + round(self.altura / 2) - round(texto.get_height() / 2)))

    def clicar(self, posicao):
        x1 = posicao[0]
        y1 = posicao[1]
        return (self.x <= x1 <= self.x + self.comprimento) and (self.y <= y1 <= self.y + self.altura)
