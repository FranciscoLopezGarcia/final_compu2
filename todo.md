## Fase 1: Núcleo del Juego Multimesa
1.  **Permitir Múltiples Partidas (Mesas de Juego)**
    * [ ] **Diseñar cómo el servidor manejará varias "mesas" de Blackjack a la vez.** (Cada mesa es una partida independiente).
    * [ ] **Modificar el servidor para crear y administrar estas mesas.**
    * [ ] **Implementar comandos básicos para que los jugadores puedan:**
        * [ ] Ver mesas disponibles.
        * [ ] Unirse a una mesa específica.
        * [ ] (Opcional) Crear una nueva mesa si no hay disponibles o si se quiere una privada.

2.  **Mejorar la Comunicación Cliente-Servidor**
    * [ ] **Definir un conjunto de comandos claros para el juego.** (Ejemplos: `PEDIR_CARTA`, `PLANTARSE`, `VER_MANO`, `UNIRSE_MESA <id_mesa>`).
    * [ ] **Actualizar el cliente y el servidor para usar estos comandos estructurados.**
    * [ ] **Asegurar que el servidor envíe respuestas claras al cliente sobre el estado del juego y el resultado de sus acciones.**

## Fase 2: Concurrencia y Estabilidad
3.  **Manejo Seguro de Jugadores Concurrentes**
    * [ ] **Revisar cómo se manejan los múltiples jugadores conectados y sus acciones.**
    * [ ] **Si varias acciones pueden ocurrir "al mismo tiempo" sobre una misma mesa o recurso compartido (ej. un mazo de cartas para una mesa), implementar mecanismos de control** (como `Locks` o semáforos) para evitar errores o inconsistencias.
    * [ ] **Probar el juego con múltiples clientes para asegurar que funciona correctamente bajo concurrencia.**

## Fase 3: Empaquetado y Despliegue (Requisito de la materia)
4.  **Preparar la Aplicación para Distribución con Docker**
    * [ ] **Escribir un `Dockerfile` para el servidor del juego.**
        * Este archivo le dirá a Docker cómo construir una imagen que contenga tu juego y todo lo necesario para que se ejecute.
    * [ ] **Probar que puedes construir la imagen de Docker y ejecutar tu servidor de Blackjack desde un contenedor Docker.**