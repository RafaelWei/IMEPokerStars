from Poker import *
from Mesa import Mesa
from Jogador import Jogador
if __name__ == '__main__':
    njogadores=int(input('Escolha a quantidade de jogadores: '))

    mesa=Mesa(njogadores)
    for i in range(0, njogadores):
        nome=str(input('Escreva o nome do jogador '+ str(i+1)+": "))
        mesa.adicionar_jogador(Jogador(nome,500))
    mesa.distribuir_cartas()
    mesa.colocar_cartas_mesa()
    print(mesa.checa_vencedor())
