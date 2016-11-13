import argparse
from settings import Modes

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=int, default=8, help='Размер доски')
    subparsers = parser.add_subparsers(dest='mode', help='Режим игры')
    subparsers.required = True
    mode_parser = subparsers.add_parser('mode')
    mode_parser.add_argument('-ha', '--human_ai', action='store_true',
                             help='Человек против искусственного интеллекта')
    mode_parser.add_argument('-hh', '--human_human', action='store_true',
                             help='Человек против человека')
    mode_parser.add_argument('-ah', '--ai_human', action = 'store_true',
                             help='Искусственный интеллект против человека')
    mode_parser.add_argument('-aa', '--ai_ai', action = 'store_true',
            help='Искусственный интеллект против искусственного интеллекта')
    return  parser

def get_mode(namespace):
    if namespace.ai_ai:
        return Modes.ai_ai
    elif namespace.ai_human:
        return Modes.ai_human
    elif namespace.human_ai:
        return Modes.human_ai
    else:
        return Modes.human_human