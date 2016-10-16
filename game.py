from itertools import cycle
from kit import Board
from mover import Mover, ConsoleMover
from player import Player
from settings import *

class Game:
    TIE_MSG = "It's a tie!"
    WHITE_MSG = 'White won!'
    BLACK_MSG = 'Black won!'

    def __init__(self, board_size, is_console_game):
        self.players = self.get_players()
        if is_console_game:
            self.mover = ConsoleMover(board_size)
        else:
            self.mover = Mover(board_size)

    def is_over(self):
        return (self.mover.board.cell_count == self.mover.board.size ** 2 or
                not self.mover.next_possible_moves)

    def next_move(self, coordinates):
        player = next(self.players)
        self.mover.next_move(player, coordinates)

    def repeat_player_move(self):
        next(self.players)

    def get_winner(self):
        white_count = 0
        black_count = 0
        for cell in self.mover.board.cells():
            if cell.state == WHITE:
                white_count += 1
            elif cell.state == BLACK:
                black_count += 1
        if white_count == black_count:
            return self.TIE_MSG
        elif white_count > black_count:
            return self.WHITE_MSG
        else:
            return self.BLACK_MSG

    def get_players(self):
        return cycle((Player(FIRST),
                        Player(Board.get_colour_of_other_player(FIRST))))

    def restart(self):
        self.players = self.get_players()
        self.mover.restart()

