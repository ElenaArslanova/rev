import os
import sys
import unittest
from copy import deepcopy
from random import randint, choice

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from game import kit
from game.game import Game
import settings as s


class TestBoard(unittest.TestCase):
    def test_valid_moves_corner(self):
        board = kit.Board(8)
        board.board[1][7].set_black()
        board.board[2][7].set_white()
        board.mark_valid_moves(s.WHITE)
        self.assertEqual(board.board[0][7].can_be_taken, True)

    def test_clear_moves(self):
        board = kit.Board(8)
        board.mark_valid_moves(s.BLACK)
        for i, j in zip([2, 3, 4, 5], [4, 5, 2, 3]):
            self.assertEqual(board.board[i][j].can_be_taken, True)
        board.clear_moves()
        for i, j in zip([2, 3, 4, 5], [4, 5, 2, 3]):
            self.assertEqual(board.board[i][j].can_be_taken, False)

    def test_restart(self):
        board = kit.Board(8)
        board.make_move((5, 3), s.BLACK)
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
            self.assertIs(cell.state, s.EMPTY)
            self.assertEqual(cell.x, x)
            self.assertEqual(cell.y, y)
            colour = choice([s.WHITE, s.BLACK])
            if colour == s.BLACK:
                cell.set_black()
                self.assertIs(cell.state, s.BLACK)
            else:
                cell.set_white()
                self.assertIs(cell.state, s.WHITE)
            self.assertIn(cell.get_state(), [s.EMPTY, s.WHITE, s.BLACK])

    def test_flip(self):
        for i in range(100):
            cell = kit.Cell(randint(0, 7), randint(0, 7))
            colour = choice([s.WHITE, s.BLACK])
            if colour == s.WHITE:
                cell.set_white()
                self.assertIs(cell.get_state(), s.WHITE)
                cell.flip()
                self.assertIs(cell.get_state(), s.BLACK)
            else:
                cell.set_black()
                self.assertIs(cell.get_state(), s.BLACK)
                cell.flip()
                self.assertIs(cell.get_state(), s.WHITE)


class TestGame(unittest.TestCase):
    def test_white_win(self):
        game = Game(4, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        self.assertTrue(not game.is_over())
        self.play_game_sequence(game, ['d2', 'd3', 'd4', 'b1', 'a3', 'b4',
                                       'a4', 'a2', 'c4'])
        self.assertTrue(game.is_over())
        self.assertEqual(game.WHITE_MSG, game.get_winner_message())

    def test_black_win(self):
        game = Game(3, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        self.assertTrue(not game.is_over())
        self.play_game_sequence(game, ['b1', 'a1', 'c3', 'c1'])
        self.assertTrue(game.is_over())
        self.assertEqual(game.BLACK_MSG, game.get_winner_message())

    def test_tie(self):
        game = Game(2, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        self.assertTrue(game.is_over())
        self.assertEqual(game.TIE_MSG, game.get_winner_message())

    def test_game_is_over(self):
        game1 = Game(3, Game.Modes.human_human, Game.DifficultyLevels.easy,
                     True, 5)
        self.play_game_sequence(game1, ['b1', 'a1', 'c1', 'c3'])
        self.assertTrue(game1.is_over())
        game2 = Game(2, Game.Modes.human_human, Game.DifficultyLevels.easy,
                     True, 5)
        self.assertTrue(game2.is_over())

    def test_get_next_state(self):
        game = Game(3, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        state = (game.mover.board, s.WHITE)
        self.assertEqual(game.mover.board, state[0])
        next_state = game.get_next_state(state, (2, 1))
        self.assertNotEqual(game.mover.board, next_state[0])
        game.mover.board.make_move((2, 1), s.WHITE)
        self.assertEqual(game.mover.board, next_state[0])

    def test_get_previous_state(self):
        game = Game(4, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        state = (game.mover.board, s.WHITE)
        my_state = game.get_next_state(state, (1, 0))
        game.next_move('a3')
        self.assertEqual(game.get_current_state(), my_state)
        opp_state = game.get_next_state(my_state, (2, 0))
        game.next_move('a2')
        self.assertEqual(game.get_current_state(), opp_state)
        my_prev_state = game.get_previous_state(opp_state, (2, 0))
        self.assertEqual(my_state, my_prev_state)

    def test_skip_player(self):
        game = Game(4, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        game.next_move('c1')
        self.assertEqual(game.current_player.colour, s.WHITE)
        game.skip_player()
        game.next_move('a2')
        self.assertEqual(game.current_player.colour, s.WHITE)

    def test_repeat_player_move(self):
        game = Game(3, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        player = next(game.players)
        self.assertEqual(player.colour, s.WHITE)
        game.repeat_player_move()
        self.assertEqual(next(game.players), player)

    def test_move_is_repeated(self):
        game = Game(3, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        self.assertIsNone(game.current_player)
        game.next_move('b1')
        self.assertIsNotNone(game.current_player)
        self.assertEqual(game.current_player.colour, s.WHITE)
        game.next_move('a1')
        self.assertEqual(game.current_player.colour, s.BLACK)
        game.next_move('c3')
        self.assertEqual(game.current_player.colour, s.BLACK)

    def test_undo_redo(self):
        game = Game(4, Game.Modes.human_human, Game.DifficultyLevels.easy,
                    True, 5)
        initial_state = (deepcopy(game.mover.board), s.WHITE)
        game.next_move('a3')
        game.next_move('a2')
        my_state = game.get_current_state()
        game.undo()
        self.assertEqual(initial_state, game.get_current_state())
        game.redo()
        self.assertEqual(my_state, game.get_current_state())
        game.undo()
        self.assertEqual(initial_state, game.get_current_state())

    @staticmethod
    def play_game_sequence(game, sequence):
        for move in sequence:
            game.next_move(move)


if __name__ == '__main__':
    unittest.main()
