from heapq import heappop, heappush

# Definir los movimientos posibles
moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # derecha, izquierda, abajo, arriba

# Obtener las coordenadas iniciales del jugador, tesoro y guardias
def get_initial_state(grid):
    treasure_position = None
    start_position = None
    guard_positions = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start_position = (i, j)
            elif grid[i][j] == 'T':
                treasure_position = (i, j)
            elif grid[i][j] == 'G':
                guard_positions.append((i, j))

    return start_position, treasure_position, guard_positions

# Heurística de distancia de Manhattan
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Verifica si la posición es válida
def is_valid_position(grid, position, visited_positions):
    x, y = position
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        if grid[x][y] != '#' and position not in visited_positions:
            return True
    return False

# Movimiento eficiente del guardia hacia el jugador
def move_guard(guard_pos, player_pos, grid, visited_positions):
    best_move = guard_pos
    best_distance = manhattan_distance(guard_pos, player_pos)

    for move in moves:
        new_guard_pos = (guard_pos[0] + move[0], guard_pos[1] + move[1])
        if is_valid_position(grid, new_guard_pos, visited_positions):
            new_distance = manhattan_distance(new_guard_pos, player_pos)
            if new_distance < best_distance:  # Elegir el movimiento que minimice la distancia
                best_distance = new_distance
                best_move = new_guard_pos

    return best_move

# Función de Alpha-Beta Pruning
def alpha_beta(grid, player_pos, treasure_pos, guard_positions, depth, alpha, beta, maximizing_player, player_path, guard_paths, visited_player, visited_guards):
    if player_pos == treasure_pos:
        return 1, player_path, guard_paths
    
    if player_pos in guard_positions:
        return -1, player_path, guard_paths

    if depth == 0:
        return 0, player_path, guard_paths

    if maximizing_player:
        max_eval = -float('inf')
        best_player_path = player_path
        best_guard_paths = guard_paths
        for move in moves:
            new_pos = (player_pos[0] + move[0], player_pos[1] + move[1])
            if is_valid_position(grid, new_pos, visited_player):
                visited_player.add(new_pos)
                eval, new_player_path, new_guard_paths = alpha_beta(grid, new_pos, treasure_pos, guard_positions, depth - 1, alpha, beta, False, player_path + [new_pos], guard_paths, visited_player, visited_guards)
                visited_player.remove(new_pos)

                if eval > max_eval:
                    max_eval = eval
                    best_player_path = new_player_path
                    best_guard_paths = new_guard_paths
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Poda
        return max_eval, best_player_path, best_guard_paths
    else:
        # Turno de los guardias (evaluar el movimiento de cada guardia)
        min_eval = float('inf')
        best_player_path = player_path
        best_guard_paths = guard_paths
        for guard_index, guard_pos in enumerate(guard_positions):
            new_guard_pos = move_guard(guard_pos, player_pos, grid, visited_guards[guard_index])
            if new_guard_pos != guard_pos:
                visited_guards[guard_index].add(new_guard_pos)

            new_guard_positions = guard_positions[:]
            new_guard_positions[guard_index] = new_guard_pos

            # Actualizar la ruta del guardia
            new_guard_paths = [path + [new_guard_pos] if idx == guard_index else path for idx, path in enumerate(guard_paths)]

            eval, new_player_path, final_guard_paths = alpha_beta(grid, player_pos, treasure_pos, new_guard_positions, depth - 1, alpha, beta, True, player_path, new_guard_paths, visited_player, visited_guards)
            if new_guard_pos != guard_pos:
                visited_guards[guard_index].remove(new_guard_pos)

            if eval < min_eval:
                min_eval = eval
                best_player_path = new_player_path
                best_guard_paths = final_guard_paths
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Poda
        return min_eval, best_player_path, best_guard_paths



# Función principal para la búsqueda con Alpha-Beta Pruning
def alpha_beta_treasure_hunt(grid):
    start_position, treasure_position, guard_positions = get_initial_state(grid)
    depth_limit = 50  # Limitar la profundidad de la búsqueda a un valor más alto
    initial_guard_paths = [[guard] for guard in guard_positions]  # Guardar los caminos de los guardias
    visited_player = {start_position}  # Conjunto de posiciones visitadas por el jugador
    visited_guards = [set([guard]) for guard in guard_positions]  # Conjunto de posiciones visitadas por cada guardia

    score, player_path, guard_paths = alpha_beta(grid, start_position, treasure_position, guard_positions, depth_limit, -float('inf'), float('inf'), True, [start_position], initial_guard_paths, visited_player, visited_guards)

    if score == 1:
        print("¡Tesoro encontrado!")
        print("Recorrido del jugador:", player_path)
        for i, guard_path in enumerate(guard_paths):
            print(f"Recorrido del guardia {i + 1}:", guard_path)
        return player_path, guard_paths
    elif score == -1:
        print("El jugador fue atrapado por los guardias.")
        print("Recorrido del jugador:", player_path)
        for i, guard_path in enumerate(guard_paths):
            print(f"Recorrido del guardia {i + 1}:", guard_path)
        return player_path, guard_paths
    else:
        print("No se encontró una solución.")
        print("Recorrido del jugador:", player_path)
        for i, guard_path in enumerate(guard_paths):
            print(f"Recorrido del guardia {i + 1}:", guard_path)
        return player_path, guard_paths



# Función para recibir la cuadrícula del usuario
if __name__ == "__main__":
    def get_grid_from_user():
        print("Introduce la cuadrícula (usa S para Start, T para Treasure, # para Obstáculo, . para Espacio vacío, G para Guardia):")
        grid = []
        while True:
            row = input()
            if not row:  # Salir con una línea vacía
                break
            grid.append(list(row))
        return grid
    # Ejecutar el algoritmo
    user_grid = get_grid_from_user()
    alpha_beta_treasure_hunt(user_grid)
