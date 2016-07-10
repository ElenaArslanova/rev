EMPTY, WHITE, BLACK = '.', 'O', 'X'
SIZE = 8
NORTH, NORTHEAST, NORTHWEST = [0, 1], [1, 1], [-1, 1]
SOUTH, SOUTHEAST, SOUTHWEST = [0, -1], [1, -1], [-1, -1]
EAST, WEST = [1, 0], [-1, 0]

DIRECTIONS = (NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST,
              NORTHWEST)


class Cell:
    def __init__(self, x, y):
        self.state = EMPTY
        #self.flipped = False
        self.can_be_taken = False
        self.x = x
        self.y = y

    def set_black(self):
        self.state = BLACK

    def set_white(self):
        self.state = WHITE

    def get_state(self):
        return self.state

    def flip(self):
        if self.state == BLACK:
            self.state = WHITE
        elif self.state == WHITE:
            self.state = BLACK
        else:
            raise ValueError("Cell in {} state can't be flipped".format(self.state.lower()))
        #self.flipped = True

    # def reset_flip(self):
    #     self.flipped = False

    def get_coordinates(self):
        return self.x, self.y

    def __str__(self):
        return self.state

    def __repr__(self):
        return self.state


class Board:
    def __init__(self):
        self.board = []
        for x in range(SIZE):
            self.board.append([])
            for y in range(SIZE):
                self.board[x].append(Cell(x, y))
        self.set_start_cells()
        self.cell_count = 4

    def set_start_cells(self):
        self.board[int(SIZE / 2) - 1][int(SIZE / 2) - 1].set_black()
        self.board[int(SIZE / 2) - 1][int(SIZE / 2)].set_white()
        self.board[int(SIZE / 2)][int(SIZE / 2) - 1].set_white()
        self.board[int(SIZE / 2)][int(SIZE / 2)].set_black()

    def get_moves(self, player_colour):
        self.mark_valid_moves(player_colour)
        cells = (self.board[x][y] for x in range(SIZE) for y in range(SIZE))
        moves = [cell for cell in cells if cell.can_be_taken]
        self.clear_moves()
        return moves

    def mark_valid_moves(self, player_colour):
        cells = (self.board[x][y] for x in range(SIZE) for y in range(SIZE))
        for cell in cells:
            if cell.get_state() == player_colour:
                for direction in DIRECTIONS:
                    self.mark_move_in_direction(player_colour, cell, direction)

    def mark_move_in_direction(self, player_colour, cell, direction):
        x, y = cell.x, cell.y
        opposite = get_colour_of_other_player(player_colour)
        if not self.is_on_board(x, y):
            return
        next_move = self.get_next_move_in_direction(x, y, direction)
        if self.board[next_move['x']][next_move['y']].get_state() == opposite:
            while self.board[next_move['x']][next_move['y']].get_state() == opposite:
                if not self.is_on_board(next_move['x'], next_move['y']):
                    break
                else:
                    next_move = self.get_next_move_in_direction(next_move['x'],
                                                                next_move['y'],
                                                                direction)
            if self.board[next_move['x']][next_move['y']].get_state() == EMPTY:
                self.board[next_move['x']][next_move['y']].can_be_taken = True

    def clear_moves(self):
        cells = (self.board[x][y] for x in range(SIZE) for y in range(SIZE))
        for cell in cells:
            if cell.can_be_taken:
                cell.can_be_taken = False

    def make_move(self, coordinates, player_colour):
        x, y = coordinates
        moves = [cell.get_coordinates()
                 for cell in self.get_moves(player_colour)]
        if coordinates not in moves or not self.is_on_board(x, y):
            raise ValueError
        opposite = get_colour_of_other_player(player_colour)
        current_cell = self.board[x][y]
        if player_colour == WHITE:
            current_cell.set_white()
        else:
            current_cell.set_black()
        for direction in DIRECTIONS:
            start = self.get_next_move_in_direction(x, y, direction)
            cell = self.board[start['x']][start['y']]
            flip = []
            while cell.get_state() != EMPTY:
                if cell.get_state() != player_colour:
                    flip.append(cell)
                    next_coord = self.get_next_move_in_direction(cell.x,
                                                                 cell.y,
                                                                 direction)
                    cell = self.board[next_coord['x']][next_coord['y']]
                    if not self.is_on_board(cell.x, cell.y):
                        break
                else:
                    break
            for cell_to_flip in flip:
                cell_to_flip.flip()
        self.cell_count += 1

    @staticmethod
    def get_next_move_in_direction(x, y, direction):
        return {'x': x + direction[0], 'y': y + direction[1]}

    @staticmethod
    def is_on_board(x, y):
        return 0 <= x < SIZE and 0 <= y < SIZE

    def reset(self):
        for x in range(SIZE):
            for y in range(SIZE):
                self.board[x][y] = Cell(x, y)
        self.set_start_cells()

    def print(self):
        for x in range(SIZE):
            print(''.join(str(cell) for cell in self.board[x]))


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


class NoMovesError(Exception):
    pass


def get_colour_of_other_player(colour):
    if colour == WHITE:
        return BLACK
    return WHITE

game = Game()
game.run()
