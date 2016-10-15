import kit
import unittest
from settings import *

class TestBoard(unittest.TestCase):
    def test_valid_moves_corner(self):
        board = kit.Board()
        board.board[1][7].set_black()
        board.board[2][7].set_white()
        board.mark_valid_moves(WHITE)
        self.assertEqual(board.board[0][7].can_be_taken, True)


    def test_clear_moves(self):
        board = kit.Board()
        board.mark_valid_moves(BLACK)
        for i, j in zip([2, 3, 4, 5], [4, 5, 2, 3]):
            self.assertEqual(board.board[i][j].can_be_taken, True)
        board.clear_moves()
        for i, j in zip([2, 3, 4, 5], [4, 5, 2, 3]):
            self.assertEqual(board.board[i][j].can_be_taken, False)



if __name__ == '__main__':
    unittest.main()
