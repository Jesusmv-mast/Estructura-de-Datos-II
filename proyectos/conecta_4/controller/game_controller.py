"""Controlador de Conecta 4: coordina modelo, vista y agentes de IA."""

import time

from model.decision_tree_agent import DecisionTreeAgent
from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent

MODE_HUMAN_VS_HUMAN = 'hvh'
MODE_HUMAN_VS_MINIMAX = 'hvm'
MODE_HUMAN_VS_TREE = 'hvt'
AI_MODES = (MODE_HUMAN_VS_MINIMAX, MODE_HUMAN_VS_TREE)
AI_THINK_DELAY_MS = 500
TREE_MODEL_PATH = 'model/tree_model.joblib'

# Nombres de color para mostrar en pantalla, en vez de la letra interna.
# 'X' y 'O' siguen siendo los simbolos que usa el modelo y el tablero.
PLAYER_NAMES = {'X': 'Rojo', 'O': 'Amarillo'}


class GameController:
    """Recibe los eventos de la vista y actualiza el modelo."""

    def __init__(self, view, ai_player='O', human_player='X',
                mode=MODE_HUMAN_VS_HUMAN, max_depth=6,
                tree_model_path=TREE_MODEL_PATH):
        self.view = view
        self.ai_player = ai_player
        self.human_player = human_player
        self.mode = mode
        self.max_depth = max_depth
        self.tree_model_path = tree_model_path
        self.agent = self._build_agent()
        self.model = GameModel()
        self.game_over = False

        self.view.set_column_click_handler(self.on_column_click)
        self.view.set_restart_handler(self.restart)
        self.view.set_mode_handler(self.set_mode)
        self._update_view(self._turn_message())

    def _build_agent(self):
        """Crea el agente de IA segun el modo (Minimax o Arbol)."""
        if self.mode == MODE_HUMAN_VS_TREE:
            return DecisionTreeAgent(
                self.tree_model_path, ai_player=self.ai_player,
                human_player=self.human_player)
        return MinimaxAgent(
            ai_player=self.ai_player, human_player=self.human_player,
            max_depth=self.max_depth)

    def _turn_message(self):
        """Arma el texto 'Turno de <color>' para el jugador actual."""
        name = PLAYER_NAMES.get(
            self.model.current_player, self.model.current_player)
        return f'Turno de {name}'

    def set_mode(self, mode):
        """Cambia de modo (Humano vs Humano / Minimax / Arbol) y reinicia."""
        self.mode = mode
        self.agent = self._build_agent()
        self.restart()

    def on_column_click(self, col):
        """Procesa el clic en una columna."""
        if self.game_over:
            return
        if self.mode in AI_MODES:
            if self.model.current_player != self.human_player:
                return  # es turno de la IA, se ignora el clic

        self._play_move(col, self.model.current_player)

        if (not self.game_over
                and self.mode in AI_MODES
                and self.model.current_player == self.ai_player):
            self.view.set_status('La IA está pensando...')
            self.view.schedule_delayed(AI_THINK_DELAY_MS, self._play_ai_turn)

    def _play_move(self, col, player):
        """Aplica una jugada (de humano o de IA) y actualiza la vista."""
        player_name = PLAYER_NAMES.get(player, player)
        if not self.model.make_move(col, player):
            self.view.set_status(
                f'Columna {col + 1} llena. Turno de {player_name}')
            return

        if self.model.check_winner(player):
            self.game_over = True
            winning_line = self.model.get_winning_line(player)
            message = f'¡Gana {player_name}!'
        elif self.model.is_draw():
            self.game_over = True
            winning_line = None
            message = 'Empate'
        else:
            self.model.switch_player()
            winning_line = None
            message = self._turn_message()
        self._update_view(message, winning_line)

    def _play_ai_turn(self):
        """Pide al agente su jugada, mide sus metricas y la aplica."""
        start = time.time()
        move, _ = self.agent.get_best_move(self.model)
        elapsed = time.time() - start

        if self.mode == MODE_HUMAN_VS_TREE:
            # El camino se calcula antes de jugar: una vez aplicada la
            # jugada el tablero ya cambio y la posicion no es la misma.
            steps = self.agent.get_decision_path(self.model)
            nodes = len(steps)
            agent_name = 'Árbol'
            self.view.show_decision_path(steps, move)
        else:
            nodes = self.agent.nodes_evaluated
            agent_name = 'Minimax'
            self.view.clear_decision_path()

        self.view.set_metrics(nodes, elapsed, agent_name)
        self._play_move(move, self.ai_player)

    def restart(self):
        """Inicia una partida nueva, conservando el modo actual."""
        self.model = GameModel()
        self.game_over = False
        self.view.clear_metrics()
        self.view.clear_decision_path()
        self._update_view(self._turn_message())

    def _update_view(self, message, winning_line=None):
        self.view.draw_board(self.model.board, winning_line)
        self.view.set_status(message)
