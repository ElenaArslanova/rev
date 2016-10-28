from settings import EMPTY, MOVE, BLACK, WHITE

class AlphaBetaPruner:
    def __init__(self, cells, first_player, second_player):
        self.empty_cells = 0
        self.move = 1  # cells that can be taken
        self.white = 2
        self.black = 3
        self.first_player = first_player
        self.second_player = second_player
        self.infinity = 1.0e400
        self.state = self.make_state(cells)

    def make_state(self, cells):
        """
        :return: tuple (current_player, state)
        """
        results = {EMPTY: self.empty_cells, MOVE: self.empty_cells,
                   WHITE: self.white, BLACK: self.black}
        return self.first_player.colour, [results[cell.get_state()] for cell in cells]

    def search(self):
        """
        :return: move for the ai
        """
        depth = 0
        pass

    def max_value(self, depth, current_state, alpha, beta):
        """
        Finds the best possible move for the ai
        """
        pass

    def min_value(self, depth, state, alpha, beta):
        """
        Finds the best possible move for the human player
        """
        pass

    def evaluate(self, current_state, player_to_check):
        """
        :return: a positive value - the player wins, zero - a tie,
        a negative value - the opponent wins
        """
        player_state, state = current_state
        player = player_to_check
        opponent =  self.get_opponent(player)


    def get_opponent(self, player):
        return self.second_player if player is self.first_player else self.first_player

    def get_moves(self, player, opponent, state):
        pass

    # def mark_move(self, player, opponent, ):