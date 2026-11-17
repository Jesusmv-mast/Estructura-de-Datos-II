"""Agente que juega usando un Arbol de Decision ya entrenado.

A diferencia de MinimaxAgent, este agente no busca jugadas en el momento
de jugar: ya aprendio un mapa "tablero -> columna" durante el
entrenamiento (ver scripts/train_tree.py), asi que responder es una
sola prediccion, casi instantanea. La contrapartida es que puede
equivocarse en posiciones que no se parecen a nada visto entrenando
(midimos esto como precision del 80% contra el Minimax, no 100%).
"""

import joblib

from model.ml_agent import encode_board
from model.game_model import COLS

DEFAULT_MODEL_PATH = 'model/tree_model.joblib'


class DecisionTreeAgent:
    """Elige jugadas con un DecisionTreeClassifier ya entrenado."""

    def __init__(self, model_path=DEFAULT_MODEL_PATH, ai_player='O',
                human_player='X'):
        self.ai_player = ai_player
        self.human_player = human_player
        self.tree = joblib.load(model_path)
        # El arbol no explora nodos en tiempo real: siempre es 0, a
        # diferencia de nodes_evaluated del MinimaxAgent.
        self.nodes_evaluated = 0

    def get_best_move(self, board):
        """Predice una columna; si esta llena, cae a la valida mas cercana."""
        state = encode_board(board.board, self.ai_player)
        predicted = int(self.tree.predict([state])[0])
        available = board.get_available_moves()

        if predicted in available:
            return predicted, None

        fallback = min(available, key=lambda col: abs(col - predicted))
        return fallback, None

    def get_decision_path(self, board):
        """Devuelve las preguntas (si/no) que el arbol fue respondiendo
        hasta llegar a la jugada, en orden, usando decision_path de
        scikit-learn (no es una aproximacion: es el camino real que
        siguio el arbol entrenado para esta posicion)."""
        state = encode_board(board.board, self.ai_player)
        leaf_id = int(self.tree.apply([state])[0])
        node_indicator = self.tree.decision_path([state])
        node_ids = node_indicator.indices[
            node_indicator.indptr[0]:node_indicator.indptr[1]]
        tree_internals = self.tree.tree_

        steps = []
        for node_id in node_ids:
            if node_id == leaf_id:
                continue  # la hoja final no es una pregunta
            feature = int(tree_internals.feature[node_id])
            threshold = float(tree_internals.threshold[node_id])
            steps.append({
                'row': feature // COLS,
                'col': feature % COLS,
                'threshold': threshold,
                'went_left': state[feature] <= threshold,
            })
        return steps
