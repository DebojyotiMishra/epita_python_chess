import unittest
from Chessboard import Game

class TestChessboard(unittest.TestCase):
    def setUp(self):
        self.game = Game()

        def test_print_board(self):
            expected_output = "♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ \n" \
                              "♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ \n" \
                              "                \n" \
                              "                \n" \
                              "                \n" \
                              "                \n" \
                              "♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ \n" \
                              "♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ \n"
            self.assertEqual(expected_output, self.game.print_board())

    if __name__ == '__main__':
        unittest.main()
