from chess import Board

import archive.quiescence_search as quiescence_search

class TestEvaluation:

    def test_quiescence_search_checkmate(self):
        board = Board("r1bqkbnr/ppp2Qpp/2np4/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
        score = quiescence_search.quiescence_search(board, -999999, 999999, 0)
        assert score == -9999

    def test_quiescence_search_checkmate_with_depth(self):
        board = Board("r1bqkbnr/ppp2Qpp/2np4/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
        score = quiescence_search.quiescence_search(board, -999999, 999999, 1)
        assert score == -10000

    def test_quiescence_search_stalemate(self):
        board = Board("k7/8/KR6/8/8/8/8/8 b - - 0 37")
        score = quiescence_search.quiescence_search(board, -999999, 999999, 0)
        assert score == 0
    
    def test_quiescence_search_insufficient_material(self):
        board = Board("8/8/K7/8/8/k7/8/8 b - - 0 37")
        score = quiescence_search.quiescence_search(board, -999999, 999999, 0)
        assert score == 0

    # ToDo: Add test for fivefold repetition

    def test_quiescence_search_seventyfive_moves(self):
        board = Board("k7/8/K7/R7/8/8/8/8 b - - 0 150")
        board.halfmove_clock = 150
        score = quiescence_search.quiescence_search(board, -999999, 999999, 0)
        assert score == 0

    def test_quiescence_search_new_game(self):
        board = Board()
        score = quiescence_search.quiescence_search(board, -999999, 999999, 0)
        assert score == 0

    def test_quiescence_search_new_game_return_beta(self):
        board = Board()
        score = quiescence_search.quiescence_search(board, -999999, -999999, 0)
        assert score == -999999


