from enum import Enum

MOVE, EMPTY, WHITE, BLACK, TIE = 'Move', '.', 'O', 'X', 'Tie'
SIZE = 8
FIRST = WHITE
NORTH, NORTHEAST, NORTHWEST = [0, 1], [1, 1], [-1, 1]
SOUTH, SOUTHEAST, SOUTHWEST = [0, -1], [1, -1], [-1, -1]
EAST, WEST = [1, 0], [-1, 0]

DIRECTIONS = (NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST,
              NORTHWEST)
Modes = Enum('Modes', 'human_human human_ai ai_human ai_ai')

States = Enum('GameStates', 'human ai')

IMG_SIZE = 60