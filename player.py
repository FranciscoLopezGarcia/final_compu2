class Player:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.total = 0
        self.estado = "jugando"

    def add_card(self, carta):
        self.mano.append(carta)
        self.total += carta
        if self.total > 21:
            self.estado = "perdio"
        elif self.total == 21:
            self.estado = "gano"
        return carta
    
    def get_status(self):
        return {
            "nombre": self.nombre,
            "mano": self.mano,
            "total": self.total,
            "estado": self.estado
        }