import unittest
from Piece import Pawn, Position, Rook, Knight, Bishop, Queen, King
from Chessboard import Game


class TestPawn(unittest.TestCase):
    def setUp(self):
        self.pawn = Pawn("white", Position(3, 3), None)

    def test_str(self):
        self.assertEqual(str(self.pawn), "♙")

    def test_first_row(self):
        p = Pawn("white", Position(1, 1), Game())
        pos = p.get_possible_moves()
        expected = [Position(1, 2), Position(1, 3)]
        self.assertEqual(pos, expected)

    def test_last_row(self):
        p = Pawn("white", Position(1, 7), Game())
        pos = p.get_possible_moves()
        expected = []
        self.assertEqual(pos, expected)

    def test_white_destination(self):
        g = Game()
        p1 = Pawn("white", Position(1, 1), g)
        p2 = Pawn("white", Position(1, 2), g)
        g.board[1][1] = p1
        g.board[2][1] = p2
        p1.game = g
        expected = []
        self.assertEqual(p1.get_possible_moves(), expected)

    def test_white_destination_2(self):
        g = Game()
        p1 = Pawn("white", Position(1, 1), g)
        r1 = Rook("black", Position(1, 3), g)
        g.board[1][1] = p1
        g.board[3][1] = r1
        p1.game = g
        expected = [Position(1, 2)]
        self.assertEqual(p1.get_possible_moves(), expected)

    def test_move(self):
        g = Game()
        p = Pawn("white", Position(1, 1), g)
        p.move(Position(1, 3))
        print(p.position)
        self.assertEqual(p.position, Position(1, 3))
        self.assertIsNone(g.get_piece_at(Position(1, 1)))
        self.assertEqual(g.get_piece_at(Position(1, 3)), p)

    def test_asText(self):
        self.assertEqual(self.pawn.asText(), "Pawn")


class TestRook(unittest.TestCase):
    def setUp(self):
        self.rook = Rook("white", Position(3, 3), None)

    def test_str(self):
        self.assertEqual(str(self.rook), "♖")

    def test_move(self):
        g = Game()
        r = Rook("white", Position(0, 0), g)
        r.move(Position(0, 3))
        self.assertEqual(r.position, Position(0, 3))
        self.assertIsNone(g.get_piece_at(Position(0, 0)))
        self.assertEqual(g.get_piece_at(Position(0, 3)), r)

    def test_asText(self):
        self.assertEqual(self.rook.asText(), "Rook")


class TestKnight(unittest.TestCase):
    def setUp(self):
        self.knight = Knight("white", Position(3, 3), None)

    def test_str(self):
        self.assertEqual(str(self.knight), "♘")

    def test_move(self):
        g = Game()
        k = Knight("white", Position(0, 0), g)
        k.move(Position(2, 1))
        self.assertEqual(k.position, Position(2, 1))
        self.assertIsNone(g.get_piece_at(Position(0, 0)))
        self.assertEqual(g.get_piece_at(Position(2, 1)), k)

    def test_get_possible_moves(self):
        k = Knight("white", Position(1, 0), Game())
        pos = k.get_possible_moves()
        expected = [Position(0, 2), Position(2, 2)]
        self.assertEqual(pos, expected)

    def test_get_possible_moves_2(self):
        k = Knight("white", Position(4, 4), Game())
        pos = k.get_possible_moves()
        expected = [
            Position(2, 3),
            Position(2, 5),
            Position(3, 2),
            Position(3, 6),
            Position(5, 2),
            Position(5, 6),
            Position(6, 3),
            Position(6, 5),
        ]
        self.assertEqual(pos, expected)

    def test_get_possible_moves_3(self):
        g = Game()
        k = Knight("white", Position(4, 4), g)
        r = Rook("white", Position(2, 3), g)
        b = Bishop("white", Position(2, 5), g)
        g.board[3][2] = r
        g.board[5][2] = b
        g.board[4][4] = k
        pos = k.get_possible_moves()
        expected = [
            Position(3, 2),
            Position(3, 6),
            Position(5, 2),
            Position(5, 6),
            Position(6, 3),
            Position(6, 5),
        ]
        self.assertEqual(pos, expected)

    def test_asText(self):
        self.assertEqual(self.knight.asText(), "Knight")


class TestBishop(unittest.TestCase):
    def setUp(self):
        self.bishop = Bishop("white", Position(3, 3), None)

    def test_str(self):
        self.assertEqual(str(self.bishop), "♗")

    def test_move(self):
        g = Game()
        b = Bishop("white", Position(0, 0), g)
        b.move(Position(3, 3))
        self.assertEqual(b.position, Position(3, 3))
        self.assertIsNone(g.get_piece_at(Position(0, 0)))
        self.assertEqual(g.get_piece_at(Position(3, 3)), b)

    def test_asText(self):
        self.assertEqual(self.bishop.asText(), "Bishop")

    def test_get_possible_moves(self):
        g = Game()
        b = Bishop("white", Position(4, 4), Game())
        g.board[4][4] = b

        pos = b.get_possible_moves()

        expected = [
            Position(2, 2),
            Position(2, 6),
            Position(3, 3),
            Position(3, 5),
            Position(5, 3),
            Position(5, 5),
            Position(6, 2),
            Position(6, 6),
        ]

        expected = sorted(expected, key=lambda pos: (pos.x, pos.y))
        self.assertEqual(pos, expected)


class TestQueen(unittest.TestCase):
    def setUp(self):
        self.queen = Queen("white", Position(3, 3), None)

    def test_str(self):
        self.assertEqual(str(self.queen), "♕")

    def test_move(self):
        g = Game()
        q = Queen("white", Position(0, 0), g)
        q.move(Position(3, 3))
        self.assertEqual(q.position, Position(3, 3))
        self.assertIsNone(g.get_piece_at(Position(0, 0)))
        self.assertEqual(g.get_piece_at(Position(3, 3)), q)

    def test_asText(self):
        self.assertEqual(self.queen.asText(), "Queen")

    def test_get_possible_moves(self):
        g = Game()
        q = Queen("white", Position(4, 4), g)
        r = Rook("white", Position(2, 3), g)
        b = Bishop("white", Position(2, 5), g)
        g.board[3][2] = r
        g.board[5][2] = b
        g.board[4][4] = q
        g.print_board()
        svg = g.to_svg()
        with open("chessboard.svg", "w") as f:
            f.write(svg)
        pos = q.get_possible_moves()
        print(pos)
        expected = [
            Position(0, 4),
            Position(1, 4),
            Position(2, 4),
            Position(3, 4),
            Position(5, 4),
            Position(6, 4),
            Position(7, 4),
            Position(4, 3),
            Position(4, 2),
            Position(4, 5),
            Position(4, 6),
            Position(3, 5),
            Position(2, 6),
            Position(3, 3),
            Position(2, 2),
            Position(5, 5),
            Position(6, 6),
            Position(5, 3),
            Position(6, 2),
        ]
        
        expected = sorted(expected, key=lambda pos: (pos.x, pos.y))
        self.assertEqual(pos, expected)


class TestKing(unittest.TestCase):
    def setUp(self):
        self.king = King("white", Position(3, 3), None)

    def test_str(self):
        self.assertEqual(str(self.king), "♔")

    def test_move(self):
        g = Game()
        k = King("white", Position(0, 0), g)
        k.move(Position(3, 3))
        self.assertEqual(k.position, Position(3, 3))
        self.assertIsNone(g.get_piece_at(Position(0, 0)))
        self.assertEqual(g.get_piece_at(Position(3, 3)), k)

    def test_asText(self):
        self.assertEqual(self.king.asText(), "King")


if __name__ == "__main__":
    unittest.main()
