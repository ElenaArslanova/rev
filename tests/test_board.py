import kit
import unittest
from settings import *


class TestBoard(unittest.TestCase):
    def test_set_start_cells(self):
        board = kit.Board()
        self.assertIsNot(board.board[SIZE // 2 - 1][SIZE // 2 - 1], EMPTY)
        self.assertIsNot(board.board[SIZE // 2 - 1][SIZE // 2], EMPTY)
        self.assertIsNot(board.board[SIZE // 2][SIZE // 2 - 1], EMPTY)
        self.assertIsNot(board.board[SIZE // 2][SIZE // 2], EMPTY)

    def test_mark_move_in_direction_west(self):
        board = kit.Board()
        board.mark_move_in_direction(BLACK, board.board[4][4], WEST)
        self.assertEqual(board.board[2][4].can_be_taken, True)
        self.assertEqual(board.board[4][2].can_be_taken, False)
        self.assertEqual(board.board[5][5].can_be_taken, False)
        board.clear_moves()

    def test_valid_moves_start(self):
        board = kit.Board()
        board.mark_valid_moves(WHITE)
        for i, j in zip([2, 3, 4, 5], [3, 2, 5, 4]):
            self.assertEqual(board.board[i][j].can_be_taken, True)


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
