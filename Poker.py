import random
valores=['A','2','3','4','5','6','7','8','9','10','J','Q','K']
naipes=["♥","♦","♠","♣"]
resultados=['Carta alta','Par','Dois pares','Trinca','Sequencia','Flush','Full House','Quadra','Straight Flush','Royal Flush']
class Carta():
    def __init__(self,valor,naipe):
        self.valor=valor
        self.naipe=naipe
    def __str__(self):
        return self.valor +self.naipe
    def __repr__(self):
        return self.valor +self.naipe
    def __eq__(self, other):
        return self.valor==other.valor and self.naipe==other.naipe
def Par_Trinca_Quadra(cartas):
    par_trinca_quadra=[[],[],[]]
    valores_jogo=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for i in cartas:
        valores_jogo[valores.index(i.valor)].append(i)
    for n in range(0,3):
        for m in range(0,13):
            if (len(valores_jogo[m])==n+2):
                jogo=[]
                for i in valores_jogo[m]:
                    jogo.append(i)
                par_trinca_quadra[n].append(jogo)
    if(len(par_trinca_quadra[2])>0):
        numero_resultado=7
        return numero_resultado
    if (len(par_trinca_quadra[1]) > 0 and len(par_trinca_quadra[0])>=1):
        numero_resultado=6
        return numero_resultado
    if (len(par_trinca_quadra[1]) > 0):
        numero_resultado=3
        return numero_resultado
    if (len(par_trinca_quadra[0])>=2):
        numero_resultado=2
        return numero_resultado
    if (len(par_trinca_quadra[0])==1):
        numero_resultado=1
        return numero_resultado
    return 0

def Flush(cartas):
    naipes_flush=[[],[],[],[]]
    for i in cartas:
        naipes_flush[naipes.index(i.naipe)].append(i)
    for i in range(0,4):
        if len(naipes_flush[i])>=5:
            royal=0
            cartas_royal=[Carta(valores[12],naipes[i]),Carta(valores[10],naipes[i]),Carta(valores[11],naipes[i]),\
                          Carta(valores[0],naipes[i]),Carta(valores[9],naipes[i])]
            for carta in cartas_royal:
                for carta_baralho in naipes_flush[i]:
                    if carta==carta_baralho:
                        royal+=1
                        continue
            if royal==5:
                numero_resultado=9
            else:
                if sequencia(naipes_flush[i])==4:
                    numero_resultado=8
                else:
                    numero_resultado=5
            return numero_resultado
    return 0
def sequencia(cartas):
    valores_jogo=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
    sequencia_corrente=0
    for i in cartas:
        valores_jogo[valores.index(i.valor)].append(i)
    for i in range(0,13):
        if len(valores_jogo[i])>=1:
            sequencia_corrente+=1
        if len(valores_jogo[i])==0:
            sequencia_corrente=0
        if sequencia_corrente==5:
            numero_resultado=4
            return numero_resultado
    return 0
def carta_alta(e):
    return e.valor
def jogar(cartas):
    jogo=max(Par_Trinca_Quadra(cartas),Flush(cartas),sequencia(cartas))
    print(resultados[jogo])
    if(jogo==0):
        cartas.sort(reverse=True,key=carta_alta)
        print(cartas[0])
baralho=[]
for valor in valores:
    for naipe in naipes:
        baralho.append(Carta(valor,naipe))
mesa=[]
mao=[]
#cartas=[]
for i in range(0,5):
    n1 = random.randint(0,len(baralho)-1)
    mesa.append(baralho[n1])
    #cartas.append(baralho[n1])
    baralho.remove(baralho[n1])
for i in range(0,2):
    n2 = random.randint(0,len(baralho)-1)
    mao.append(baralho[n2])
    #cartas.append(baralho[n2])
    baralho.remove(baralho[n2])
cartas=[Carta(valores[12],naipes[0]),Carta(valores[12],naipes[1]),Carta(valores[2],naipes[2]),Carta(valores[11],naipes[0]),Carta(valores[0],naipes[2]),Carta(valores[7],naipes[2]),Carta(valores[11],naipes[3])]
for i in cartas:
    print(i,end=' ')
print('\n')
jogar(cartas)



