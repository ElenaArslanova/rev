from settings import IMG_SIZE
from random import choice
from game.montecarlo_ai import MonteCarloAI


class Player:
    def __init__(self, colour):
        self.colour = colour

    def next_move(self, coordinates):
        pass


class HumanPlayer(Player):
    def __init__(self, colour, board_size, is_console):
        super().__init__(colour)
        self.board_size = board_size
        if is_console:
            self.parse_coordinates = self.parse_console_coordinates

    def next_move(self, coordinates):
        return self.parse_coordinates(coordinates)

    @staticmethod
    def parse_coordinates(coordinates):
        x, y = coordinates.x(), coordinates.y()
        return y // IMG_SIZE, x // IMG_SIZE

    def parse_console_coordinates(self, coordinates):
        x, y = coordinates[0], coordinates[1]
        return self.board_size - int(y), ord(x) - ord('a')


class AIPlayer(Player):
    def __init__(self, colour, game, difficulty_level, time_for_move):
        super().__init__(colour)
        self.ai = MonteCarloAI(game, colour, difficulty_level, time=time_for_move)
        self.game = game

    def next_move(self, coordinates):
        return self.ai.get_move((self.game.mover.board, self.colour))


class RandomAIPlayer(Player):
    def __init__(self, colour, game):
        super().__init__(colour)
        self.colour = colour
        self.game = game

    def next_move(self, coordinates):
        return choice(self.game.mover.board.get_moves(self.colour))