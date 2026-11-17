"""Pruebas para model/ml_agent.py (generacion de dataset)."""

from model.ml_agent import encode_board
from model.game_model import GameModel


def test_encode_board_empty():
    model = GameModel()
    encoded = encode_board(model.board, 'X')
    assert encoded == [0] * (model.rows * model.cols)


def test_encode_board_marks_own_and_opponent():
    model = GameModel()
    model.make_move(0, 'X')
    model.make_move(1, 'O')

    encoded_from_x = encode_board(model.board, 'X')
    assert encoded_from_x[15] == 1
    assert encoded_from_x[16] == -1

    encoded_from_o = encode_board(model.board, 'O')
    assert encoded_from_o[15] == -1
    assert encoded_from_o[16] == 1
