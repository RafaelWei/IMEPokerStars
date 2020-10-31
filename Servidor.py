import socket
from _thread import *
from Jogador import Jogador
socket_Poker=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_Poker.bind(('SEU_IPV4',5555))
socket_Poker.listen()
print('Aguardando novos jogadores')
jogadores_conectados=[]

def nova_thread(conexao,jogador,jogo):
    #Manipulacao das mensagens que o servidor vai enviar
    return 0
while True:
    (conexao, endereco)=socket_Poker.accept()
    #Manipulacao do servidor do q vai acontecer quando um jogador se conectar
    jogador=0
    jogo=0
    start_new_thread(nova_thread,(conexao,jogador,jogo))
