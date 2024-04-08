import unittest
from Piece import *

class PawnTest(unittest.TestCase):
    def test_first_row(self):
        p = Pawn("white", Position(1, 1))
        pos = p.get_possible_moves()
        expected = [
            Position(1, 2),
            Position(1, 3)
        ]
        self.assertEqual(pos, expected)
        
    def test_last_row(self):
        p = Pawn("white", Position(1, 7))
        pos = p.get_possible_moves()
        expected = []
        self.assertEqual(pos, expected)
        
    def test_white_destination(self):
        p1 = Pawn("white", Position(1, 1))
        p2 = Pawn("white", Position(1, 2))
        expected = []
        self.assertEqual(p1.get_possible_moves(), expected)
        