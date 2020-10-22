import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created!")

port = 8080
host = '127.0.0.1'

#Registra o a porta do processo ao qual o socket vai fazer a interface
s.bind(('', port))
print("Socket binded to ", port)

#Coloca o socket em estado de listen, esperando requisicoes externas
s.listen(5)
print("Socket listening")

while True:
    #Quando um cliente conecta, ganhamos acesso ao socket do processo cliente assim como ao endereco desse cliente
    conn, addr = s.accept()

    with conn:
        print("Got connection from", addr)

        data = conn.recv(1024)
        if not data:
            s.close()
        else:
            conn.sendall(data)

        s.close()