"""Vista grafica de Conecta 4 con ttkbootstrap (tema 'superhero')."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, LEFT, SECONDARY, X

CELL_SIZE = 80
PADDING = 10
MARGIN = 6
BOARD_COLOR = '#0b1f3a'
EMPTY_COLOR = '#16314f'
PLAYER_COLORS = {'X': '#e63946', 'O': '#ffd166'}
PLAYER_OUTLINES = {'X': '#9d1f29', 'O': '#c49a1e'}

# Resaltado de las 4 celdas ganadoras.
WIN_BG = '#ffe066'        # fondo de la celda ganadora (amarillo brillante)
WIN_OUTLINE = '#ffffff'   # borde de la ficha ganadora (blanco)
WIN_WIDTH = 4             # grosor del borde de las fichas ganadoras

PATH_CANVAS_WIDTH = 400
PATH_ROW_HEIGHT = 32
PATH_MAX_ROWS = 11
PATH_TAKEN_COLOR = '#2ecc71'
PATH_SKIPPED_COLOR = '#7a2b32'
PATH_BG_COLOR = '#0b1f3a'
PATH_TEXT_COLOR = '#d9e2ec'
PATH_RESULT_COLOR = '#ffd166'

MODE_LABELS = {
    'hvh': 'Humano vs Humano',
    'hvm': 'Humano vs IA (Minimax)',
    'hvt': 'Humano vs IA (Árbol)',
}


class GameView:
    """Dibuja el tablero y reporta clics, modo y reinicio."""

    def __init__(self, root, rows, cols, container=None,
                show_mode_selector=True, show_path_panel=False):
        self.root = root
        self.rows = rows
        self.cols = cols
        self._column_handler = None
        self._mode_handler = None
        parent = container if container is not None else root

        if container is None:
            self.root.title('Conecta 4')
            self.root.resizable(False, False)

        # Frame contenedor del tablero y sus controles.
        # - Modos Humano vs Humano y Minimax: se expande para centrar el
        #   tablero verticalmente en la ventana.
        # - Modo Árbol: no se expande, el tablero queda arriba y el panel
        #   de decisión se coloca debajo.
        self.content_frame = ttk.Frame(parent)
        if show_path_panel:
            self.content_frame.pack(pady=(10, 0))
        else:
            self.content_frame.pack(expand=True)

        if show_mode_selector:
            self.mode_var = ttk.StringVar(value='hvh')
            self._build_mode_selector(self.content_frame)

        self.status_var = ttk.StringVar()
        self.status_label = ttk.Label(
            self.content_frame, textvariable=self.status_var,
            font=('Helvetica', 15, 'bold'), bootstyle=INFO,
        )
        self.status_label.pack(pady=(10, 8))

        width = cols * CELL_SIZE + 2 * PADDING
        height = rows * CELL_SIZE + 2 * PADDING
        self.canvas = ttk.Canvas(
            self.content_frame, width=width, height=height,
            bg=BOARD_COLOR, highlightthickness=0, bd=0)
        self.canvas.pack(padx=4, pady=4)

        self.restart_button = ttk.Button(
            self.content_frame, text='Reiniciar', bootstyle='warning-outline', width=14)
        self.restart_button.pack(pady=(14, 4))

        self.metrics_var = ttk.StringVar(value='')
        self.metrics_label = ttk.Label(
            self.content_frame, textvariable=self.metrics_var,
            font=('Helvetica', 9), bootstyle=SECONDARY)
        self.metrics_label.pack(pady=(2, 6))

        # Panel del camino de decision del Arbol: solo ocupa espacio en
        # la ventana cuando el modo activo es Humano vs IA con Arbol.
        # En Humano vs Humano o Minimax, path_canvas queda en None y
        # no se reserva nada de pantalla para el.
        self.path_canvas = None
        if show_path_panel:
            path_height = PATH_ROW_HEIGHT * PATH_MAX_ROWS
            self.path_canvas = ttk.Canvas(
                parent, width=PATH_CANVAS_WIDTH, height=path_height,
                bg=PATH_BG_COLOR, highlightthickness=0, bd=0)
            self.path_canvas.pack(pady=(10, 6))

    def _build_mode_selector(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(pady=(4, 2), fill=X)
        ttk.Label(frame, text='Modo:', bootstyle=SECONDARY).pack(side=LEFT)
        for mode_key, label in MODE_LABELS.items():
            ttk.Radiobutton(
                frame, text=label, variable=self.mode_var,
                value=mode_key, command=self._on_mode_change,
                bootstyle='primary-toolbutton',
            ).pack(side=LEFT, padx=5)

    def _on_mode_change(self):
        if self._mode_handler:
            self._mode_handler(self.mode_var.get())

    def set_column_click_handler(self, handler):
        self._column_handler = handler
        self.canvas.bind('<Button-1>', self._on_click)

    def set_restart_handler(self, handler):
        self.restart_button.config(command=handler)

    def set_mode_handler(self, handler):
        self._mode_handler = handler

    def set_status(self, text):
        self.status_var.set(text)

    def set_metrics(self, nodes, elapsed_seconds, agent_name='IA'):
        """Muestra nodos explorados y tiempo de la ultima jugada de la IA."""
        self.metrics_var.set(
            f'{agent_name}: {nodes} nodos explorados, '
            f'{elapsed_seconds:.3f}s de respuesta')

    def clear_metrics(self):
        self.metrics_var.set('')

    def show_decision_path(self, steps, move):
        """Dibuja el camino del Arbol: en cada pregunta, la rama que
        tomo en verde y la que descarto en rojo, hasta la jugada."""
        if self.path_canvas is None:
            return
        canvas = self.path_canvas
        canvas.delete('all')
        y = 16

        for step in steps:
            label = (
                f"Fila {step['row'] + 1}, col {step['col'] + 1} "
                f"<= {step['threshold']:.1f} ?")
            canvas.create_text(
                8, y, anchor='w', text=label,
                fill=PATH_TEXT_COLOR, font=('Helvetica', 9))

            si_color = (
                PATH_TAKEN_COLOR if step['went_left']
                else PATH_SKIPPED_COLOR)
            no_color = (
                PATH_SKIPPED_COLOR if step['went_left']
                else PATH_TAKEN_COLOR)
            self._draw_branch_box(canvas, 290, y, 'Si', si_color)
            self._draw_branch_box(canvas, 345, y, 'No', no_color)
            y += PATH_ROW_HEIGHT

        canvas.create_text(
            8, y + 4, anchor='w',
            text=f'-> Jugada elegida: columna {move + 1}',
            fill=PATH_RESULT_COLOR, font=('Helvetica', 11, 'bold'))

    @staticmethod
    def _draw_branch_box(canvas, x, y, text, color):
        canvas.create_rectangle(
            x, y - 11, x + 40, y + 11, fill=color, outline=color)
        canvas.create_text(
            x + 20, y, text=text, fill='white',
            font=('Helvetica', 9, 'bold'))

    def clear_decision_path(self):
        if self.path_canvas is not None:
            self.path_canvas.delete('all')

    def schedule_delayed(self, delay_ms, callback):
        """Ejecuta callback despues de delay_ms, sin congelar la ventana."""
        self.root.after(delay_ms, callback)

    def draw_board(self, board, winning_line=None):
        """Dibuja el tablero. Si se pasa winning_line (lista de (fila,col)),
        esas 4 celdas se resaltan con fondo y borde llamativos."""
        self.canvas.delete('all')
        winning_set = set(winning_line) if winning_line else set()
        for r in range(self.rows):
            for c in range(self.cols):
                cell_x0 = PADDING + c * CELL_SIZE
                cell_y0 = PADDING + r * CELL_SIZE
                cell_x1 = cell_x0 + CELL_SIZE
                cell_y1 = cell_y0 + CELL_SIZE

                # Fondo circular resaltado para las celdas de la linea
                # ganadora (un ovalo que llena la celda).
                if (r, c) in winning_set:
                    self.canvas.create_oval(
                        cell_x0, cell_y0, cell_x1, cell_y1,
                        fill=WIN_BG, outline='')

                x0 = cell_x0 + MARGIN
                y0 = cell_y0 + MARGIN
                x1 = cell_x1 - MARGIN
                y1 = cell_y1 - MARGIN
                player = board[r][c]
                fill = PLAYER_COLORS.get(player, EMPTY_COLOR)
                outline = PLAYER_OUTLINES.get(player, BOARD_COLOR)
                width = WIN_WIDTH if (r, c) in winning_set else 2
                self.canvas.create_oval(
                    x0, y0, x1, y1, fill=fill, outline=outline, width=width)

    def _on_click(self, event):
        left = PADDING + MARGIN
        right = PADDING + self.cols * CELL_SIZE - MARGIN
        top = PADDING + MARGIN
        bottom = PADDING + self.rows * CELL_SIZE - MARGIN
        if not (left <= event.x < right and top <= event.y < bottom):
            return
        col = (event.x - PADDING) // CELL_SIZE
        if self._column_handler:
            self._column_handler(col)
