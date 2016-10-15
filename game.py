from itertools import cycle
from kit import Board
from mover import Mover, ConsoleMover
from player import Player
from settings import *

class Game:
    def __init__(self, is_console_game):
        self.players = self.get_players()
        if is_console_game:
            self.mover = ConsoleMover()
        else:
            self.mover = Mover()

    def is_over(self):
        return (self.mover.board.cell_count == SIZE ** 2 or
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
            return "It's a tie!"
        elif white_count > black_count:
            return 'White won!'
        else:
            return 'Black won!'

    def get_players(self):
        return cycle((Player(FIRST),
                        Player(Board.get_colour_of_other_player(FIRST))))

    def restart(self):
        self.players = self.get_players()
        self.mover.restart()

