import unittest
from Chess.Piece import Pawn, Rook, Position
from Chess.ChessBoard import Game


class PawnTest(unittest.TestCase):
    def test_first_row(self):
        p = Pawn("white", Position(1, 1), Game())
        pos = p.get_possible_moves()
        expected = [
            Position(1, 2),
            Position(1, 3)
        ]
        self.assertEqual(pos, expected)

    def test_last_row(self):
        p = Pawn("white", Position(1, 7), Game())
        pos = p.get_possible_moves()
        expected = []
        self.assertEqual(pos, expected)

    def test_white_destination(self):
        p1 = Pawn("white", Position(1, 1))
        p2 = Rook("white", Position(1, 2)) 
        g = Game()
        g.board[1][1] = p1
        g.board[2][1] = p2
        p1.g = g
        excepted = []
        self.assertEqual(p1.get_possible_moves(), excepted)

    def test_white_destination_2(self):
        p1 = Pawn("white", Position(1, 1))
        p2 = Rook("white", Position(1, 3)) 
        g = Game()
        g.board[1][1] = p1
        g.board[3][1] = p2
        p1.g = g
        excepted = [Position(1, 2)]
        self.assertEqual(p1.get_possible_moves(), excepted)

if __name__ == "__main__":
    unittest.main()