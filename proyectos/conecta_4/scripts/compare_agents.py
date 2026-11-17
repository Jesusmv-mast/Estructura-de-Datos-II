"""Comparacion final: Minimax vs Arbol de Decision (Semana 3, Dia 5).

Juega partidas de autojuego con el Minimax para generar posiciones de
prueba, y en cada una le pregunta a los dos agentes que jugarian.
Mide:
- Precision: en que porcentaje de las posiciones el Arbol elige la
    misma columna que el Minimax a profundidad 6 (el Minimax se usa
    como referencia de "jugada fuerte", no como verdad absoluta).
- Latencia: cuanto tarda cada uno, en promedio, en decidir una
    jugada en esas mismas posiciones.

Uso: python3 scripts/compare_agents.py
"""

import os
import random
import sys
import time

# Permite correr este script directamente (python3 scripts/..) sin
# tener que instalar el proyecto: agrega la carpeta raiz al path para
# que "import model" encuentre el paquete model/.
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.decision_tree_agent import DecisionTreeAgent  # noqa: E402
from model.game_model import GameModel  # noqa: E402
from model.minimax_agent import MinimaxAgent  # noqa: E402

NUM_GAMES = 12
MAX_DEPTH = 6
EPSILON = 0.15
SEED = 999


def collect_test_positions():
    """Juega partidas de autojuego y guarda una foto de cada posicion."""
    rng = random.Random(SEED)
    agent_x = MinimaxAgent(
        ai_player='X', human_player='O', max_depth=MAX_DEPTH)
    agent_o = MinimaxAgent(
        ai_player='O', human_player='X', max_depth=MAX_DEPTH)
    positions = []
    for _ in range(NUM_GAMES):
        model = GameModel()
        while True:
            agent = agent_x if model.current_player == 'X' else agent_o
            best_move, _ = agent.get_best_move(model)
            positions.append(
                ([row[:] for row in model.board], model.current_player))

            move = (rng.choice(model.get_available_moves())
                    if rng.random() < EPSILON else best_move)
            model.make_move(move, model.current_player)
            if model.check_winner(model.current_player) or model.is_draw():
                break
            model.switch_player()
    return positions


def model_from_snapshot(board, current_player):
    """Reconstruye un GameModel jugable a partir de una foto guardada."""
    model = GameModel()
    model.board = [row[:] for row in board]
    model.current_player = current_player
    model.heights = [
        sum(1 for r in range(model.rows) if model.board[r][c] != ' ')
        for c in range(model.cols)
    ]
    return model


def main():
    positions = collect_test_positions()
    total = len(positions)
    print(f'Posiciones de prueba: {total}')

    # Un solo agente de cada tipo, reutilizado en el bucle: crear un
    # DecisionTreeAgent nuevo en cada iteracion recargaria el archivo
    # .joblib cada vez y mediria mal su latencia real de inferencia.
    minimax = MinimaxAgent(
        ai_player='X', human_player='O', max_depth=MAX_DEPTH)
    tree = DecisionTreeAgent(ai_player='X', human_player='O')

    matches = 0
    minimax_total_time = 0.0
    tree_total_time = 0.0

    for board, player in positions:
        opponent = 'O' if player == 'X' else 'X'
        model = model_from_snapshot(board, player)

        minimax.ai_player, minimax.human_player = player, opponent
        tree.ai_player, tree.human_player = player, opponent

        start = time.perf_counter()
        minimax_move, _ = minimax.get_best_move(model)
        minimax_total_time += time.perf_counter() - start

        start = time.perf_counter()
        tree_move, _ = tree.get_best_move(model)
        tree_total_time += time.perf_counter() - start

        if minimax_move == tree_move:
            matches += 1

    print()
    print('--- Precision (coincidencia con Minimax) ---')
    print(f'{matches}/{total} = {matches / total:.2%}')
    print()
    print('--- Latencia promedio por jugada ---')
    minimax_ms = minimax_total_time / total * 1000
    tree_ms = tree_total_time / total * 1000
    print(f'Minimax (depth={MAX_DEPTH}): {minimax_ms:.2f} ms')
    print(f'Arbol de Decision:        {tree_ms:.2f} ms')
    print(f'El arbol responde {minimax_total_time / tree_total_time:.0f}x '
        f'mas rapido en promedio.')


if __name__ == '__main__':
    main()
