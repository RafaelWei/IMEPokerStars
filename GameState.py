class GameState:
    def __init__(self):
        self.jogadores=[]
        self.jogadores_validos=[]
        self.pot=0
        self.cartas_mesa=[]
        self.cartas_mesa_objeto=[]
        self.maior_aposta=0
        self.jogadorSmallBlind=0
        self.aposta_big=40
        self.jogadorDaVez=0