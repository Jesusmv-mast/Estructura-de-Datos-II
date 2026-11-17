"""Punto de entrada de Conecta 4."""

import ttkbootstrap as ttk

from view.app import ConnectFourApp

APP_THEME = 'superhero'


def main():
    root = ttk.Window(themename=APP_THEME)
    ConnectFourApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
