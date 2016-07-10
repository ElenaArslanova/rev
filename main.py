from kit import Board
from player import HumanPlayer
from settings import *


class Game:
    def __init__(self):
        self.player_1 = HumanPlayer(WHITE)
        self.player_2 = HumanPlayer(BLACK)
        self.board = Board()

    def is_over(self):
        return self.board.cell_count == SIZE ** 2

    def run(self):
        self.board.print()
        while not self.is_over():
            move_1 = self.player_1.next_move(self.board)
            self.board.make_move(move_1, self.player_1.colour)
            print()
            self.board.print()
            move_2 = self.player_2.next_move(self.board)
            self.board.make_move(move_2, self.player_2.colour)
            print()
            self.board.print()


def get_colour_of_other_player(colour):
    if colour == WHITE:
        return BLACK
    return WHITE


if __name__ == 'main':
    game = Game()
    game.run()
