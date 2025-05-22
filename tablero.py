class Tablero:
    def __init__(self):
        # Define las posiciones de cada casilla en pantalla

        self.nombres =[(5, 690), (484, 690), (484, 10), (5, 10)]

        self.casillas_carcel = [
            # Cárcel Amarillo (jugador 0)
            [(53, 531), (157, 531), (53, 635), (157, 635)],
            # Cárcel Azul (jugador 1)
            [(531, 531), (635, 531), (531, 635), (635, 635)],
            # Cárcel Verde (jugador 2)
            [(531, 53), (635, 53), (531, 157), (635, 157)],
            # Cárcel Rojo (jugador 3)
            [(53, 53), (157, 53), (53, 157), (157, 157)]
        ]
        
        self.casillas = [
            # Casillas del tablero principal
            (139, 424), (173, 424), (207, 424), 
            (241, 424), (275, 447), (264, 481),
            (264, 515), (264, 549), (264, 583),
            (264, 617), (264, 651), (264, 685),
            (344, 685), (424, 685), (424, 651),
            (424, 617), (424, 583), (424, 549),
            (424, 515), (424, 481), (413, 447),
            (447, 424), (481, 424), (515, 424),
            (549, 424), (583, 424), (617, 424),
            (651, 424), (685, 424), (685, 344),
            (685, 264), (651, 264), (617, 264),
            (583, 264), (549, 264), (515, 264),
            (481, 264), (447, 264), (413, 241),
            (424, 207), (424, 173), (424, 139),
            (424, 105), (424, 71), (424, 37),
            (424, 3), (344, 3), (264, 3),
            (264, 37), (264, 71), (264, 105),
            (264, 139), (264, 173), (264, 207),
            (264, 241), (241, 264), (207, 264), 
            (173, 264), (139, 264), (105, 264),
            (71, 264), (37, 264), (3, 264),
            (3, 344),
            
            # Casillas camino al cielo jugador 0
            (37, 344), (71, 344), (105, 344), 
            (139, 344), (173, 344), (207, 344), 
            (244, 344), (303, 344),

            # casillas restantes camino por el jugador 0
            (3, 424), (37, 424),
            (71, 424), (105, 424),

            # Casillas camino al cielo jugador 1
            (344, 651), (344, 617), (344, 583),
            (344, 549), (344, 515), (344, 481),
            (344, 444), (344, 385),

            # Casillas camino al cielo jugador 2
            (651, 344), (617, 344), (583, 344),
            (549, 344), (515, 344), (481, 344),
            (444, 344), (385, 344),

            # Casillas camino al cielo jugador 3
            (344, 37), (344, 71), (344, 105),
            (344, 139), (344, 173), (344, 207),
            (344, 244), (344, 303)
        ]

        # Almacenar las posiciones actuales de las fichas
        self.posiciones_fichas = [[None for _ in range(4)] for _ in range(4)]

    def obtener_posicion(self, numero_casilla, numero_ficha, jugador):
        """
        Obtiene la posición en píxeles para una ficha.
        
        Args:
            numero_casilla: Número de casilla (0 para cárcel)
            numero_ficha: Índice de la ficha (0-3)
            jugador: Índice del jugador (0-3)
            
        Returns:
            tuple: Coordenadas (x, y) en píxeles
        """
        try:
            if numero_casilla == 0:  # Si está en la cárcel
                if 0 <= jugador < len(self.casillas_carcel) and 0 <= numero_ficha < 4:
                    return self.casillas_carcel[jugador][numero_ficha]
            elif 1 <= numero_casilla <= len(self.casillas):
                #Si el jugador es 0
                if jugador == 0 and numero_casilla - 1 <= 71:
                    return self.casillas[numero_casilla - 1]
                #Si el jugador es 1
                elif jugador == 1:
                    if numero_casilla + 16 <= 63:
                        return self.casillas[numero_casilla + 16]
                    elif numero_casilla + 24 <= 75:
                        return self.casillas[numero_casilla + 24]
                    elif numero_casilla - 52 <= 12:
                        return self.casillas[numero_casilla - 52]
                    elif numero_casilla + 11 <= 83:
                        return self.casillas[numero_casilla + 11]
                #Si el jugador es 2
                elif jugador == 2:
                    if numero_casilla + 33 <= 63:
                        return self.casillas[numero_casilla + 33]
                    elif numero_casilla + 41 <= 75:
                        return self.casillas[numero_casilla + 41]
                    elif numero_casilla - 35 <= 29:
                        return self.casillas[numero_casilla - 35]
                    elif numero_casilla + 19 <= 91:
                        return self.casillas[numero_casilla + 19]
                #Si el jugador es 3
                elif jugador == 3:
                    if numero_casilla + 50 <= 63:
                        return self.casillas[numero_casilla + 50]
                    elif numero_casilla + 58 <= 75:
                        return self.casillas[numero_casilla + 58]
                    elif numero_casilla - 18 <= 46:
                        return self.casillas[numero_casilla - 18]
                    elif numero_casilla + 27 <= 99:
                        return self.casillas[numero_casilla + 27]
            return None
        except Exception as e:
            print(f"Error obteniendo posición: {e}")
            return None

    def actualizar_posicion_ficha(self, jugador, numero_ficha, posicion):
        """
        Actualiza la posición de una ficha en el tablero.
        
        Args:
            jugador: Índice del jugador (0-3)
            numero_ficha: Índice de la ficha (0-3)
            posicion: Coordenadas (x, y) en píxeles
        """
        if 0 <= jugador < len(self.posiciones_fichas) and 0 <= numero_ficha < 4:
            self.posiciones_fichas[jugador][numero_ficha] = posicion