import kit
import unittest
from game import Game
from random import randint, choice
from settings import *

class TestBoard(unittest.TestCase):
    def test_valid_moves_corner(self):
        board = kit.Board(8)
        board.board[1][7].set_black()
        board.board[2][7].set_white()
        board.mark_valid_moves(WHITE)
        self.assertEqual(board.board[0][7].can_be_taken, True)


    def test_clear_moves(self):
        board = kit.Board(8)
        board.mark_valid_moves(BLACK)
        for i, j in zip([2, 3, 4, 5], [4, 5, 2, 3]):
            self.assertEqual(board.board[i][j].can_be_taken, True)
        board.clear_moves()
        for i, j in zip([2, 3, 4, 5], [4, 5, 2, 3]):
            self.assertEqual(board.board[i][j].can_be_taken, False)

    def test_restart(self):
        board = kit.Board(8)
        board.make_move((5, 3), BLACK)
        self.assertTrue(board.cell_count > 4)
        board.restart()
        self.assertTrue(board.cell_count == 4)
        self.assertEqual(board.board, kit.Board(8).board)


class TestCell(unittest.TestCase):
    def test_cell(self):
        for i in range(100):
            x = randint(0, 7)
            y = randint(0, 7)
            cell = kit.Cell(x, y)
            self.assertIs(cell.state, EMPTY)
            self.assertEqual(cell.x, x)
            self.assertEqual(cell.y, y)
            colour = choice([WHITE, BLACK])
            if colour == BLACK:
                cell.set_black()
                self.assertIs(cell.state, BLACK)
            else:
                cell.set_white()
                self.assertIs(cell.state, WHITE)
            self.assertIn(cell.get_state(), [EMPTY, WHITE, BLACK])

    def test_flip(self):
        for i in range(100):
            cell = kit.Cell(randint(0, 7), randint(0, 7))
            colour = choice([WHITE, BLACK])
            if colour == WHITE:
                cell.set_white()
                self.assertIs(cell.get_state(), WHITE)
                cell.flip()
                self.assertIs(cell.get_state(), BLACK)
            else:
                cell.set_black()
                self.assertIs(cell.get_state(), BLACK)
                cell.flip()
                self.assertIs(cell.get_state(), WHITE)


class TestGame(unittest.TestCase):
    def test_white_win(self):
        game = Game(4, True)
        self.assertTrue(not game.is_over())
        self.play_game_sequence(game, ['c1', 'b1', 'a3', 'd1'])
        self.assertTrue(game.is_over())
        self.assertEqual(game.WHITE_MSG, game.get_winner())

    def test_black_win(self):
        game = Game(3, True)
        self.assertTrue(not game.is_over())
        self.play_game_sequence(game, ['c2', 'c1', 'b1', 'a1'])
        self.assertTrue(game.is_over())
        self.assertEqual(game.BLACK_MSG, game.get_winner())

    def test_tie(self):
        game = Game(2, True)
        self.assertTrue(game.is_over())
        self.assertEqual(game.TIE_MSG, game.get_winner())

    @staticmethod
    def play_game_sequence(game, sequence):
        for move in sequence:
            game.next_move(move)


if __name__ == '__main__':
    unittest.main()
