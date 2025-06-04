# tablero.py

class Tablero:
    def __init__(self):
        # (opcional) posiciones de los nombres en las esquinas, si las usas:
        self.nombres = [(5, 690), (484, 690), (484, 10), (5, 10)]

        # --------------------------------------------------------------------
        # 16 posiciones de cárcel para cada jugador, medidas sobre 720×720 px
        # --------------------------------------------------------------------
        self.casillas_carcel = [
            # Cárcel Amarillo (jugador 0)
            [
                ( 53, 531),  # J0-0: centro del cuadro amarillo inf-izq
                (157, 531),  # J0-1
                ( 53, 635),  # J0-2
                (157, 635)   # J0-3
            ],
            # Cárcel Azul (jugador 1)
            [
                (531, 531),  # J1-0: centro del cuadro azul inf-der
                (635, 531),  # J1-1
                (531, 635),  # J1-2
                (635, 635)   # J1-3
            ],
            # Cárcel Verde (jugador 2)
            [
                (531,  53),  # J2-0: centro del cuadro verde sup-der
                (635,  53),  # J2-1
                (531, 157),  # J2-2
                (635, 157)   # J2-3
            ],
            # Cárcel Rojo (jugador 3)
            [
                ( 53,  53),  # J3-0: centro del cuadro rojo sup-izq
                (157,  53),  # J3-1
                ( 53, 157),  # J3-2
                (157, 157)   # J3-3
            ]
        ]

        # --------------------------------------------------------------------
        # 99 posiciones de “casillas” del camino principal (1–99), sobre 720×720
        # --------------------------------------------------------------------
        self.casillas = [
            # casillas 1..12 (fila inferior, encima del pasillo marrón central)
            (139, 424),  # 1
            (173, 424),  # 2
            (207, 424),  # 3
            (241, 424),  # 4
            (275, 447),  # 5
            (264, 481),  # 6
            (264, 515),  # 7
            (264, 549),  # 8
            (264, 583),  # 9
            (264, 617),  # 10
            (264, 651),  # 11
            (264, 685),  # 12

            # casillas 13..24 (curva inferior derecha)
            (344, 685),  # 13
            (424, 685),  # 14
            (424, 651),  # 15
            (424, 617),  # 16
            (424, 583),  # 17
            (424, 549),  # 18
            (424, 515),  # 19
            (424, 481),  # 20
            (413, 447),  # 21
            (447, 424),  # 22
            (481, 424),  # 23
            (515, 424),  # 24

            # casillas 25..36 (fila derecha, subiendo verticalmente)
            (549, 424),  # 25
            (583, 424),  # 26
            (617, 424),  # 27
            (651, 424),  # 28
            (685, 424),  # 29
            (685, 344),  # 30
            (685, 264),  # 31
            (651, 264),  # 32
            (617, 264),  # 33
            (583, 264),  # 34
            (549, 264),  # 35
            (515, 264),  # 36

            # casillas 37..48 (curva superior derecha)
            (481, 264),  # 37
            (447, 264),  # 38
            (413, 241),  # 39
            (424, 207),  # 40
            (424, 173),  # 41
            (424, 139),  # 42
            (424, 105),  # 43
            (424,  71),  # 44
            (424,  37),  # 45
            (424,   3),  # 46
            (344,   3),  # 47
            (264,   3),  # 48

            # casillas 49..60 (fila superior, hacia la izquierda)
            (264,  37),  # 49
            (264,  71),  # 50
            (264, 105),  # 51
            (264, 139),  # 52
            (264, 173),  # 53
            (264, 207),  # 54
            (264, 241),  # 55
            (241, 264),  # 56
            (207, 264),  # 57
            (173, 264),  # 58
            (139, 264),  # 59
            (105, 264),  # 60

            # casillas 61..72 (curva superior izquierda)
            ( 71, 264),  # 61
            ( 37, 264),  # 62
            (  3, 264),  # 63
            (  3, 344),  # 64
            ( 37, 344),  # 65
            ( 71, 344),  # 66
            (105, 344),  # 67
            (139, 344),  # 68
            (173, 344),  # 69
            (207, 344),  # 70
            (244, 344),  # 71
            (303, 344),  # 72

            # casillas 73..84 (fila izquierda, bajando verticalmente)
            (  3, 424),  # 73
            ( 37, 424),  # 74
            ( 71, 424),  # 75
            (105, 424),  # 76
            (   0,   0), # 77 <— NO se usa; sirve para alinear condicionalmente si quisieras>
                         #     (en el diseño original había un tramo “extra” que no se dibuja)
            (  48, 481), # 78  (punto 1 px a la derecha del “ 3, 424 ”)
            (  48, 464), # 79
            (  48, 447), # 80
            (  48, 430), # 81
            (  48, 413), # 82
            (  48, 396), # 83
            (  48, 379), # 84

            # casillas 85..96 (curva inferior izquierda)
            (  84, 378),  # 85
            (  96, 395),  # 86
            ( 108, 412),  # 87
            ( 120, 429),  # 88
            ( 132, 446),  # 89
            ( 144, 463),  # 90
            ( 156, 480),  # 91
            ( 168, 497),  # 92
            ( 180, 514),  # 93
            ( 192, 531),  # 94
            ( 204, 548),  # 95
            ( 216, 565),  # 96

            # casillas 97..99 (escalera central hacia el medio)
            ( 228, 587),  # 97
            ( 242, 607),  # 98
            ( 256, 627)   # 99  (justo debajo de la “99” roja del centro)
        ]

        # Resto de la inicialización
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
            # Si está en la cárcel (casilla 0)
            if numero_casilla == 0:
                if 0 <= jugador < len(self.casillas_carcel) and 0 <= numero_ficha < 4:
                    return self.casillas_carcel[jugador][numero_ficha]

            # Si va sobre el camino principal (1–99)
            elif 1 <= numero_casilla <= len(self.casillas):
                # Jugador 0: avanza sobre la lista 1..72 (índices 0..71)
                if jugador == 0 and (numero_casilla - 1) <= 71:
                    return self.casillas[numero_casilla - 1]

                # Jugador 1
                elif jugador == 1:
                    # en la lista de 720×720 está desfasado así:
                    if numero_casilla + 16 <= 63:
                        return self.casillas[numero_casilla + 16]
                    elif numero_casilla + 24 <= 75:
                        return self.casillas[numero_casilla + 24]
                    elif numero_casilla - 52 <= 12:
                        return self.casillas[numero_casilla - 52]
                    elif numero_casilla + 11 <= 83:
                        return self.casillas[numero_casilla + 11]

                # Jugador 2
                elif jugador == 2:
                    if numero_casilla + 33 <= 63:
                        return self.casillas[numero_casilla + 33]
                    elif numero_casilla + 41 <= 75:
                        return self.casillas[numero_casilla + 41]
                    elif numero_casilla - 35 <= 29:
                        return self.casillas[numero_casilla - 35]
                    elif numero_casilla + 19 <= 91:
                        return self.casillas[numero_casilla + 19]

                # Jugador 3
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
        Almacena la posición pixel-perfect de la ficha en memoria interna.
        
        Args:
            jugador: Índice del jugador (0..3)
            numero_ficha: Índice de la ficha dentro de ese jugador (0..3)
            posicion: Tupla (x, y) en píxeles sobre 720×720
        """
        if 0 <= jugador < len(self.posiciones_fichas) and 0 <= numero_ficha < 4:
            self.posiciones_fichas[jugador][numero_ficha] = posicion
