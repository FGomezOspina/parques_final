import pygame

class MenuInicio:
    def __init__(self, pantalla):
        # --- Parámetros de la ventana/menu ---
        self.ancho = 900
        self.altura = 720
        self.pantalla = pantalla

        # --- Fondo y título (tu imagen existente) ---
        self.fondo = pygame.image.load('sprites/fondomenu.jpg').convert()
        self.fondo = pygame.transform.scale(self.fondo, (self.ancho, self.altura))
        self.titulo_imagen = pygame.image.load('sprites/titulo.png').convert_alpha()
        # Escalamos el título a 450×120 (ajusta si lo necesitas distinto)
        self.titulo_imagen = pygame.transform.scale(self.titulo_imagen, (450, 120))

        # --- Fuente para textos ---
        self.fuente_input = pygame.font.Font(None,  thirty_two := 32)
        self.fuente_boton = pygame.font.Font(None, sixty := 48)
        self.fuente_error = pygame.font.Font(None, twenty_eight := 28)

        # --- Input de nombre ---
        # Rectángulo que marca la zona donde el usuario escribe su nombre
        self.input_rect = pygame.Rect(self.ancho // 2 - 225,  # x
                                      self.altura // 2 - 180,  # y
                                      450,                    # ancho
                                      50)                     # alto
        self.nombre_texto = ""
        self.input_activo = False
        self.cursor_visible = True
        self.cursor_timer = 0

        # --- Selector de color (rectángulo que muestra la opción actual) ---
        self.colores_disponibles = ['Amarillo', 'Azul', 'Verde', 'Rojo']
        # Colores RGB reales para cada nombre, para que se vea algo:
        self.map_color = {
            'Amarillo': (245, 223, 77),
            'Azul':     (66, 135, 245),
            'Verde':    (80, 200, 120),
            'Rojo':     (235, 75, 75)
        }
        self.color_actual = 0
        self.color_rect = pygame.Rect(self.ancho // 2 - 100,    # x
                                      self.altura // 2 - 100,   # y
                                      200,                      # ancho
                                      50)                       # alto

        # --- Botón “¡JUGAR!” (rectángulo con texto) ---
        self.play_rect = pygame.Rect(self.ancho // 2 - 150,     # x
                                     self.altura // 2 +  20,   # y
                                     300,                     # ancho
                                     70)                      # alto

        # --- Mensaje de error (se muestra si el usuario intenta jugar sin nombre) ---
        self.mensaje_error = ""
        self.tiempo_error = 0

    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        self.tiempo_error = pygame.time.get_ticks()

    def procesar_eventos(self, event):
        # --- Manejo de clics y teclado ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # 1) Si el clic está dentro del cuadro de texto, lo activamos para escribir
            if self.input_rect.collidepoint(mouse_pos):
                self.input_activo = True
            else:
                self.input_activo = False

            # 2) Si el clic está dentro del rectángulo de color, cambiamos al siguiente color
            if self.color_rect.collidepoint(mouse_pos):
                self.color_actual = (self.color_actual + 1) % len(self.colores_disponibles)

            # 3) Si el clic está dentro del botón “¡JUGAR!”, validamos el nombre
            if self.play_rect.collidepoint(mouse_pos):
                if len(self.nombre_texto.strip()) > 0:
                    return {
                        'nombre': self.nombre_texto.strip(),
                        'color':  self.colores_disponibles[self.color_actual]
                    }
                else:
                    self.mostrar_error("Por favor ingresa tu nombre antes de jugar.")

        elif event.type == pygame.KEYDOWN and self.input_activo:
            # Solo procesamos teclas si el input está activo
            if event.key == pygame.K_BACKSPACE:
                self.nombre_texto = self.nombre_texto[:-1]
            elif event.key == pygame.K_RETURN:
                # Si presiona Enter estando en el input, nada especial (podrías incluso intentar jugar):
                pass
            else:
                # Concatenamos caracteres normales (podrías filtrar si quieres solo letras/dígitos)
                self.nombre_texto += event.unicode

        return None

    def actualizar(self, delta_time):
        # Hacemos parpadear el cursor cada 500 ms
        self.cursor_timer += delta_time
        if self.cursor_timer >= 500:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

        # Limpiar mensaje de error después de 3 segundos
        if self.mensaje_error != "":
            if pygame.time.get_ticks() - self.tiempo_error > 3000:
                self.mensaje_error = ""

    def dibujar(self):
        # 1) Fondo
        self.pantalla.blit(self.fondo, (0, 0))

        # 2) Título centrado arriba
        titulo_x = self.ancho // 2 - self.titulo_imagen.get_width() // 2
        self.pantalla.blit(self.titulo_imagen, (titulo_x, 40))

        # 3) Panel semitransparente oscuro detrás de todo
        panel_surf = pygame.Surface((550, 380), pygame.SRCALPHA)
        panel_surf.fill((0, 0, 0, 180))  # negro con alfa=180 (semi-opa)
        panel_x = self.ancho // 2 - 275
        panel_y = self.altura // 2 - 210
        self.pantalla.blit(panel_surf, (panel_x, panel_y))

        # 4) Cuadro de texto (input de nombre)
        #   - Borde coloreado si está activo
        borde_color = (245, 180, 60) if self.input_activo else (200, 200, 200)
        pygame.draw.rect(self.pantalla, borde_color, self.input_rect, border_radius=8)
        pygame.draw.rect(self.pantalla, (30, 30, 30), self.input_rect.inflate(-4, -4), border_radius=6)

        #   - Texto ingresado
        texto_superficie = self.fuente_input.render(self.nombre_texto, True, (255, 255, 255))
        self.pantalla.blit(texto_superficie, (self.input_rect.x + 10, self.input_rect.y + 10))

        #   - Cursor parpadeante
        if self.input_activo and self.cursor_visible:
            cursor_x = self.input_rect.x + 10 + texto_superficie.get_width()
            cursor_y = self.input_rect.y + 10
            cursor_height = self.fuente_input.get_height()
            pygame.draw.line(self.pantalla, (255, 255, 255),
                             (cursor_x, cursor_y),
                             (cursor_x, cursor_y + cursor_height),
                             2)

        # 5) Selector de color
        #   - Fondo del rectángulo: color brillante del color actual
        color_nombre = self.colores_disponibles[self.color_actual]
        color_rgb = self.map_color[color_nombre]
        pygame.draw.rect(self.pantalla, color_rgb, self.color_rect, border_radius=8)
        #   - Borde blanco
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.color_rect, 3, border_radius=8)

        #   - Texto que indica el nombre del color en contraste
        texto_color = self.fuente_input.render(color_nombre, True, (0, 0, 0))
        txt_x = self.color_rect.x + self.color_rect.width // 2 - texto_color.get_width() // 2
        txt_y = self.color_rect.y + self.color_rect.height // 2 - texto_color.get_height() // 2
        self.pantalla.blit(texto_color, (txt_x, txt_y))

        # 6) Botón “¡JUGAR!”
        #   - Detectar si el ratón está sobre el botón para cambiar el color ligeramente
        mouse_pos = pygame.mouse.get_pos()
        if self.play_rect.collidepoint(mouse_pos):
            boton_color = (70, 170, 250)  # más claro al pasar el cursor
            texto_color_boton = (255, 255, 255)
        else:
            boton_color = (50, 130, 220)
            texto_color_boton = (255, 255, 255)

        pygame.draw.rect(self.pantalla, boton_color, self.play_rect, border_radius=12)
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.play_rect, 4, border_radius=12)

        texto_play = self.fuente_boton.render("¡JUGAR!", True, texto_color_boton)
        play_x = self.play_rect.x + self.play_rect.width // 2 - texto_play.get_width() // 2
        play_y = self.play_rect.y + self.play_rect.height // 2 - texto_play.get_height() // 2
        self.pantalla.blit(texto_play, (play_x, play_y))

        # 7) Mensaje de error (si existe)
        if self.mensaje_error != "":
            texto_err = self.fuente_error.render(self.mensaje_error, True, (255, 70, 70))
            err_x = self.ancho // 2 - texto_err.get_width() // 2
            err_y = self.altura // 2 + 110
            self.pantalla.blit(texto_err, (err_x, err_y))
