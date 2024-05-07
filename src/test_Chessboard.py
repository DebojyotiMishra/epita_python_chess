import unittest
from Chessboard import Game, Position, Piece, Rook, Knight, Bishop, Queen, King, Pawn


class ChessboardTest(unittest.TestCase):
    def test_get_piece_at(self):
        game = Game()
        piece = game.get_piece_at(Position(0, 0))
        self.assertIsInstance(piece, Rook)
        self.assertEqual(piece.color, "white")


    def test_chess_notation_to_position(self):
        game = Game()
        pos = game.chess_notation_to_position("a1")
        self.assertEqual(pos.x, 7)
        self.assertEqual(pos.y, 0)

    def test_full_chess_notation_to_position(self):
        game = Game()
        start, end = game.full_chess_notation_to_position("a1-a2")
        self.assertEqual(start.x, 7)
        self.assertEqual(start.y, 0)
        self.assertEqual(end.x, 7)
        self.assertEqual(end.y, 1)

    def test_make_move(self):
        game = Game()
        game.make_move(Position(4, 6), Position(4, 4))
        piece = game.get_piece_at(Position(4, 4))
        self.assertIsInstance(piece, Pawn)

    def test_is_valid_move(self):
        game = Game()
        valid = game.is_valid_move(Position(4, 6), Position(4, 4))
        self.assertTrue(valid)

    def test_is_check(self):
        game = Game()
        self.assertFalse(game.is_check("white"))

    def test_is_checkmate(self):
        game = Game()
        self.assertFalse(game.is_checkmate("white"))

    def test_is_stalemate(self):
        game = Game()
        self.assertFalse(game.is_stalemate("white"))

    def test_is_draw(self):
        game = Game()
        self.assertFalse(game.is_draw())

    def test_to_svg(self):
        game = Game()
        svg_content = game.to_svg()
        self.assertTrue(len(svg_content) > 0)


if __name__ == "__main__":
    unittest.main()
