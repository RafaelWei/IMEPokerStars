import random
from Carta import Carta
valores=['2','3','4','5','6','7','8','9','10','J','Q','K','A']
naipes=["♥","♦","♠","♣"]

class Baralho:
    def __init__(self):
        self.baralho=[]
        for valor in valores:
            for naipe in naipes:
                self.baralho.append(Carta(valor, naipe))
        self.embaralhar()

    def embaralhar(self):
        random.shuffle(self.baralho)

    def sacar_carta(self):
        carta=self.baralho[0]
        self.baralho.remove(self.baralho[0])
        return carta

