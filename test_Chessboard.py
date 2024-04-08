import unittest
from Chessboard import Game

class TestChessboard(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_print_board(self):
        expected_output = "R N B Q K B N R \n" \
                          "P P P P P P P P \n" \
                          "                \n" \
                          "                \n" \
                          "                \n" \
                          "                \n" \
                          "p p p p p p p p \n" \
                          "r n b q k b n r \n"
        self.assertEqual(expected_output, self.game.print_board())

if __name__ == '__main__':
    unittest.main()