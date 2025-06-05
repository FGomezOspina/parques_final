import pygame
from tablero import Tablero

# Cargar los sprites de las fichas
sprite_amarillo = pygame.image.load("Sprites/Ficha_1.png")
sprite_azul = pygame.image.load("Sprites/Ficha_2.png")
sprite_verde = pygame.image.load("Sprites/Ficha_3.png")
sprite_rojo = pygame.image.load("Sprites/Ficha_4.png")

class Jugador:
    def __init__(self, nombre, color, fichas):
        self.nombre = nombre
        self.color = color
        self.fichas = fichas
        self.tablero = Tablero()
        self.turno = False
        self.listo = False
        self.estado = "esperando"
        self.dados = [0,0]
        self.accion = None
        self.intentos_par = 0
        self.actualizar= False
        self.tiros_dados = 0
        self.seleccionada = None
        self.historial_movimientos = []
        self.movimiento_restante = [0,0]

        # Determinar el índice del jugador basado en el color
        self.jugador_index = {
            "Amarillo": 0,
            "Azul": 1,
            "Verde": 2,
            "Rojo": 3,
            "": -1
        }[self.color]

    def actualizar_en_pantalla(self, pantalla, color_cliente):
        # Obtener el sprite correspondiente al color
        sprite_ficha = None
        if self.color == "Amarillo":
            sprite_ficha = sprite_amarillo
        elif self.color == "Azul":
            sprite_ficha = sprite_azul
        elif self.color == "Verde":
            sprite_ficha = sprite_verde
        elif self.color == "Rojo":
            sprite_ficha = sprite_rojo

        # Dibujar cada ficha del jugador
        for indice_ficha, posicion_casilla in enumerate(self.fichas):
            # Obtener las coordenadas para esta ficha
            if color_cliente == "Amarillo":
                coordenadas = self.tablero.obtener_posicion(
                    posicion_casilla, 
                    indice_ficha, 
                    self.jugador_index,
                )
            elif color_cliente == "Azul":
                if self.jugador_index == 0:
                    jugador_index = 3
                else:
                    jugador_index = self.jugador_index - 1

                coordenadas = self.tablero.obtener_posicion(
                    posicion_casilla, 
                    indice_ficha, 
                    jugador_index,
                )
            elif color_cliente == "Verde":
                if self.jugador_index == 0:
                    jugador_index = 2
                elif self.jugador_index == 1:
                    jugador_index = 3
                else:
                    jugador_index = self.jugador_index - 2

                coordenadas = self.tablero.obtener_posicion(
                    posicion_casilla, 
                    indice_ficha, 
                    jugador_index
                )
            elif color_cliente == "Rojo":
                if self.jugador_index == 0:
                    jugador_index = 1
                elif self.jugador_index == 1:
                    jugador_index = 2
                elif self.jugador_index == 2:
                    jugador_index = 3
                else:
                    jugador_index = 0

                coordenadas = self.tablero.obtener_posicion(
                    posicion_casilla, 
                    indice_ficha, 
                    jugador_index
                )
            
            if coordenadas:
                if posicion_casilla == 72:
                    # Ajustar la posición para evitar superposición en la casilla final
                    x = coordenadas[0] + (indice_ficha * 10)
                    y = coordenadas[1] + (indice_ficha * 10)
                else:
                    x = coordenadas[0] + (indice_ficha * 2)  # Ajustar la posición para evitar superposición
                    y = coordenadas[1] + (indice_ficha * 2)
                
                # Actualizar la posición de la ficha en el tablero
                self.tablero.actualizar_posicion_ficha(self.jugador_index, indice_ficha, (x, y))
                
                # Dibujar la ficha
                pantalla.blit(sprite_ficha, (x, y))
                
                # Dibujar la hitbox para cada ficha
                hitbox = pygame.Rect(x, y, sprite_ficha.get_width(), sprite_ficha.get_height())
        
    # Función auxiliar para dibujar texto
    def dibujar_nombre(self,pantalla, color_cliente):
        fuente = pygame.font.Font(None, 32)
        # Mostrar el nombre según el estado
        if self.estado == "listo":
            nombre_mostrado = f"{self.nombre} - Listo"
        elif self.estado == "jugando":
            nombre_mostrado = self.nombre
        else:
            nombre_mostrado = self.nombre
        
        texto = fuente.render(nombre_mostrado, True, (0,0,0))

        if color_cliente == "Amarillo":
            pantalla.blit(texto, Tablero().nombres[self.jugador_index])
        
        elif color_cliente == "Azul":
            if self.jugador_index == 0:
                jugador_index = 3
            else:
                jugador_index = self.jugador_index - 1
            pantalla.blit(texto, Tablero().nombres[jugador_index])
        
        elif color_cliente == "Verde":
            if self.jugador_index == 0:
                jugador_index = 2
            elif self.jugador_index == 1:
                jugador_index = 3
            else:
                jugador_index = self.jugador_index - 2
            pantalla.blit(texto, Tablero().nombres[jugador_index])

        elif color_cliente == "Rojo":
            if self.jugador_index == 0:
                jugador_index = 1
            elif self.jugador_index == 1:
                jugador_index = 2
            elif self.jugador_index == 2:
                jugador_index = 3
            else:
                jugador_index = 0
            pantalla.blit(texto, Tablero().nombres[jugador_index])