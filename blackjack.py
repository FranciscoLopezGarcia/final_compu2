import random

class Blackjack:
    def __init__(self, jugador):
        self.cartas = list(range(1, 12))  # Cartas simples de 1 a 11
        self.jugador = jugador

    def repartir(self):
        carta = random.choice(self.cartas)
        self.jugador.add_card(carta)
        return carta