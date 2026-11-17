"""Entrena el Arbol de Decision con los datos de autojuego del Minimax.

Uso: python3 scripts/train_tree.py

Lee data/minimax_games.csv (generado con model/dataset_generator.py),
separa una parte como prueba, entrena un DecisionTreeClassifier y lo
guarda en model/tree_model.joblib. Imprime la precision en el conjunto
de prueba: el porcentaje de posiciones donde el arbol elige la misma
columna que eligio el Minimax (no es una medida de "quien gana mas",
solo de que tanto imita las jugadas del Minimax que no vio entrenando).
"""

import csv

import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

DATA_PATH = 'data/minimax_games.csv'
MODEL_PATH = 'model/tree_model.joblib'
MAX_DEPTH = 15


def load_dataset(path):
    """Lee el CSV y separa las columnas del tablero de la columna move."""
    states, moves = [], []
    with open(path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        feature_names = [
            name for name in reader.fieldnames if name != 'move']
        for row in reader:
            states.append([int(row[name]) for name in feature_names])
            moves.append(int(row['move']))
    return states, moves


def main():
    states, moves = load_dataset(DATA_PATH)
    x_train, x_test, y_train, y_test = train_test_split(
        states, moves, test_size=0.2, random_state=42)

    tree = DecisionTreeClassifier(max_depth=MAX_DEPTH, random_state=42)
    tree.fit(x_train, y_train)

    accuracy = tree.score(x_test, y_test)
    print(f'Muestras de entrenamiento: {len(x_train)}')
    print(f'Muestras de prueba: {len(x_test)}')
    print(f'Precision en prueba (coincide con Minimax): {accuracy:.2%}')

    joblib.dump(tree, MODEL_PATH)
    print(f'Modelo guardado en {MODEL_PATH}')


if __name__ == '__main__':
    main()
