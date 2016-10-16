from settings import *
from kit import Board

class Mover:
    def __init__(self, board_size):
        self.board = Board(board_size)
        self.next_possible_moves = self.get_start_possible_moves()

    def get_next_move(self, player, coordinates):
        move = self.parse_coordinates(coordinates)
        if move not in self.next_possible_moves:
            raise ValueError('Invalid coordinates')
        return move

    def next_move(self, player, coordinates):
        move = self.get_next_move(player, coordinates)
        self.board.make_move(move, player.colour)
        self.next_possible_moves = self.get_possible_moves(
            Board.get_colour_of_other_player(player.colour))

    def get_possible_moves(self, player_colour):
        return [cell.get_coordinates() for cell in
                                  self.board.get_moves(player_colour)]

    def restart(self):
        self.board.restart()
        self.next_possible_moves = self.get_start_possible_moves()

    def get_start_possible_moves(self):
        return self.get_possible_moves(FIRST)

    def parse_coordinates(self, coordinates):
        x, y = coordinates.x(), coordinates.y()
        return y// IMG_SIZE, x // IMG_SIZE

class ConsoleMover(Mover):
    def __init__(self, board_size):
        super().__init__(board_size)

    def parse_coordinates(self, coordinates):
        x, y = coordinates[0], coordinates[1]
        return self.board.size - int(y), ord(x) - ord('a')
