## Aplicación de Blackjack en línea

El proyecto planteado para el final de Computación II es una aplicación de Blackjack multijugador basada en consola, donde varios usuarios pueden conectarse y jugar en turnos desde diferentes clientes.

### Características

* **Servidor multicliente**: Los jugadores se conectan por consola a un servidor central usando sockets TCP.
* **Modo por turnos**: El servidor gestiona los turnos y muestra a cada jugador su estado.
* **Reglas simples de Blackjack**: Cada jugador puede pedir carta (hit) o plantarse (stand).
* **Historial opcional**: El servidor puede guardar resultados en archivos de texto.
* **CLI interactiva**: La aplicación se ejecuta por línea de comandos (sin interfaz gráfica).

---

### Comandos

* `<start>`: Comenzar partida (cuando hay más de un jugador).
* `hit`: Pedir una carta.
* `stand`: Plantarse.
* `<quit>`: Salir del juego.