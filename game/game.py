from itertools import cycle
from copy import deepcopy
from game.kit import Board
from game.mover import Mover
from game.player import HumanPlayer, AIPlayer, RandomAIPlayer
import settings as s
from enum import Enum


class Game:
    TIE_MSG = "It's a tie!"
    WHITE_MSG = 'White won!'
    BLACK_MSG = 'Black won!'
    Modes = Enum('Modes', 'human_human human_ai ai_human ai_ai',
                 module = __name__, qualname='Game.Modes')
    States = Enum('GameStates', 'human ai', module = __name__,
                  qualname='Game.States')
    DifficultyLevels = Enum('DifficultyLevels', 'easy normal hard',
                            module=__name__, qualname='Game.DifficultyLevels')
    REVERSING_MODES = (Modes.human_ai, Modes.ai_human)

    def __init__(self, board_size, mode, difficulty_level, is_console_game, time_for_move):
        self.mode = mode
        self.board_size = board_size
        self.difficulty_level = difficulty_level
        self.time_for_move = time_for_move
        self.is_console = is_console_game
        self.mover = Mover(board_size)
        self.players = self.get_players()
        self.current_player = None
        self.same_player_passing = False

    def is_over(self):
        return (self.mover.board.cell_count == self.mover.board.size ** 2 or
                not self.mover.board.someone_has_moves())

    def next_move(self, coordinates=None):
        try:
            player = next(self.players)
            self.current_player = player
            self.mover.next_move(player, coordinates)
            self.reverse_mode_if_needed()
            self.check_next_player_pass()
        except ValueError:
            if not self.mover.board.has_moves(self.current_player.colour):
                self.same_player_passing = True
                next(self.players)
                self.pass_move()
            else:
                self.repeat_player_move()

    def reverse_mode_if_needed(self):
        if self.mode in self.REVERSING_MODES:
            self.reverse_game_state()

    def check_next_player_pass(self):
        cur_player = self.current_player
        next_player_colour = Board.get_colour_of_other_player(cur_player.colour)
        if not self.mover.board.has_moves(next_player_colour):
            self.pass_move()

    def repeat_player_move(self):
        next(self.players)

    def skip_player(self):
        next(self.players)
        self.reverse_mode_if_needed()

    def pass_move(self):
        if self.current_player is None:
            player_colour = Board.get_colour_of_other_player(s.FIRST)
        else:
            player_colour = self.current_player.colour
        if self.same_player_passing:
            self.mover.pass_move(player_colour)
            self.same_player_passing = False
        else:
            self.mover.pass_move(Board.get_colour_of_other_player(player_colour))
        self.skip_player()

    def get_winner_message(self):
        winner = self.get_winner(self.mover.board)
        if winner == s.WHITE:
            return self.WHITE_MSG
        elif winner == s.BLACK:
            return self.BLACK_MSG
        else:
            return self.TIE_MSG

    def get_players(self):
        first = s.FIRST
        second = Board.get_colour_of_other_player(first)
        first_human_player = HumanPlayer(first, self.board_size, self.is_console)
        second_human_player = HumanPlayer(second, self.board_size, self.is_console)
        if self.difficulty_level == self.DifficultyLevels.easy:
            first_ai_player = RandomAIPlayer(first, self)
            second_ai_player = RandomAIPlayer(second, self)
        else:
            first_ai_player = AIPlayer(first, self, self.difficulty_level, time_for_move=self.time_for_move)
            second_ai_player = AIPlayer(second, self, self.difficulty_level, time_for_move=self.time_for_move)
        if self.mode == self.Modes.human_human:
            self.game_state = self.States.human
            players = cycle((first_human_player, second_human_player))
        elif self.mode == self.Modes.human_ai:
            self.game_state = self.States.human
            players = cycle((first_human_player, second_ai_player))
        elif self.mode == self.Modes.ai_human:
            self.game_state = self.States.ai
            players = cycle((first_ai_player, second_human_player))
        else:
            self.game_state = self.States.ai
            players = cycle((first_ai_player, second_ai_player))
        return players

    def reverse_game_state(self):
        if self.game_state == self.States.human:
            self.game_state = self.States.ai
        else:
            self.game_state = self.States.human

    @staticmethod
    def get_next_state(state, move_coordinates):
        board, player = deepcopy(state[0]), state[1]
        if move_coordinates is not None:
            board.make_move(move_coordinates, player)
        return board, Board.get_colour_of_other_player(player)

    @staticmethod
    def get_previous_state(state, last_move_coordinates):
        board, player = deepcopy(state[0]), state[1]
        flipped_cells = board.move_flipped_cells[last_move_coordinates]
        for cell in flipped_cells:
            cell.flip()
        board.board[last_move_coordinates[0]][last_move_coordinates[1]].set_empty()
        return board, Board.get_colour_of_other_player(player)

    def get_current_state(self):
        return (deepcopy(self.mover.board),
                Board.get_colour_of_other_player(self.current_player.colour))

    def get_winner(self, board):
        white_count, black_count = self.mover.board.count_cells()
        if (white_count + black_count != board.size ** 2 and
                board.someone_has_moves()):
            return None
        if white_count == black_count:
            return s.TIE
        elif white_count > black_count:
            return s.WHITE
        else:
            return s.BLACK

    def restart(self):
        self.players = self.get_players()
        self.mover.restart()

    def undo(self):
        if self.mover.current_move_number == 0:
            return
        opponent_last_move = self.mover.move_back()
        opponent_previous_state = self.get_previous_state(self.get_current_state(),
                                                 opponent_last_move)
        last_move = self.mover.move_back()
        previous_state = self.get_previous_state(opponent_previous_state, last_move)
        self.mover.update_board(previous_state[0],
                        Board.get_colour_of_other_player(previous_state[1]))

    def redo(self):
        if self.mover.current_move_number == len(self.mover.moves):
            return
        next_move = self.mover.move_forward()
        next_state = self.get_next_state(self.get_current_state(), next_move)
        opponent_next_move = self.mover.move_forward()
        opponent_next_state = self.get_next_state(next_state,
                                                  opponent_next_move)
        self.mover.update_board(opponent_next_state[0],
                    Board.get_colour_of_other_player(opponent_next_state[1]))
