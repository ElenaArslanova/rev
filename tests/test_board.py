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
