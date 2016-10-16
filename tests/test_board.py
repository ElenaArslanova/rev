import kit
import unittest
from game import Game
from settings import *

class TestBoard(unittest.TestCase):
    def test_valid_moves_corner(self):
        board = kit.Board(SIZE)
        board.board[1][7].set_black()
        board.board[2][7].set_white()
        board.mark_valid_moves(WHITE)
        self.assertEqual(board.board[0][7].can_be_taken, True)


    def test_clear_moves(self):
        board = kit.Board(SIZE)
        board.mark_valid_moves(BLACK)
        for i, j in zip([2, 3, 4, 5], [4, 5, 2, 3]):
            self.assertEqual(board.board[i][j].can_be_taken, True)
        board.clear_moves()
        for i, j in zip([2, 3, 4, 5], [4, 5, 2, 3]):
            self.assertEqual(board.board[i][j].can_be_taken, False)

    def test_restart(self):
        board = kit.Board(SIZE)
        board.make_move((5, 3), BLACK)
        self.assertTrue(board.cell_count > 4)
        board.restart()
        self.assertTrue(board.cell_count == 4)
        self.assertEqual(board.board, kit.Board(SIZE).board)

    def test_white_win(self):
        pass

    def test_black_win(self):
        pass

    def test_tie(self):
        pass



if __name__ == '__main__':
    unittest.main()
