from game import Game
from settings import *

def main():
    game = Game(SIZE, is_console_game=True)
    game.mover.board.print()
    while not game.is_over():
        player_input = input('Enter coordinates of your next move: ')
        try:
            if len(player_input) != 2:
                raise ValueError("Invalid coordinates")
            game.next_move(player_input)
            print()
            game.mover.board.print()
        except ValueError as e:
            print(e)
            game.repeat_player_move()
    print('The game is over! {}'.format(game.get_winner()))

if __name__ == '__main__':
    main()
