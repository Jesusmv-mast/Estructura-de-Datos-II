"""Orquesta las pantallas: Inicio -> Modo -> Dificultad -> Juego."""

import ttkbootstrap as ttk

from controller.game_controller import GameController
from model.game_model import COLS, ROWS
from view.gui_view import GameView
from view.menu_view import (
    DIFFICULTY_DEPTHS,
    MODE_HUMAN_VS_HUMAN,
    MODE_HUMAN_VS_MINIMAX,
    MODE_HUMAN_VS_TREE,
    DifficultyScreen,
    ModeScreen,
    StartScreen,
)

# Tamaño fijo de la ventana para que no cambie entre pantallas.
# El alto es generoso para que quepa el panel del camino de decision
# del modo Arbol y el boton de Menu principal sin que nada quede cortado.
WINDOW_WIDTH = 560
WINDOW_HEIGHT = 1000


class ConnectFourApp:
    """Controla que pantalla se muestra y arranca la partida."""

    def __init__(self, root):
        self.root = root
        self.root.title('Conecta 4')
        self.root.resizable(False, False)

        # Fondo bonito y consistente para toda la aplicacion.
        self.root.configure(bg='#0b1f3a')

        # Estilos para los contenedores con el mismo fondo.
        style = ttk.Style()
        style.configure('App.TFrame', background='#0b1f3a')
        style.configure('Screen.TFrame', background='#0b1f3a')

        # Centrar la ventana en la pantalla.
        self._center_window()

        self.container = ttk.Frame(root, padding=10, style='App.TFrame')
        self.container.pack(expand=True, fill='both')

        self._current_frame = None
        self._chosen_mode = MODE_HUMAN_VS_HUMAN
        self.show_start()

    def _center_window(self):
        """Coloca la ventana en el centro de la pantalla y fija su tamaño."""
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - WINDOW_WIDTH) // 2
        y = (screen_h - WINDOW_HEIGHT) // 2
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}')

    def _clear(self):
        if self._current_frame is not None:
            self._current_frame.destroy()
            self._current_frame = None

    def show_start(self):
        self._clear()
        self._current_frame = StartScreen(self.container, self.show_mode)
        self._current_frame.pack(expand=True, fill='both')

    def show_mode(self):
        self._clear()
        self._current_frame = ModeScreen(
            self.container, self._on_mode_selected, self.show_start)
        self._current_frame.pack(expand=True, fill='both')

    def _on_mode_selected(self, mode):
        self._chosen_mode = mode
        if mode == MODE_HUMAN_VS_MINIMAX:
            self.show_difficulty()  # Solo el Minimax tiene dificultad.
        else:
            self.start_game(mode, max_depth=6)

    def show_difficulty(self):
        self._clear()
        self._current_frame = DifficultyScreen(
            self.container, self._on_difficulty_selected, self.show_mode)
        self._current_frame.pack(expand=True, fill='both')

    def _on_difficulty_selected(self, difficulty_key):
        max_depth = DIFFICULTY_DEPTHS[difficulty_key]
        self.start_game(self._chosen_mode, max_depth)

    def start_game(self, mode, max_depth):
        self._clear()
        game_frame = ttk.Frame(self.container, padding=(0, 10, 0, 0))
        game_frame.pack(expand=True, fill='both')

        view = GameView(
            self.root, ROWS, COLS, container=game_frame,
            show_mode_selector=False,
            show_path_panel=(mode == MODE_HUMAN_VS_TREE))
        ttk.Button(
            game_frame, text='Menu principal', bootstyle='secondary-outline',
            command=self.show_start,
        ).pack(pady=(4, 10))

        GameController(view, mode=mode, max_depth=max_depth)
        self._current_frame = game_frame
