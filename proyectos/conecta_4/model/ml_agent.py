"""Herramienta de simulacion: genera el dataset para el Arbol de Decision.

Un agente Minimax juega contra un jugador que elige columnas al azar,
partida tras partida. En cada jugada del Minimax se guarda el tablero
(desde la perspectiva de quien mueve: 1 = mis fichas, -1 = rival,
0 = vacio) junto con la columna que eligio: esa es la "respuesta
correcta" que el Arbol de Decision va a aprender a imitar.

Jugar contra un rival aleatorio (en vez de Minimax contra Minimax)
genera tableros mas variados y menos repetitivos, porque el rival no
juega siempre optimo.
"""

import csv
import random

from model.game_model import COLS, ROWS, GameModel
from model.minimax_agent import MinimaxAgent

MAX_DEPTH = 6
DEFAULT_OUTPUT_PATH = 'data/minimax_games.csv'


def encode_board(board, current_player):
    """Aplana el tablero a 1 (mis fichas), -1 (rival), 0 (vacio)."""
    opponent = 'O' if current_player == 'X' else 'X'
    cells = []
    for row in board:
        for cell in row:
            if cell == current_player:
                cells.append(1)
            elif cell == opponent:
                cells.append(-1)
            else:
                cells.append(0)
    return cells


def play_one_game(minimax_agent, minimax_player, rng):
    """Minimax vs un jugador aleatorio; guarda solo las jugadas de
    Minimax (las del jugador aleatorio no son un ejemplo a imitar)."""
    model = GameModel()
    random_player = 'O' if minimax_player == 'X' else 'X'
    samples = []
    while True:
        if model.current_player == minimax_player:
            move, _ = minimax_agent.get_best_move(model)
            state = encode_board(model.board, model.current_player)
            samples.append((state, move))
        else:
            move = rng.choice(model.get_available_moves())

        model.make_move(move, model.current_player)
        if model.check_winner(model.current_player) or model.is_draw():
            break
        model.switch_player()
    return samples, random_player


def generate_dataset(num_games, seed=42, max_depth=MAX_DEPTH):
    """Genera `num_games` partidas Minimax vs aleatorio."""
    rng = random.Random(seed)
    all_samples = []
    for i in range(num_games):
        # Alterna quien empieza para no sesgar el dataset.
        minimax_player = 'X' if i % 2 == 0 else 'O'
        agent = MinimaxAgent(
            ai_player=minimax_player,
            human_player='O' if minimax_player == 'X' else 'X',
            max_depth=max_depth)
        samples, _ = play_one_game(agent, minimax_player, rng)
        all_samples.extend(samples)
    return all_samples


def save_dataset(samples, path):
    """Guarda las muestras en un CSV: columnas del tablero + 'move'."""
    header = [f'c{i}' for i in range(ROWS * COLS)] + ['move']
    with open(path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for state, move in samples:
            writer.writerow(state + [move])


if __name__ == '__main__':
    import sys

    games = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    print(f'Generando {games} partidas Minimax vs aleatorio '
        f'(depth={MAX_DEPTH})...')
    dataset = generate_dataset(games)
    save_dataset(dataset, DEFAULT_OUTPUT_PATH)
    print(f'{len(dataset)} muestras guardadas en {DEFAULT_OUTPUT_PATH}')
