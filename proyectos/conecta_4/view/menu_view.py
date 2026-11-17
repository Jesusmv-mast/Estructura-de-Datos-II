"""Pantallas de inicio, seleccion de modo y dificultad (ttkbootstrap)."""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SECONDARY, SUCCESS

MODE_HUMAN_VS_HUMAN = 'hvh'
MODE_HUMAN_VS_MINIMAX = 'hvm'
MODE_HUMAN_VS_TREE = 'hvt'

DIFFICULTY_LABELS = {
    'fácil': 'Facil',
    'medio': 'Medio',
    'difícil': 'Dificil',
}

# Profundidad de busqueda del Minimax por nivel.
DIFFICULTY_DEPTHS = {
    'fácil': 2,
    'medio': 4,
    'difícil': 6,
}

PANEL_WIDTH = 320

# Colores de fondo bonitos y consistentes.
BG_COLOR = '#0b1f3a'      # azul marino oscuro
PANEL_COLOR = '#16314f'   # azul un poco mas claro para los paneles


class _BaseScreen(ttk.Frame):
    """Pantalla base con fondo bonito y centrado."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(style='Screen.TFrame')

        # Panel interior con fondo distinto para resaltar el contenido.
        self.panel = tk.Frame(
            self, bg=PANEL_COLOR, width=PANEL_WIDTH, highlightthickness=0,
            bd=0,
        )
        self.panel.pack(expand=True, fill='both', padx=40, pady=20)
        self.panel.pack_propagate(False)

        # Contenedor real de los widgets dentro del panel.
        self.content = ttk.Frame(self.panel, padding=30)
        self.content.pack(expand=True)


class StartScreen(_BaseScreen):
    """Pantalla de bienvenida con el boton para empezar."""

    def __init__(self, parent, on_play):
        super().__init__(parent)
        ttk.Label(
            self.content, text='Conecta 4', font=('Helvetica', 30, 'bold'),
            bootstyle=PRIMARY,
        ).pack(pady=(30, 6))
        ttk.Label(
            self.content, text='Tablero reducido 5 x 4',
            font=('Helvetica', 12), bootstyle=SECONDARY,
        ).pack(pady=(0, 36))
        ttk.Button(
            self.content, text='Jugar', width=16, bootstyle=SUCCESS,
            command=on_play,
        ).pack(ipady=6, pady=10)


class ModeScreen(_BaseScreen):
    """Pantalla para elegir Humano vs Humano, Minimax o Arbol."""

    def __init__(self, parent, on_select, on_back):
        super().__init__(parent)
        ttk.Label(
            self.content, text='Elige un modo', font=('Helvetica', 18, 'bold'),
        ).pack(pady=(10, 24))
        ttk.Button(
            self.content, text='Humano vs Humano', width=24, bootstyle=PRIMARY,
            command=lambda: on_select(MODE_HUMAN_VS_HUMAN),
        ).pack(ipady=4, pady=8)
        ttk.Button(
            self.content, text='Humano vs IA (Minimax)', width=24,
            bootstyle=PRIMARY,
            command=lambda: on_select(MODE_HUMAN_VS_MINIMAX),
        ).pack(ipady=4, pady=8)
        ttk.Button(
            self.content, text='Humano vs IA (AD)', width=24,
            bootstyle='info',
            command=lambda: on_select(MODE_HUMAN_VS_TREE),
        ).pack(ipady=4, pady=8)
        ttk.Button(
            self.content, text='Atras', width=24, bootstyle='secondary-outline',
            command=on_back,
        ).pack(pady=(24, 0))


class DifficultyScreen(_BaseScreen):
    """Pantalla para elegir la dificultad de la IA."""

    def __init__(self, parent, on_select, on_back):
        super().__init__(parent)
        ttk.Label(
            self.content, text='Elige la dificultad',
            font=('Helvetica', 18, 'bold'),
        ).pack(pady=(10, 24))
        styles = {
            'fácil': SUCCESS,
            'medio': 'warning',
            'difícil': 'danger',
        }
        for key, label in DIFFICULTY_LABELS.items():
            ttk.Button(
                self.content, text=label, width=24, bootstyle=styles[key],
                command=lambda k=key: on_select(k),
            ).pack(ipady=4, pady=8)
        ttk.Button(
            self.content, text='Atras', width=24, bootstyle='secondary-outline',
            command=on_back,
        ).pack(pady=(24, 0))
