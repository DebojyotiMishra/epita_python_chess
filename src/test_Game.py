import unittest
from Chessboard import Game, Position
from Piece import *


class TestGame(unittest.TestCase):
    def test_valid_move(self):
        game = Game()
        game.board[1][1] = Pawn("white", Position(1, 1), game)
        valid_move = game.is_valid_move(Position(1, 1), Position(1, 2))
        self.assertTrue(valid_move)

    def test_get_piece_at(self):
        game = Game()
        piece = game.get_piece_at(Position(1, 0))
        self.assertIsInstance(piece, Knight)
        self.assertEqual(piece.color, "white")
 

    def test_check(self):
        game = Game()
        game.board[2][3] = King("white", Position(2, 3), game)
        game.board[5][3] = Rook("black", Position(5, 3), game)
        game.board[3][3] = None
        game.board[4][3] = None 
        is_check = game.is_check("white")
        self.assertTrue(is_check)

    def test_not_check(self):
        game = Game()
        game.board[2][3] = King("white", Position(2, 3), game)
        game.board[5][3] = Queen("black", Position(5, 3), game)
        game.board[3][3] = Bishop("black", Position(4, 3), game)
        game.board[4][3] = None 
        is_check = game.is_check("white")
        self.assertFalse(is_check)

    def test_not_checkmate(self):
        game = Game()
        game.board[0][0] = King("black", Position(0, 0), game)
        game.board[1][1] = Rook("white", Position(1, 1), game)
        is_checkmate = game.is_checkmate("black")
        self.assertFalse(is_checkmate)


if __name__ == "__main__":
    unittest.main()