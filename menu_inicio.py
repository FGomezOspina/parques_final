import pygame

class MenuInicio:
    def __init__(self, pantalla):
        # --- Parámetros de la ventana/menu ---
        self.ancho = 900
        self.altura = 720
        self.pantalla = pantalla

        # --- Fondo (tu imagen existente) ---
        self.fondo = pygame.image.load('sprites/fondomenu4.jpg').convert()
        self.fondo = pygame.transform.scale(self.fondo, (self.ancho, self.altura))

        # --- Fuentes ---
        self.fuente_input = pygame.font.Font(None, 32)
        self.fuente_boton = pygame.font.Font(None, 48)
        self.fuente_error = pygame.font.Font(None, 28)

        # --- Input de nombre ---
        self.input_rect = pygame.Rect(
            self.ancho // 2 - 225,   # x
            self.altura // 2 - 180,  # y
            450,                     # ancho
            50                       # alto
        )
        self.nombre_texto = ""
        self.input_activo = False
        self.cursor_visible = True
        self.cursor_timer = 0

        # --- Selector de color tipo dropdown ---
        self.colores_disponibles = ['Amarillo', 'Azul', 'Verde', 'Rojo']
        self.map_color = {
            'Amarillo': (245, 223, 77),
            'Azul':     (66, 135, 245),
            'Verde':    (80, 200, 120),
            'Rojo':     (235, 75, 75)
        }
        self.color_actual = 0
        self.color_rect = pygame.Rect(
            self.ancho // 2 - 100,   # x
            self.altura // 2 - 100,  # y
            200,                     # ancho
            50                       # alto
        )
        self.dropdown_abierto = False
        self.altura_item = 40

        # --- Botón “¡JUGAR!” ---
        self.play_rect = pygame.Rect(
            self.ancho // 2 - 150,   # x
            self.altura // 2 +  20,  # y
            300,                     # ancho
            70                       # alto
        )

        # --- Mensaje de error ---
        self.mensaje_error = ""
        self.tiempo_error = 0

    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        self.tiempo_error = pygame.time.get_ticks()

    def procesar_eventos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            estaba_abierto = self.dropdown_abierto

            # 1) Click en el input de nombre
            if self.input_rect.collidepoint(mouse_pos):
                self.input_activo = True
            else:
                self.input_activo = False

            # 2) Si el dropdown estaba abierto antes de este click, comprobamos si clic en una opción
            if estaba_abierto:
                for idx, _ in enumerate(self.colores_disponibles):
                    item_rect = pygame.Rect(
                        self.color_rect.x,
                        self.color_rect.y + (idx + 1) * self.altura_item,
                        self.color_rect.width,
                        self.altura_item
                    )
                    if item_rect.collidepoint(mouse_pos):
                        self.color_actual = idx
                        break
                self.dropdown_abierto = False
                return None  # Evitar que el botón “¡JUGAR!” procese este mismo click

            # 3) Click en el rectángulo principal del dropdown
            if self.color_rect.collidepoint(mouse_pos):
                self.dropdown_abierto = not self.dropdown_abierto
                return None  # Ya manejamos el toggle, no verificamos “¡JUGAR!” en este click

            # 4) Si el dropdown está abierto ahora mismo (es decir, no había estado abierto y no hizo toggle aquí), no permitir “¡JUGAR!”
            if self.dropdown_abierto:
                return None

            # 5) Click en el botón “¡JUGAR!” (solo si dropdown cerrado)
            if self.play_rect.collidepoint(mouse_pos):
                if len(self.nombre_texto.strip()) > 0:
                    return {
                        'nombre': self.nombre_texto.strip(),
                        'color':  self.colores_disponibles[self.color_actual]
                    }
                else:
                    self.mostrar_error("Por favor ingresa tu nombre antes de jugar.")

        elif event.type == pygame.KEYDOWN and self.input_activo:
            if event.key == pygame.K_BACKSPACE:
                self.nombre_texto = self.nombre_texto[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                self.nombre_texto += event.unicode

        return None

    def actualizar(self, delta_time):
        # Cursor parpadeante
        self.cursor_timer += delta_time
        if self.cursor_timer >= 500:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

        # Limpiar mensaje de error después de 3 segundos
        if self.mensaje_error:
            if pygame.time.get_ticks() - self.tiempo_error > 3000:
                self.mensaje_error = ""

    def dibujar(self):
        # 1) Fondo
        self.pantalla.blit(self.fondo, (0, 0))

        # 2) Panel clarito semitransparente (casi blanco)
        #panel_surf = pygame.Surface((550, 380), pygame.SRCALPHA)
       # panel_surf.fill((255, 255, 255, 220))
        #panel_x = self.ancho // 2 - 275
        #panel_y = self.altura // 2 - 210
        #self.pantalla.blit(panel_surf, (panel_x, panel_y))

        # 3) Botón “¡JUGAR!” (se dibuja antes del dropdown)
        mouse_pos = pygame.mouse.get_pos()
        if self.play_rect.collidepoint(mouse_pos) and not self.dropdown_abierto:
            boton_color = (0, 122, 255)      # azul iOS al hover
            texto_color_boton = (255, 255, 255)
        else:
            boton_color = (0, 102, 204)
            texto_color_boton = (255, 255, 255)

        pygame.draw.rect(self.pantalla, boton_color, self.play_rect, border_radius=20)
        pygame.draw.rect(self.pantalla, (200, 200, 200), self.play_rect, 1, border_radius=20)

        texto_play = self.fuente_boton.render("¡JUGAR!", True, texto_color_boton)
        play_x = self.play_rect.x + (self.play_rect.width - texto_play.get_width()) // 2
        play_y = self.play_rect.y + (self.play_rect.height - texto_play.get_height()) // 2
        self.pantalla.blit(texto_play, (play_x, play_y))

        # 4) Cuadro de texto (input de nombre)
        if self.input_activo:
            borde_color = (0, 122, 255)
        else:
            borde_color = (200, 200, 200)

        pygame.draw.rect(self.pantalla, borde_color, self.input_rect, border_radius=20, width=1)
        pygame.draw.rect(self.pantalla, (245, 245, 245), self.input_rect.inflate(-2, -2), border_radius=20)

        if self.nombre_texto == "":
            placeholder_surf = self.fuente_input.render("ingresa tu nombre", True, (150, 150, 150))
            self.pantalla.blit(placeholder_surf, (self.input_rect.x + 10, self.input_rect.y + 12))
        else:
            texto_superficie = self.fuente_input.render(self.nombre_texto, True, (50, 50, 50))
            self.pantalla.blit(texto_superficie, (self.input_rect.x + 10, self.input_rect.y + 12))

        if self.input_activo and self.cursor_visible and self.nombre_texto:
            texto_superficie = self.fuente_input.render(self.nombre_texto, True, (50, 50, 50))
            cursor_x = self.input_rect.x + 10 + texto_superficie.get_width()
            cursor_y = self.input_rect.y + 12
            cursor_height = self.fuente_input.get_height()
            pygame.draw.line(self.pantalla, (50, 50, 50),
                             (cursor_x, cursor_y),
                             (cursor_x, cursor_y + cursor_height),
                             2)

        # 5) Selector de color (rectángulo “cerrado”)
        color_nombre = self.colores_disponibles[self.color_actual]
        color_rgb = self.map_color[color_nombre]
        pygame.draw.rect(self.pantalla, color_rgb, self.color_rect, border_radius=20)
        pygame.draw.rect(self.pantalla, (200, 200, 200), self.color_rect, 1, border_radius=20)

        texto_color = self.fuente_input.render(color_nombre, True, (0, 0, 0))
        txt_x = self.color_rect.x + (self.color_rect.width - texto_color.get_width()) // 2
        txt_y = self.color_rect.y + (self.color_rect.height - texto_color.get_height()) // 2
        self.pantalla.blit(texto_color, (txt_x, txt_y))

        # 6) Dropdown abierto: siempre encima de todo
        if self.dropdown_abierto:
            for idx, nombre in enumerate(self.colores_disponibles):
                item_rect = pygame.Rect(
                    self.color_rect.x,
                    self.color_rect.y + (idx + 1) * self.altura_item,
                    self.color_rect.width,
                    self.altura_item
                )
                pygame.draw.rect(self.pantalla, (255, 255, 255), item_rect, border_radius=20)
                pygame.draw.rect(self.pantalla, (200, 200, 200), item_rect, 1, border_radius=20)

                texto_item = self.fuente_input.render(nombre, True, (50, 50, 50))
                text_x = item_rect.x + 10
                text_y = item_rect.y + (self.altura_item - texto_item.get_height()) // 2
                self.pantalla.blit(texto_item, (text_x, text_y))

        # 7) Mensaje de error
        if self.mensaje_error:
            texto_err = self.fuente_error.render(self.mensaje_error, True, (255, 59, 48))
            err_x = self.ancho // 2 - texto_err.get_width() // 2
            err_y = self.altura // 2 + 110
            self.pantalla.blit(texto_err, (err_x, err_y))
