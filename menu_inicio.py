import pygame
import pygame_gui

class MenuInicio:
    def __init__(self, pantalla):
        self.ancho = 900
        self.altura = 720
        self.pantalla = pantalla
        self.manager = pygame_gui.UIManager((self.ancho, self.altura))
        
        # Cargar la imagen de fondo
        self.fondo = pygame.image.load('sprites/fondomenu.jpg')
        self.fondo = pygame.transform.scale(self.fondo, (self.ancho, self.altura))  # Ajustar la imagen al tamaño de la pantalla
        
        # Cargar la imagen del título
        self.titulo_imagen = pygame.image.load('sprites/titulo.png')
        self.titulo_imagen = pygame.transform.scale(self.titulo_imagen, (400, 100))  # Ajustar tamaño si es necesario
        
        # Crear elementos de la interfaz
        self.nombre_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((350, 200), (200, 30)),
            manager=self.manager,
        )
        
        self.colores_disponibles = ['Amarillo', 'Azul', 'Verde', 'Rojo']
        self.color_actual = 0
        
        self.color_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 250), (200, 30)),
            text=self.colores_disponibles[self.color_actual],
            manager=self.manager
        )
        
        self.jugar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 300), (200, 50)),
            text='¡JUGAR!',
            manager=self.manager
        )
        
        self.mensaje_error = None
        self.tiempo_error = 0
    
    def mostrar_error(self, mensaje):
        self.mensaje_error = mensaje
        self.tiempo_error = pygame.time.get_ticks()
    
    def procesar_eventos(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.color_button:
                    # Cambiar al siguiente color disponible
                    self.color_actual = (self.color_actual + 1) % len(self.colores_disponibles)
                    self.color_button.set_text(self.colores_disponibles[self.color_actual])
                
                elif event.ui_element == self.jugar_button:
                    # Validar que se haya ingresado un nombre
                    if len(self.nombre_input.get_text()) > 0:
                        return {
                            'nombre': self.nombre_input.get_text(),
                            'color': self.colores_disponibles[self.color_actual]
                        }
                    else:
                        self.mostrar_error("Por favor ingrese un nombre")
        
        self.manager.process_events(event)
        return None
    
    def actualizar(self, delta_time):
        self.manager.update(delta_time)
        
        # Borrar mensaje de error después de 3 segundos
        if self.mensaje_error and pygame.time.get_ticks() - self.tiempo_error > 3000:
            self.mensaje_error = None
    
    def dibujar(self):
        self.pantalla.blit(self.fondo, (0, 0))  # Fondo blanco
        
        # Dibujar imagen título
        self.pantalla.blit(self.titulo_imagen, (250, 50))
        
        # Dibujar mensaje de error si existe
        if self.mensaje_error:
            fuente_error = pygame.font.Font(None, 32)
            texto_error = fuente_error.render(self.mensaje_error, True, (255, 0, 0))
            self.pantalla.blit(texto_error, (300, 400))
        
        self.manager.draw_ui(self.pantalla)