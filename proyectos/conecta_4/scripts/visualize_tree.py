"""Visualiza el Arbol de Decision entrenado (Semana 3, Dia 3).

El arbol completo tiene profundidad 10 y seria ilegible como imagen,
asi que esta visualizacion solo muestra los primeros 3 niveles (las
decisiones mas generales). El modelo que realmente juega sigue siendo
el completo (model/tree_model.joblib); esto es solo para entender
visualmente como decide.

Uso: python scripts/visualize_tree.py
o python visualize_tree.py  (desde la carpeta scripts/)
"""

import os
import sys

# Agregar la carpeta raíz del proyecto al path para que "import model"
# funcione sin importar desde dónde se ejecute el script.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

try:
    import matplotlib  # noqa: E402
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt  # noqa: E402
    from sklearn.tree import plot_tree  # noqa: E402
    import joblib  # noqa: E402
except ImportError as exc:
    print(f"Error: faltan dependencias para visualizar el árbol: {exc}")
    print("Instálalas con: pip install matplotlib scikit-learn joblib")
    sys.exit(1)

from model.game_model import COLS, ROWS  # noqa: E402

# Rutas absolutas basadas en la ubicación de este script.
MODEL_PATH = os.path.join(ROOT_DIR, 'model', 'tree_model.joblib')
OUTPUT_PATH = os.path.join(ROOT_DIR, 'data', 'tree_visualization.png')
DISPLAY_DEPTH = 3

FEATURE_NAMES = [f'c{i}' for i in range(ROWS * COLS)]
CLASS_NAMES = [f'col{i}' for i in range(COLS)]


def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: no se encontró el modelo en {MODEL_PATH}")
        print("Primero ejecuta: python scripts/train_tree.py")
        sys.exit(1)

    tree = joblib.load(MODEL_PATH)

    plt.figure(figsize=(22, 10))
    plot_tree(
        tree, max_depth=DISPLAY_DEPTH, feature_names=FEATURE_NAMES,
        class_names=CLASS_NAMES, filled=True, rounded=True, fontsize=8)
    plt.title(
        f'Arbol de Decision (primeros {DISPLAY_DEPTH} niveles de '
        f'{tree.get_depth()} reales)')
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches='tight')
    print(f'Imagen guardada en {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
