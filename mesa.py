from blackjack import Blackjack

class MesaBlackjack:
    def __init__(self, id_mesa):
        self.id = id_mesa
        self.jugadores = []  # Lista de Player
        self.juegos = {}     # conn -> Blackjack

    def agregar_jugador(self, conn, jugador):
        self.jugadores.append(jugador)
        self.juegos[conn] = Blackjack(jugador)

    def repartir_a(self, conn):
        """Reparte una carta al jugador asociado a esa conexión"""
        juego = self.juegos.get(conn)
        if juego:
            return juego.repartir()
        return None

    def get_estado_de(self, conn):
        """Devuelve el estado del jugador asociado a esa conexión"""
        juego = self.juegos.get(conn)
        if juego:
            return juego.jugador.get_status()
        return None

    def get_info_mesa(self):
        """Devuelve un resumen de los jugadores en la mesa"""
        return [jugador.nombre for jugador in self.jugadores]
