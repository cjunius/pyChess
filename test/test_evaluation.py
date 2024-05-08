import chess

import engines.evaluation as evaluation

class TestEvaluation:
    def test_material_balance_new_game(self):
        board = chess.Board()
        score = evaluation.evaluate_material_balance(board)
        assert score == 0

    def test_piece_square_table_new_game(self):
        board = chess.Board()
        score = evaluation.evaluate_piece_square_table(board)
        assert score == 0

    def test_mobility_new_game(self):
        board = chess.Board()
        score = evaluation.evaluate_mobility(board)
        assert score == 0

    def test_board_control_new_game(self):
        board = chess.Board()
        score = evaluation.board_control(board)
        assert score == 0

