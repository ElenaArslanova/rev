from game.game import Game
from settings import States
import argparser

def main():
    reversi_parser = argparser.create_parser()
    namespace = reversi_parser.parse_args()
    game = Game(namespace.size, mode=argparser.get_mode(namespace),
                difficulty_level=argparser.get_difficulty_level(namespace),
                is_console_game=True)
    game.mover.board.print()
    while not game.is_over():
        try:
            if game.game_state == States.human:
                player_input = input('Enter coordinates of your next move: ')
                if len(player_input) != 2:
                    raise ValueError("Invalid coordinates")
                game.next_move(player_input)
            else:
                game.next_move()
            print()
            game.mover.board.print()
        except ValueError as e:
            print(e)
            game.repeat_player_move()
    print('The game is over! {}'.format(game.get_winner_message()))

if __name__ == '__main__':
    main()
