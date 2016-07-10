class Player:
    def __init__(self, colour):
        self.colour = colour

    def next_move(self, board):
        pass


class HumanPlayer(Player):
    def __init__(self, colour):
        super().__init__(colour)

    def next_move(self, board):
        move = None
        while move is None:
            player_input = input('Enter coordinates of your next move: ')
            try:
                if len(player_input) != 2:
                    raise ValueError("Invalid coordinates")
                x, y = player_input[0], player_input[1]
                move = self.parse_coordinates(x, y)
                possible_moves = [cell.get_coordinates() for cell in
                                  board.get_moves(self.colour)]
                if not possible_moves:
                    raise NoMovesError
                if move not in possible_moves:
                    raise ValueError("Invalid coordinates")
                return move

            except (ValueError, NoMovesError) as e:
                move = None
                print(e)

    @staticmethod
    def parse_coordinates(x, y):
        return int(y), ord(x) - ord('a')


class NoMovesError(Exception):
    pass
