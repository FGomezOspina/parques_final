import pygame
import pygame_gui
from jugador import Jugador
from tablero import Tablero
from network import Network
from menu_inicio import MenuInicio

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
pantalla = pygame.display.set_mode((900, 720))
pygame.display.set_caption("Parqués")

# Cargar sprites
sprite_tablero_amarillo = pygame.image.load("Sprites/Tablero_amarillo.jpeg")
sprite_tablero_amarillo = pygame.transform.scale(sprite_tablero_amarillo, (720, 720))

sprite_tablero_azul = pygame.image.load("Sprites/Tablero_azul.jpeg")
sprite_tablero_azul = pygame.transform.scale(sprite_tablero_azul, (720, 720))

sprite_tablero_verde = pygame.image.load("Sprites/Tablero_verde.jpeg")
sprite_tablero_verde = pygame.transform.scale(sprite_tablero_verde, (720, 720))

sprite_tablero_rojo = pygame.image.load("Sprites/Tablero_rojo.jpeg")
sprite_tablero_rojo = pygame.transform.scale(sprite_tablero_rojo, (720, 720))


sprite_dado0 = pygame.image.load("Sprites/Dado0.png")
sprite_dado1 = pygame.image.load("Sprites/Dado1.png")
sprite_dado2 = pygame.image.load("Sprites/Dado2.png")
sprite_dado3 = pygame.image.load("Sprites/Dado3.png")
sprite_dado4 = pygame.image.load("Sprites/Dado4.png")
sprite_dado5 = pygame.image.load("Sprites/Dado5.png")
sprite_dado6 = pygame.image.load("Sprites/Dado6.png")

dados = [sprite_dado0, sprite_dado1, sprite_dado2, sprite_dado3, sprite_dado4, sprite_dado5, sprite_dado6]
Pintar = True

pantalla.fill((255, 255, 255))
pantalla.blit(sprite_dado0, (736, 640))
pantalla.blit(sprite_dado0, (816, 640))

def redraw_window(pantalla, jugador, otros_jugadores, mensaje, fuente_mensajes):
    global Pintar
    if Pintar:
        pantalla.fill((255, 255, 255))
        Pintar = False

    # Limpiar zona derecha donde van botones/mensajes
    pygame.draw.rect(pantalla, (255, 255, 255), (720, 0, 180, 300))

    # Dibuja el tablero según el color del jugador
    if jugador.color == "Amarillo":
        pantalla.blit(sprite_tablero_amarillo, (0, 0))
    elif jugador.color == "Azul":
        pantalla.blit(sprite_tablero_azul, (0, 0))
    elif jugador.color == "Verde":
        pantalla.blit(sprite_tablero_verde, (0, 0))
    elif jugador.color == "Rojo":
        pantalla.blit(sprite_tablero_rojo, (0, 0))

    # Dados del jugador
    pantalla.blit(dados[jugador.dados[0]], (736, 640))
    pantalla.blit(dados[jugador.dados[1]], (816, 640))

    # Si todos están listos y el jugador también, dibujamos un subtítulo fijo:
    total_jugadores = len(otros_jugadores) + 1
    jugadores_listos = len([j for j in otros_jugadores if j.estado == "listo"]) + (1 if jugador.estado == "listo" else 0)
    if total_jugadores >= 2 and jugadores_listos == total_jugadores and jugador.estado == "listo":
        subtitulo = pygame.font.Font(None, 48).render("¡Listos para jugar!", True, (0, 0, 0))
        pantalla.blit(subtitulo, (200, 75))

    # Dibujar fichas y nombres
    jugador.actualizar_en_pantalla(pantalla, jugador.color)
    jugador.dibujar_nombre(pantalla, jugador.color)
    for otro_jugador in otros_jugadores:
        if otro_jugador.color != jugador.color:
            otro_jugador.actualizar_en_pantalla(pantalla, jugador.color)
            otro_jugador.dibujar_nombre(pantalla, jugador.color)

    # Dibujar mensaje si existe
    if mensaje is not None:
        texto_surf = fuente_mensajes.render(mensaje, True, (0, 0, 0))
        rect_texto = texto_surf.get_rect(center=(pantalla.get_width() // 2, 60))
        pantalla.blit(texto_surf, rect_texto)

def menu_principal(network):
    menu = MenuInicio(pantalla)
    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            resultado = menu.procesar_eventos(event)
            if resultado:
                # Intentar establecer el color seleccionado
                jugador_temp = Jugador(resultado['nombre'], resultado['color'], [0, 0, 0, 0])
                try:
                    response = network.send(jugador_temp)
                    if isinstance(response, dict) and "error" in response:
                        menu.mostrar_error(response["error"])
                        pygame.display.update()
                        pygame.time.wait(5000)  # Esperar 5 segundos antes de cerrar
                        return None
                    else:
                        jugadores = response
                        for j in jugadores:
                            if j.color == resultado['color'] and j.nombre == resultado['nombre']:
                                return resultado
                        menu.mostrar_error(f"El color {resultado['color']} ya está en uso")
                except Exception as e:
                    print(f"Error al verificar color: {e}")
                    menu.mostrar_error("Error de conexión")

        menu.actualizar(time_delta)
        menu.dibujar()
        pygame.display.update()


def main():
    running = True
    try:
        n = Network()
        jugador_inicial = n.get_p()
        if not jugador_inicial:
            print("No se pudo conectar al servidor")
            return

        datos_jugador = menu_principal(n)
        if not datos_jugador:
            return

        jugador = Jugador(datos_jugador['nombre'], datos_jugador['color'], [0, 0, 0, 0])

        manager = pygame_gui.UIManager((900, 720))
        boton_listo = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((750, 550), (100, 50)),
            text='Listo',
            manager=manager
        )

        boton_tirar_dado = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((750, 550), (100, 50)),
            text='Tirar Dado',
            manager=manager
        )
        boton_tirar_dado.hide()

        boton_mover_ficha_1_1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((750, 385), (100, 50)),
            text='Mover #',
            manager=manager
        )
        boton_mover_ficha_1_1.hide()

        boton_mover_ficha_1_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((750, 440), (100, 50)),
            text='Mover #',
            manager=manager
        )
        boton_mover_ficha_1_2.hide()

        boton_mover_ficha_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((750, 495), (100, 50)),
            text='Mover #',
            manager=manager
        )
        boton_mover_ficha_2.hide()

        boton_sacar_ficha = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((750, 550), (100, 50)),
            text='Sacar Ficha',
            manager=manager
        )
        boton_sacar_ficha.hide()

        boton_sacar_ficha_carcel = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((750, 550), (100, 50)),
            text='Sacar Ficha de la Cárcel',
            manager=manager
        )
        boton_sacar_ficha_carcel.hide()

        clock = pygame.time.Clock()
        partida_iniciada = False
        countdown = None
        tiempo_inicio = None

        # Fuente para mensajes
        fuente_mensajes = pygame.font.Font(None, 40)
        mensaje_actual = None

        while running:
            time_delta = clock.tick(60) / 1000.0

            try:
                jugadores = n.send(jugador)
                # Si los dados cambiaron en el servidor, actualizar localmente
                if jugadores is not None:
                    for otro in jugadores:
                        if otro.color == jugador.color and otro.actualizar:
                            jugador.dados = otro.dados
                            jugador.estado = otro.estado
                            jugador.turno = otro.turno
                            jugador.fichas = otro.fichas
                            jugador.intentos_par = otro.intentos_par
                            jugador.accion = None
                            jugador.actualizar = False
                            jugador.tiros_dados = otro.tiros_dados
                            jugador.seleccionada = otro.seleccionada
                            jugador.movimiento_restante = otro.movimiento_restante
                            break

                # Lógica de estado de partida
                total_jugadores = len(jugadores)
                jugadores_listos = len([j for j in jugadores if j.estado == "listo"])

                # Mostrar/ocultar botón de tirar dados en "definiendo_turno" y "jugando"
                if jugador.estado == "jugando" and jugador.turno:
                    if jugador.fichas == [0, 0, 0, 0] and jugador.intentos_par < 3:
                        boton_tirar_dado.show()
                    elif jugador.fichas != [0, 0, 0, 0]:
                        boton_mover_ficha_1_1.set_text(f"Mover {jugador.movimiento_restante[0]}")
                        boton_mover_ficha_1_2.set_text(f"Mover {jugador.movimiento_restante[1]}")
                        boton_mover_ficha_2.set_text(f"Mover {jugador.movimiento_restante[0] + jugador.movimiento_restante[1]}")

                        # Si alguna ficha está en posición 0 y hay intentos
                        if 0 in jugador.fichas and jugador.intentos_par > 0 and jugador.tiros_dados == 1:
                            boton_sacar_ficha_carcel.show()
                        else:
                            boton_sacar_ficha_carcel.hide()
                            pygame.draw.rect(pantalla, (255, 255, 255), (750, 550, 100, 50))

                        if jugador.tiros_dados == 0:
                            boton_tirar_dado.show()
                        else:
                            boton_tirar_dado.hide()
                            boton_mover_ficha_1_1.show()
                            boton_mover_ficha_1_2.show()
                            boton_mover_ficha_2.show()
                            pygame.draw.rect(pantalla, (255, 255, 255), (750, 550, 100, 50))

                        if jugador.movimiento_restante[0] == 0:
                            boton_mover_ficha_1_1.hide()
                            boton_mover_ficha_2.hide()
                            pygame.draw.rect(pantalla, (255, 255, 255), (750, 385, 100, 50))
                            pygame.draw.rect(pantalla, (255, 255, 255), (750, 495, 100, 50))
                        else:
                            boton_mover_ficha_1_1.show()

                        if jugador.movimiento_restante[1] == 0:
                            boton_mover_ficha_1_2.hide()
                            boton_mover_ficha_2.hide()
                            pygame.draw.rect(pantalla, (255, 255, 255), (750, 440, 100, 110))
                        else:
                            boton_mover_ficha_1_2.show()

                        if jugador.movimiento_restante == [0, 0] and jugador.movimiento_restante[0] + jugador.movimiento_restante[1] == 0:
                            boton_mover_ficha_1_1.hide()
                            boton_mover_ficha_1_2.hide()
                            boton_mover_ficha_2.hide()
                            pygame.draw.rect(pantalla, (255, 255, 255), (750, 385, 100, 160))

                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        sprite_ficha_width = 32
                        sprite_ficha_height = 32

                        for indice_ficha, posicion_casilla in enumerate(jugador.fichas):
                            coordenadas = Tablero().obtener_posicion(posicion_casilla, indice_ficha, 0)
                            if pygame.mouse.get_pressed()[0] and coordenadas and coordenadas[0] <= mouse_x <= coordenadas[0] + sprite_ficha_width and coordenadas[1] <= mouse_y <= coordenadas[1] + sprite_ficha_height:
                                jugador.accion = "seleccionar_ficha"
                                jugador.seleccionada = indice_ficha
                                break
                    else:
                        boton_tirar_dado.hide()
                        pygame.draw.rect(pantalla, (255, 255, 255), (750, 550, 100, 50))
                elif jugador.estado == "jugando" and not jugador.turno:
                    boton_tirar_dado.hide()
                    pygame.draw.rect(pantalla, (255, 255, 255), (750, 550, 100, 50))
                elif jugador.estado == "escoja_ficha":
                    boton_tirar_dado.hide()
                    boton_mover_ficha_1_1.hide()
                    boton_mover_ficha_1_2.hide()
                    boton_mover_ficha_2.hide()
                    boton_sacar_ficha.show()
                    pygame.draw.rect(pantalla, (255, 255, 255), (750, 385, 100, 160))
                    pygame.draw.rect(pantalla, (255, 255, 255), (750, 440, 100, 110))
                    pygame.draw.rect(pantalla, (255, 255, 255), (750, 495, 100, 50))

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    sprite_ficha_width = 32
                    sprite_ficha_height = 32
                    for indice_ficha, posicion_casilla in enumerate(jugador.fichas):
                        coordenadas = Tablero().obtener_posicion(posicion_casilla, indice_ficha, 0)
                        if pygame.mouse.get_pressed()[0] and coordenadas and coordenadas[0] <= mouse_x <= coordenadas[0] + sprite_ficha_width and coordenadas[1] <= mouse_y <= coordenadas[1] + sprite_ficha_height:
                            jugador.accion = "seleccionar_ficha"
                            jugador.seleccionada = indice_ficha
                            break

                # Esconder el botón de sacar ficha después de sacar una ficha
                if jugador.estado == "jugando" and jugador.seleccionada is None:
                    boton_sacar_ficha.hide()

                # Si todos están listos pero la partida no ha iniciado
                if total_jugadores >= 2 and jugadores_listos == total_jugadores and not partida_iniciada:
                    if countdown is None:
                        countdown = 3
                        tiempo_inicio = pygame.time.get_ticks()

                    tiempo_actual = pygame.time.get_ticks()
                    if tiempo_inicio is not None:
                        tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / 1000
                        countdown = 3 - int(tiempo_transcurrido)

                        if countdown <= 0:
                            partida_iniciada = True
                            jugador.accion = "definiendo_turno"
                            boton_listo.hide()
                            boton_tirar_dado.show()
                            print("Iniciando partida...")

                # 1) Determinar qué mensaje mostrar (o ninguno) en función del estado:
                if jugador.estado.startswith("Ganador:"):
                    mensaje_actual = jugador.estado
                elif jugador.estado == "definiendo_turno":
                    mensaje_actual = "¡Tira los dados para determinar el orden!"
                elif jugador.estado == "esperando_orden":
                    mensaje_actual = f"Esperando a que todos tiren... Tu valor: {sum(jugador.dados)}"
                elif jugador.estado == "jugando":
                    if jugador.turno:
                        if all(ficha == 0 for ficha in jugador.fichas):
                            mensaje_actual = f"Tu turno - Intento {jugador.intentos_par}/3 para sacar par"
                        elif jugador.tiros_dados == 0:
                            mensaje_actual = "¡Tu turno! Tira los dados para mover"
                        elif jugador.tiros_dados == 1 and jugador.seleccionada is None:
                            mensaje_actual = "Selecciona una ficha para mover"
                        elif jugador.tiros_dados == 1 and jugador.seleccionada is not None:
                            mensaje_actual = "Selecciona cuántas casillas mover"
                        else:
                            mensaje_actual = "Moviendo ficha..."
                    else:
                        mensaje_actual = "Esperando tu turno..."
                elif jugador.estado == "escoja_ficha":
                    if jugador.seleccionada is None:
                        mensaje_actual = "Selecciona una ficha para sacar"
                    else:
                        mensaje_actual = f"Ficha seleccionada, sacará la ficha {jugador.seleccionada + 1}"
                else:
                    mensaje_actual = None

                # 2) Llamar a redraw_window con el mensaje
                redraw_window(pantalla, jugador, jugadores, mensaje_actual, fuente_mensajes)

                # 3) Si ya hay un ganador, esperamos 5 segundos y salimos
                if jugador.estado.startswith("Ganador:"):
                    pygame.time.wait(5000)
                    running = False

            except Exception as e:
                print(f"Error de conexión: {e}")
                running = False
                break

            # Procesar eventos (botones y demás)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    

                # Aquí imprimimos en terminal la posición del mouse cuando se mueva
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    print(f"Coordenadas mouse: ({x}, {y})")


                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == boton_listo and not partida_iniciada:
                            if jugador.estado == "listo":
                                jugador.accion = "no_listo"
                                boton_listo.set_text("Listo")
                            else:
                                jugador.accion = "listo"
                                boton_listo.set_text("No listo")
                            print(f"Jugador {jugador.color} - Acción: {jugador.accion}")

                        elif event.ui_element == boton_tirar_dado and jugador.estado == "definiendo_turno":
                            jugador.accion = "tirar_dados_turno"
                            boton_tirar_dado.hide()
                            pygame.draw.rect(pantalla, (255, 255, 255), (750, 550, 100, 50))

                        elif event.ui_element == boton_tirar_dado and jugador.estado == "jugando" and jugador.turno:
                            print("Tirando dados...")
                            jugador.accion = "tirar_dados"
                            boton_tirar_dado.hide()

                        elif event.ui_element == boton_mover_ficha_1_1 and jugador.estado == "jugando" and jugador.turno:
                            print("moviendo ficha con el dado 1")
                            jugador.accion = "mover_ficha_1_1"
                            jugador.movimiento_restante[0] = 0

                        elif event.ui_element == boton_mover_ficha_1_2 and jugador.estado == "jugando" and jugador.turno:
                            print("moviendo ficha con el dado 2")
                            jugador.accion = "mover_ficha_1_2"
                            jugador.movimiento_restante[1] = 0

                        elif event.ui_element == boton_mover_ficha_2 and jugador.estado == "jugando" and jugador.turno:
                            print("moviendo ficha con el dado 1 y 2")
                            jugador.accion = "mover_ficha_2"
                            jugador.movimiento_restante = [0, 0]

                        elif event.ui_element == boton_sacar_ficha and jugador.estado == "escoja_ficha":
                            print("sacando ficha")
                            jugador.accion = "sacar_ficha"
                            boton_sacar_ficha.hide()
                            mensaje_actual = None

                        elif event.ui_element == boton_sacar_ficha_carcel and jugador.estado == "jugando":
                            print("sacando ficha de la cárcel")
                            jugador.accion = "sacar_ficha_carcel"
                            jugador.movimiento_restante = [0, 0]

                manager.process_events(event)

            manager.update(time_delta)
            manager.draw_ui(pantalla)

            # Solo una llamada a pygame.display.update() por fotograma
            pygame.display.update()

    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
