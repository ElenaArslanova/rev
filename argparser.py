import argparse
from game.game import Game


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=positive, default=8,
                        help='Размер доски')
    parser.add_argument('-l', '--level', choices=['easy', 'normal', 'hard'],
                        help='Уровень сложности', required=True)
    parser.add_argument('-t', '--time', type=positive, default=5,
                        help='Время на ход')
    subparsers = parser.add_subparsers(dest='mode', help='Режим игры')
    subparsers.required = True
    mode_parser = subparsers.add_parser('mode')
    mode_parser.add_argument('-ha', '--human_ai', action='store_true',
                             help='Человек против искусственного интеллекта')
    mode_parser.add_argument('-hh', '--human_human', action='store_true',
                             help='Человек против человека')
    mode_parser.add_argument('-ah', '--ai_human', action='store_true',
                             help='Искусственный интеллект против человека')
    mode_parser.add_argument(
        '-aa', '--ai_ai', action='store_true',
        help='Искусственный интеллект против искусственного интеллекта')
    return parser


def positive(value):
    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError('%s is invalid positive int value' %
                                         value)
    return int_value


def get_mode(namespace):
    if namespace.ai_ai:
        return Game.Modes.ai_ai
    elif namespace.ai_human:
        return Game.Modes.ai_human
    elif namespace.human_ai:
        return Game.Modes.human_ai
    else:
        return Game.Modes.human_human


def get_difficulty_level(namespace):
    if namespace.level == 'easy':
        return Game.DifficultyLevels.easy
    elif namespace.level == 'normal':
        return Game.DifficultyLevels.normal
    else:
        return Game.DifficultyLevels.hard
