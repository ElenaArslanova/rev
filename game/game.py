from itertools import cycle
from copy import deepcopy
from game.kit import Board
from game.mover import Mover
from game.player import HumanPlayer, AIPlayer
import settings as s


class Game:
    TIE_MSG = "It's a tie!"
    WHITE_MSG = 'White won!'
    BLACK_MSG = 'Black won!'
    REVERSING_MODES = (s.Modes.human_ai, s.Modes.ai_human)

    def __init__(self, board_size, mode, is_console_game):
        self.mode = mode
        self.board_size = board_size
        self.is_console = is_console_game
        self.mover = Mover(board_size)
        self.players = self.get_players()

    def is_over(self):
        return (self.mover.board.cell_count == self.mover.board.size ** 2 or
                not self.mover.board.someone_has_moves())

    def next_move(self, coordinates=None):
        try:
            player = next(self.players)
            self.mover.next_move(player, coordinates)
            self.reverse_mode_if_needed()
        except ValueError:
            self.repeat_player_move()
        except Exception as e:
            print(e)

    def reverse_mode_if_needed(self):
        if self.mode in self.REVERSING_MODES:
            self.reverse_game_state()

    def check_player_pass(self):
        player = self.get_current_player()
        if not self.mover.board.has_moves(player.colour):
            self.mover.pass_move(player)
            self.skip_player()

    def repeat_player_move(self):
        next(self.players)

    def skip_player(self):
        next(self.players)
        self.reverse_mode_if_needed()

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
        first_ai_player = AIPlayer(first, self)
        second_ai_player = AIPlayer(second, self)
        if self.mode == s.Modes.human_human:
            self.game_state = s.States.human
            players = cycle((first_human_player, second_human_player))
        elif self.mode == s.Modes.human_ai:
            self.game_state = s.States.human
            players = cycle((first_human_player, second_ai_player))
        elif self.mode == s.Modes.ai_human:
            self.game_state = s.States.ai
            players = cycle((first_ai_player, second_human_player))
        else:
            self.game_state = s.States.ai
            players = cycle((first_ai_player, second_ai_player))
        return players

    def reverse_game_state(self):
        if self.game_state == s.States.human:
            self.game_state = s.States.ai
        else:
            self.game_state = s.States.human

    def get_current_player(self):
        current = next(self.players)
        self.repeat_player_move()
        return current

    # @staticmethod
    # def get_current_state_player(state):
    #     return state[-1]

    @staticmethod
    def get_next_state(state, move_coordinates):
        board, player = deepcopy(state[0]), state[1]
        if move_coordinates is not None:
            board.make_move(move_coordinates, player)
        return (board, Board.get_colour_of_other_player(player))

    # def get_current_state(self):
    #     return (deepcopy(self.mover.board), self.get_current_player())

    def get_winner(self, board):
        white_count, black_count = self.count_cells(board)
        if (white_count + black_count != board.size ** 2 and
                board.someone_has_moves()):
            return None
        if white_count == black_count:
            return s.TIE
        elif white_count > black_count:
            return s.WHITE
        else:
            return s.BLACK



    @staticmethod
    def count_cells(board):
        white_count = 0
        black_count = 0
        for cell in board.cells():
            if cell.state == s.WHITE:
                white_count += 1
            elif cell.state == s.BLACK:
                black_count += 1
        return (white_count, black_count)

    def restart(self):
        self.players = self.get_players()
        self.mover.restart()

