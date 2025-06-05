import socket
import pickle
from _thread import *
from jugador import Jugador
import random
import time
import os

server = "0.0.0.0"
port = int(os.getenv("PORT", 5555))  # Usar el puerto asignado por Render, o 5555 como predeterminado

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Estados del juego
GAME_STATES = {
    "WAITING_PLAYERS": "waiting_players",
    "ROLLING_FOR_TURNS": "rolling_for_turns",
    "PLAYING": "playing"
}

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(4)
print("Waiting for a connection, Server Started")

# Inicializar array de jugadores y estado del juego
players = [None] * 4  # [Amarillo, Azul, Verde, Rojo]
game_state = GAME_STATES["WAITING_PLAYERS"]
turn_order = []  # Lista que mantendrá el orden de los turnos
current_turn_index = 0

color_to_index = {
    "Amarillo": 0,
    "Azul": 1,
    "Verde": 2,
    "Rojo": 3,
    "":-1
}
conexiones = {}

def get_player_index(color):
    return color_to_index[color]

def tirar_dados():
    return [random.randint(1, 6), random.randint(1, 6)]

'''def tirar_dados():
    return [6, 6]'''

def calcular_valor_dados(dados):
    return dados[0] + dados[1]

def get_jugadores_activos():
    """Retorna la lista de jugadores activos en el orden correcto"""
    return [p for p in players if p is not None]

def determinar_orden_turnos(jugadores):
    valores_dados = []
    for i, jugador in enumerate(jugadores):
        if jugador is not None:
            valor = calcular_valor_dados(jugador.dados)
            valores_dados.append((i, valor))
    valores_dados.sort(key=lambda x: x[1], reverse=True)
    return [idx for idx, _ in valores_dados]

def broadcast_game_state():
    """Envía el estado actual del juego a todos los jugadores conectados"""
    jugadores_activos = get_jugadores_activos()
    print("Broadcasting estado del juego:")
    for jugador in jugadores_activos:
        print(f"{jugador.color}: {jugador.estado}")
        print(f"Fichas: {jugador.fichas}")
        jugador.actualizar=True
    
    for conn in conexiones.values():
        try:
            conn.sendall(pickle.dumps(jugadores_activos))
        except Exception as e:
            print(f"Error al enviar estado: {e}")

def update_player_state(player_index, new_state, broadcast=True):
    """Actualiza el estado de un jugador y opcionalmente hace broadcast"""
    if players[player_index] is not None:
        players[player_index].estado = new_state
        if broadcast:
            broadcast_game_state()

def check_all_players_rolled():
    """Verifica si todos los jugadores han tirado los dados"""
    jugadores_activos = get_jugadores_activos()
    return all(p.estado == "esperando_orden" for p in jugadores_activos)

def check_winner():
    for player in players:
        if player is not None and all(ficha == 72 for ficha in player.fichas):
            return player.color
        elif player is not None:
            print(f"Jugador {player.color} no ha ganado, tiene las fichas en {player.fichas}")
    return None

def comer_ficha(player_index, ficha_seleccionada):
    """Lógica para comer fichas de otros jugadores"""
    casillas_seguro =[8,13,25,30,42,47,59,64,65,66,67,68,69,70,71,72]
    casillas_salidas = [1,18,35,52]

    print("Hola!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"Posición de la ficha: {players[player_index].fichas[ficha_seleccionada]}")
    for i, player in enumerate(players):
        if i != player_index and player is not None:
            for j, ficha in enumerate(player.fichas):
                # Verifica que la posición no sea la inicial o las casillas de seguro
                if ficha != 0 and ficha != 72 and ficha not in casillas_seguro and ficha not in casillas_salidas:
                    if player_index == 0:
                        if player.color == 'Azul':
                            ficha_corregida = ficha + 17
                        elif player.color == 'Verde':
                            ficha_corregida = ficha + 34
                        elif player.color == 'Rojo':
                            ficha_corregida = ficha + 51
                    elif player_index == 1:
                        if player.color == 'Verde':
                            ficha_corregida = ficha + 17
                        elif player.color == 'Rojo':
                            ficha_corregida = ficha + 34
                        elif player.color == 'Amarillo':
                            ficha_corregida = ficha + 51
                    elif player_index == 2:
                        if player.color == 'Rojo':
                            ficha_corregida = ficha + 17
                        elif player.color == 'Amarillo':
                            ficha_corregida = ficha + 34
                        elif player.color == 'Azul':
                            ficha_corregida = ficha + 51
                    elif player_index == 3:
                        if player.color == 'Amarillo':
                            ficha_corregida = ficha + 17
                        elif player.color == 'Azul':
                            ficha_corregida = ficha + 34
                        elif player.color == 'Verde':
                            ficha_corregida = ficha + 51

                    if ficha_corregida == 65:
                        ficha_corregida = 73
                    elif ficha_corregida == 66:
                        ficha_corregida = 74
                    elif ficha_corregida == 67:
                        ficha_corregida = 75
                    elif ficha_corregida == 68:
                        ficha_corregida = 76
                    elif ficha_corregida >= 69:
                        ficha_corregida -= 68

                    
                    if ficha_corregida == players[player_index].fichas[ficha_seleccionada]:
                        print(f"Ficha del jugador {player.color} en la posición {ficha_corregida} fue comida")
                        player.fichas[j] = 0
                        return True
                    else:
                        print(f"Ficha del jugador {player.color} en la posición {ficha_corregida} no fue comida")

    
    return False  # No se comió ninguna ficha

def threaded_client(conn, addr):
    global game_state, turn_order, current_turn_index, players
    
    try:
        if game_state != GAME_STATES["WAITING_PLAYERS"]:
            conn.send(pickle.dumps({"error": "El juego ya ha iniciado, no te puedes unir"}))
            conn.close()
            return
        
        initial_player = Jugador("", "", [0, 0, 0, 0])
        conn.send(pickle.dumps(initial_player))
        
        player_index = None
        
        while True:
            try:
                full_data = b''
                while True:
                    part = conn.recv(2048)
                    if not part:

                        raise ConnectionError("Cliente desconectado")
                    full_data += part
                    if len(part) < 2048:
                        break
                
                data = pickle.loads(full_data)
                
                if not data:
                    break
            
                # Manejo de conexión inicial y asignación de color
                if player_index is None or players[player_index] is None or players[player_index].color != data.color:
                    new_index = get_player_index(data.color)
                    
                    if players[new_index] is not None and players[new_index].color == data.color:
                        conn.sendall(pickle.dumps(get_jugadores_activos()))
                        continue
                    
                    if player_index is not None:
                        players[player_index] = None
                    
                    player_index = new_index
                    players[player_index] = data
                    conexiones[player_index] = conn
                    
                    print(f"Jugador asignado a la posición {player_index} con color {data.color}")

                # Manejar estados del juego
                jugadores_conectados = get_jugadores_activos()
                
                if game_state == GAME_STATES["WAITING_PLAYERS"]:
                    if data.accion == "listo" and data.estado == "esperando":
                        print(f"Jugador {player_index} listo")
                        players[player_index].estado = "listo"
                    elif data.accion == "no_listo" and data.estado == "listo":
                        print(f"Jugador {player_index} no listo")
                        players[player_index].estado = "esperando"
                    broadcast_game_state()

                    if len(jugadores_conectados) >= 2 and all(j.estado == "listo" for j in jugadores_conectados) and data.accion == "definiendo_turno":
                        game_state = GAME_STATES["ROLLING_FOR_TURNS"]
                        for player in players:
                            if player is not None:
                                print(f"Actualizando estado de {player.color} a definiendo_turno")
                                player.estado = "definiendo_turno"
                        broadcast_game_state()
                
                elif game_state == GAME_STATES["ROLLING_FOR_TURNS"]:

                    if data.accion == "tirar_dados_turno" and data.estado == "definiendo_turno":
                        nuevos_dados = tirar_dados()
                        players[player_index].dados = nuevos_dados
                        players[player_index].estado = "esperando_orden"
                        players[player_index].accion = None

                        print(f"\nJugador {players[player_index].color} tiró los dados")
                        print(f"Estado actualizado a: {players[player_index].estado}")
                        broadcast_game_state()

                        if check_all_players_rolled():
                            #Simular espera de 2 segundos
                            time.sleep(2)
                            turn_order = determinar_orden_turnos(players)
                            game_state = GAME_STATES["PLAYING"]
                            current_turn_index = 0
                            
                            # Asegurar que todos los estados se actualizan correctamente
                            for i, player_idx in enumerate(turn_order):
                                if players[player_idx] is not None:
                                    players[player_idx].estado = "jugando"
                                    players[player_idx].turno = (i == 0)
                                    players[player_idx].intentos_par = 0
                                    print(f"Jugador {players[player_idx].color} estado actualizado a: {players[player_idx].estado}")
                        
                        broadcast_game_state()

                elif game_state == GAME_STATES["PLAYING"]:
                    # Verificar si es el turno del jugador actual y si realizó la acción de tirar dados
                    if (player_index == turn_order[current_turn_index] and data.accion == "tirar_dados"):
                        # Si el jugador tiene todas las fichas en la cárcel y no ha agotado sus intentos
                        if all(ficha == 0 for ficha in players[player_index].fichas) and players[player_index].intentos_par < 3:
                            nuevos_dados = tirar_dados()
                            players[player_index].intentos_par += 1
                            players[player_index].dados = nuevos_dados
                            players[player_index].accion = None

                            print(f"\nJugador {players[player_index].color} tiró los dados")
                            print(f"Dados: {nuevos_dados}")
                            print(f"Intentos de sacar par: {players[player_index].intentos_par}")
                            

                            # Si saca par, libera las fichas
                            if nuevos_dados[0] == nuevos_dados[1]:
                                players[player_index].intentos_par = 0
                                players[player_index].fichas = [1, 1, 1, 1]
                                players[player_index].dados = [0, 0]
                                print("¡Par! Fichas liberadas")
                            
                            # Si agotó los intentos, cambiar turno
                            if players[player_index].intentos_par >= 3 and not any(players[player_index].fichas):
                                print("Cambio de turno por agotar intentos")
                                current_turn_index = (current_turn_index + 1) % len(turn_order)
                                players[player_index].turno = False
                                players[player_index].intentos_par = 0
                                players[player_index].dados = [0, 0]
                                if players[turn_order[current_turn_index]] is not None:
                                    players[turn_order[current_turn_index]].turno = True
                            
                            broadcast_game_state()
                        # Si ya tiene fichas fuera de la cárcel
                        elif any(ficha != 0 for ficha in players[player_index].fichas) and players[player_index].tiros_dados == 0:
                            nuevos_dados = tirar_dados()
                            if nuevos_dados[0] == nuevos_dados[1]:
                                players[player_index].intentos_par += 1
                                print(f'Sacó par {players[player_index].intentos_par} veces')
                            else:
                                print(nuevos_dados)
                                players[player_index].intentos_par = 0
                            if players[player_index].intentos_par == 3:
                                players[player_index].intentos_par = 0
                                players[player_index].estado = "escoja_ficha"
                            players[player_index].dados = nuevos_dados
                            players[player_index].movimiento_restante = nuevos_dados
                            players[player_index].accion = None
                            players[player_index].tiros_dados = 1
                            print(f"\nJugador {players[player_index].color} tiró los dados")
                            print(f"Dados: {nuevos_dados}")

                            broadcast_game_state()
                    # Si va a sacar una ficha de la cárcel
                    elif (player_index == turn_order[current_turn_index] and data.accion == "sacar_ficha_carcel"):
                        for i, ficha in enumerate(players[player_index].fichas):
                            if ficha == 0:
                                players[player_index].fichas[i] = 1
                                print(f"Jugador {players[player_index].color} sacó la ficha {i} de la cárcel")
                                break
                        players[player_index].estado = "jugando"
                        players[player_index].seleccionada = None
                        players[player_index].accion = None
                        players[player_index].movimiento_restante = [0, 0]
                        players[player_index].dados = [0, 0]
                        broadcast_game_state()

                    # Si va a mover una ficha
                    elif (player_index == turn_order[current_turn_index] and data.accion == "seleccionar_ficha"):
                        if players[player_index].fichas[data.seleccionada] != 72 and players[player_index].fichas[data.seleccionada] != 0:
                            players[player_index].seleccionada = data.seleccionada
                            print(f"Jugador {players[player_index].color} seleccionó la ficha {data.seleccionada}")
                    
                    elif (player_index == turn_order[current_turn_index] and players[player_index].estado == "escoja_ficha" and data.accion == "sacar_ficha"):
                        ficha_seleccionada = players[player_index].seleccionada
                        if ficha_seleccionada is not None:
                            players[player_index].fichas[ficha_seleccionada] = 72  # Mueve la ficha a la casilla final
                            players[player_index].estado = "jugando"
                            players[player_index].seleccionada = None
                            players[player_index].intentos_par = 0
                            players[player_index].tiros_dados = 1
                            players[player_index].movimiento_restante = [0, 0]

                    elif (player_index == turn_order[current_turn_index] and data.accion == "mover_ficha_1_1"):
                        ficha_seleccionada = players[player_index].seleccionada
                        if ficha_seleccionada is not None:
                            nueva_posicion = players[player_index].fichas[ficha_seleccionada] + players[player_index].movimiento_restante[0]
                            if nueva_posicion <= 72 or (players[player_index].fichas[ficha_seleccionada] >= 65 and nueva_posicion >= 72):
                                print(f"Jugador {players[player_index].color} mueve la ficha {ficha_seleccionada} con el valor de un solo dado {players[player_index].dados[0]}")
                                # Lógica para mover la ficha
                                players[player_index].seleccionada = None
                                players[player_index].accion = None
                                players[player_index].fichas[ficha_seleccionada] = min(nueva_posicion, 72)
                                comer_ficha(player_index, ficha_seleccionada)
                                players[player_index].historial_movimientos.append(ficha_seleccionada)
                                players[player_index].movimiento_restante[0] = 0
                                players[player_index].dados[0] = 0
                                broadcast_game_state()
                            else:
                                print(f"Jugador {players[player_index].color} no puede mover la ficha {ficha_seleccionada} con el valor de un solo dado {players[player_index].dados[0]}")
                        else:
                            print(f"Jugador {players[player_index].color} no ha seleccionado una ficha")
                    
                    elif (player_index == turn_order[current_turn_index] and data.accion == "mover_ficha_1_2"):
                        ficha_seleccionada = players[player_index].seleccionada
                        if ficha_seleccionada is not None:
                            nueva_posicion = players[player_index].fichas[ficha_seleccionada] + players[player_index].movimiento_restante[1]
                            if nueva_posicion <= 72 or (players[player_index].fichas[ficha_seleccionada] >= 65 and nueva_posicion >= 72):
                                print(f"Jugador {players[player_index].color} mueve la ficha {ficha_seleccionada} con el valor de un solo dado {players[player_index].dados[1]}")
                                # Lógica para mover la ficha
                                players[player_index].seleccionada = None
                                players[player_index].accion = None
                                players[player_index].fichas[ficha_seleccionada] = min(nueva_posicion, 72)
                                comer_ficha(player_index, ficha_seleccionada)
                                players[player_index].historial_movimientos.append(ficha_seleccionada)
                                players[player_index].movimiento_restante[1] = 0
                                players[player_index].dados[1] = 0
                                broadcast_game_state()
                            else:
                                print(f"Jugador {players[player_index].color} no puede mover la ficha {ficha_seleccionada} con el valor de un solo dado {players[player_index].dados[1]}")
                        else:
                            print(f"Jugador {players[player_index].color} no ha seleccionado una ficha")

                    elif (player_index == turn_order[current_turn_index] and data.accion == "mover_ficha_2"):
                        ficha_seleccionada = players[player_index].seleccionada
                        if ficha_seleccionada is not None:
                            nueva_posicion = players[player_index].fichas[ficha_seleccionada] + sum(players[player_index].movimiento_restante)
                            if nueva_posicion <= 72 or (players[player_index].fichas[ficha_seleccionada] >= 65 and nueva_posicion >= 72):
                                print(f"Jugador {players[player_index].color} mueve la ficha {ficha_seleccionada} con el valor de dos dados {sum(players[player_index].dados)}")
                                # Lógica para mover la ficha
                                players[player_index].seleccionada = None
                                players[player_index].accion = None
                                players[player_index].fichas[ficha_seleccionada] = min(nueva_posicion, 72)
                                comer_ficha(player_index, ficha_seleccionada)
                                players[player_index].historial_movimientos.append(ficha_seleccionada)
                                players[player_index].movimiento_restante = [0, 0]
                                players[player_index].dados = [0, 0]
                                broadcast_game_state()
                            else:
                                print(f"Jugador {players[player_index].color} no puede mover la ficha {ficha_seleccionada} con el valor de dos dados {sum(players[player_index].dados)}")
                        else:
                            print(f"Jugador {players[player_index].color} no ha seleccionado una ficha")
                    
                    elif (player_index == turn_order[current_turn_index] and players[player_index].movimiento_restante == [0,0] and players[player_index].tiros_dados == 1 and players[player_index].intentos_par == 0):
                        print(f"Jugador {players[player_index].color} ha terminado su turno")
                        current_turn_index = (current_turn_index + 1) % len(turn_order)
                        players[player_index].turno = False
                        players[player_index].intentos_par = 0
                        players[player_index].tiros_dados = 0
                        players[player_index].movimiento_restante = [0, 0]

                        if players[turn_order[current_turn_index]] is not None:
                            players[turn_order[current_turn_index]].turno = True


                        # Verificar si hay un ganador
                        ganador = check_winner()
                        if ganador:
                            game_state = "FINISHED"
                            print(f"Jugador {ganador} ha ganado el juego")
                            for player in players:
                                if player is not None:
                                    player.estado = f"Ganador: {ganador}"
                        broadcast_game_state()
                    
                    elif (player_index == turn_order[current_turn_index] and players[player_index].movimiento_restante == [0,0] and players[player_index].tiros_dados == 1 and players[player_index].intentos_par > 0 and players[player_index].intentos_par < 3):
                        print(f"Jugador {players[player_index].color} ha sacado par, puede tirar de nuevo")
                        players[player_index].tiros_dados = 0
                        players[player_index].movimiento_restante = [0, 0]
                        broadcast_game_state()
                        
                        if players[turn_order[current_turn_index]] is not None:
                            players[turn_order[current_turn_index]].turno = True
                        broadcast_game_state()
                        
                # Enviar estado actualizado al cliente actual
                response_data = get_jugadores_activos()
                conn.sendall(pickle.dumps(response_data))

            except (pickle.UnpicklingError, ConnectionError) as e:
                print(f"Error de conexión: {e}")
                break
            except Exception as e:
                print(f"Error en threaded_client: {e}")
                break
    finally:
        if player_index is not None:
            print(f"Jugador {player_index} desconectado")
            players[player_index] = None
            if player_index in conexiones:
                del conexiones[player_index]
            if players.count(None) == 3 and game_state != GAME_STATES["WAITING_PLAYERS"]:
                for player in players:
                    if player is not None:
                        player.fichas = [72, 72, 72, 72]
                        ganador = check_winner()
                        if ganador:
                            game_state = "FINISHED"
                            print(f"Jugador {ganador} ha ganado el juego")
                            for player in players:
                                if player is not None:
                                    player.estado = f"Ganador: {ganador}"
            broadcast_game_state()
        if players.count(None) == 4:
            game_state = GAME_STATES["WAITING_PLAYERS"]
        
        conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    if len(conexiones) < 4:
        start_new_thread(threaded_client, (conn, addr))
    else:
        print("Máximo de jugadores alcanzado")
        conn.close()