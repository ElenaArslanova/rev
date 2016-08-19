from settings import *


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
        self.board[SIZE // 2 - 1][SIZE // 2 - 1].set_black()
        self.board[SIZE // 2 - 1][SIZE // 2].set_white()
        self.board[SIZE // 2][SIZE // 2 - 1].set_white()
        self.board[SIZE // 2][SIZE // 2].set_black()

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
        opposite = self.get_colour_of_other_player(player_colour)
        next_move = self.get_next_move_in_direction(x, y, direction)
        if next_move is None:
            return
        if self.board[next_move['x']][next_move['y']].get_state() == opposite:
            while self.board[next_move['x']][next_move['y']].get_state() == opposite:
                next_move = self.get_next_move_in_direction(next_move['x'],
                                                            next_move['y'],
                                                            direction)
                if next_move is None:
                    return
            #print('before empty: x {} y {}'.format(next_move['x'], next_move['y']))
            if self.board[next_move['x']][next_move['y']].get_state() == EMPTY:
                self.board[next_move['x']][next_move['y']].can_be_taken = True

    def clear_moves(self):
        cells = (self.board[x][y] for x in range(SIZE) for y in range(SIZE))
        for cell in cells:
            if cell.can_be_taken:
                cell.can_be_taken = False

    def make_move(self, coordinates, player_colour):
        x, y = coordinates
        current_cell = self.board[x][y]
        if player_colour == WHITE:
            current_cell.set_white()
        else:
            current_cell.set_black()
        for direction in DIRECTIONS:
            start = self.get_next_move_in_direction(x, y, direction)
            # if not self.is_on_board(start['x'], start['y']):
            #     continue
            if start is None:
                continue
            cell = self.board[start['x']][start['y']]
            flip = []
            cancel_flipping = False
            while cell.get_state() != player_colour:
                if cell.get_state() == EMPTY:
                    cancel_flipping = True
                    break
                flip.append(cell)
                next_coord = self.get_next_move_in_direction(cell.x, cell.y,
                                                             direction)
                # if self.is_on_board(next_coord['x'], next_coord['y']):
                if next_coord is not None:
                    cell = self.board[next_coord['x']][next_coord['y']]
                else:
                    cancel_flipping = True
                    break
            if not cancel_flipping:
                for cell_to_flip in flip:
                    cell_to_flip.flip()
        self.cell_count += 1

    @staticmethod
    def get_colour_of_other_player(colour):
        if colour == WHITE:
            return BLACK
        return WHITE

    def get_next_move_in_direction(self, x, y, direction):
        """
        :return: coordinates of the next move, None if this move is not on the
        board
        """
        next_move = {'x': x + direction[0], 'y': y + direction[1]}
        if self.is_on_board(next_move['x'], next_move['y']):
            return next_move

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
