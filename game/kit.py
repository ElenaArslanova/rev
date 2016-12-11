import settings as s


class Cell:
    def __init__(self, x, y):
        self.state = s.EMPTY
        self.can_be_taken = False
        self.x = x
        self.y = y

    def set_black(self):
        self.state = s.BLACK

    def set_white(self):
        self.state = s.WHITE

    def set_empty(self):
        self.state = s.EMPTY

    def get_state(self):
        return self.state

    def flip(self):
        if self.state == s.BLACK:
            self.state = s.WHITE
        elif self.state == s.WHITE:
            self.state = s.BLACK
        else:
            raise ValueError("Cell in {} state can't be flipped".format(
                self.state.lower()))

    def get_coordinates(self):
        return self.x, self.y

    def __str__(self):
        return self.state

    def __repr__(self):
        return self.state

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y))


class Board:
    def __init__(self, size):
        self.size = size
        self.board = []
        self.move_flipped_cells = {}
        for x in range(self.size):
            self.board.append([])
            for y in range(self.size):
                self.board[x].append(Cell(x, y))
        self.set_start_cells()
        self.cell_count = 4

    def set_start_cells(self):
        self.board[self.size // 2 - 1][self.size // 2 - 1].set_black()
        self.board[self.size // 2 - 1][self.size // 2].set_white()
        self.board[self.size // 2][self.size // 2 - 1].set_white()
        self.board[self.size // 2][self.size // 2].set_black()

    def get_moves(self, player_colour):
        self.mark_valid_moves(player_colour)
        cells = (self.board[x][y] for x in range(self.size)
                 for y in range(self.size))
        moves = [cell.get_coordinates() for cell in cells if cell.can_be_taken]
        self.clear_moves()
        return moves

    def mark_valid_moves(self, player_colour):
        cells = (self.board[x][y] for x in range(self.size)
                 for y in range(self.size))
        for cell in cells:
            if cell.get_state() == player_colour:
                for direction in s.DIRECTIONS:
                    self.mark_move_in_direction(player_colour, cell, direction)

    def mark_move_in_direction(self, player_colour, cell, direction):
        x, y = cell.x, cell.y
        opposite = self.get_colour_of_other_player(player_colour)
        next_move = self.get_next_move_in_direction(x, y, direction)
        if next_move is None:
            return
        if self.board[next_move['x']][next_move['y']].get_state() == opposite:
            next_x = next_move['x']
            next_y = next_move['y']
            while self.board[next_x][next_y].get_state() == opposite:
                next_move = self.get_next_move_in_direction(next_move['x'],
                                                            next_move['y'],
                                                            direction)
                if next_move is None:
                    return
                next_x = next_move['x']
                next_y = next_move['y']
            if self.board[next_x][next_y].get_state() == s.EMPTY:
                self.board[next_x][next_y].can_be_taken = True

    def clear_moves(self):
        cells = (self.board[x][y] for x in range(self.size)
                 for y in range(self.size))
        for cell in cells:
            if cell.can_be_taken:
                cell.can_be_taken = False

    def make_move(self, coordinates, player_colour):
        x, y = coordinates
        current_cell = self.board[x][y]
        if player_colour == s.WHITE:
            current_cell.set_white()
        else:
            current_cell.set_black()
        all_flips = []
        for direction in s.DIRECTIONS:
            start = self.get_next_move_in_direction(x, y, direction)
            if start is None:
                continue
            cell = self.board[start['x']][start['y']]
            flip = []
            cancel_flipping = False
            while cell.get_state() != player_colour:
                if cell.get_state() == s.EMPTY:
                    cancel_flipping = True
                    break
                flip.append(cell)
                next_coord = self.get_next_move_in_direction(cell.x, cell.y,
                                                             direction)
                if next_coord is not None:
                    cell = self.board[next_coord['x']][next_coord['y']]
                else:
                    cancel_flipping = True
                    break
            if not cancel_flipping:
                for cell_to_flip in flip:
                    cell_to_flip.flip()
                all_flips.extend(flip)
        if coordinates not in self.move_flipped_cells:
            self.move_flipped_cells[coordinates] = all_flips
        self.cell_count += 1

    @staticmethod
    def get_colour_of_other_player(colour):
        if colour == s.WHITE:
            return s.BLACK
        return s.WHITE

    def get_next_move_in_direction(self, x, y, direction):
        """
        :return: coordinates of the next move, None if this move is not on the
        board
        """
        next_move = {'x': x + direction[0], 'y': y + direction[1]}
        if self.is_on_board(next_move['x'], next_move['y']):
            return next_move

    def is_on_board(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def someone_has_moves(self):
        return self.has_moves(s.BLACK) or self.has_moves(s.WHITE)

    def has_moves(self, colour):
        return len(self.get_moves(colour)) > 0

    def restart(self):
        for x in range(self.size):
            for y in range(self.size):
                self.board[x][y] = Cell(x, y)
        self.set_start_cells()
        self.cell_count = 4

    def print(self):
        for x in range(self.size):
            print('{}{}'.format(self.size - x,
                                ''.join(str(cell) for cell in self.board[x])))
        print(' {}'.format(''.join([chr(i + ord('a'))
                                    for i in range(self.size)])))

    def cells(self):
        for x in range(self.size):
            for cell in self.board[x]:
                yield cell

    def count_cells(self):
        white_count = 0
        black_count = 0
        for cell in self.cells():
            if cell.state == s.WHITE:
                white_count += 1
            elif cell.state == s.BLACK:
                black_count += 1
        return white_count, black_count

    def update_cell_count(self):
        self.cell_count = sum(self.count_cells())

    def __hash__(self):
        board_string = ''.join(cell.state for row in self.board
                               for cell in row)
        return hash(board_string)

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        cells_pairs = zip(self.cells(), other.cells())
        for cell1, cell2 in cells_pairs:
            if cell1 != cell2:
                return False
        return True
