from unittest import TestCase
from game.game import Game
from game.montecarlo_ai import MonteCarloAI, Node
from settings import WHITE


class TestMonteCarloAI(TestCase):
    def setUp(self):
        self.game = Game(3, Game.Modes.human_human, Game.DifficultyLevels.hard,
                         True, 5)
        self.ai = MonteCarloAI(self.game, WHITE, Game.DifficultyLevels.hard)
        first_move = (1, 2)
        first_state = Game.get_next_state((self.game.mover.board, WHITE),
                                          first_move)
        self.root_possible_moves = self.game.mover.board.get_moves(WHITE)
        self.root = Node(first_state, first_move,
                         len(self.root_possible_moves))

    def test_get_best_move(self):
        node = Node(self.root.state, (1, 2), 2)
        children = [Node(node.state, (2, 3), 1), Node(node.state, (2, 1), 2)]
        children[0].plays, children[0].wins = 3, 2
        children[1].plays, children[1].wins = 2, 2
        for child in children:
            node.add_child(child)
        self.assertEqual(self.ai.get_best_move(node), children[0].move)
        node.children[0].plays, node.children[0].wins = 2, 1
        self.assertEqual(self.ai.get_best_move(node), children[1].move)

    def test_back_propagate(self):
        node = Node(self.root.state, (1, 2), 2)
        child = Node(node.state, (2, 3), 1)
        child.plays, child.wins = 2, 1
        node.add_child(child)
        self.assertTrue(node.plays == 0)
        self.assertTrue(node.wins == 0)
        self.ai.back_propagate(child, 1)
        self.assertTrue(child.plays == 3)
        self.assertTrue(child.wins == 2)
        self.assertTrue(node.plays == 1)
        self.assertTrue(node.wins == 1)


    def test_get_best_child(self):
        children  = [Node(self.game.get_next_state(self.root.state, (1, 2)),
                      (1, 2), 3),
                     Node(self.game.get_next_state(self.root.state, (2, 1)),
                      (2, 1), 3)]
        children[0].plays, children[0].wins = 2, 1
        children[1].plays, children[1].wins = 1, 0
        self.root.plays = 3
        for child in children:
            self.root.add_child(child)
        self.assertEqual(self.ai.get_best_child(self.root), children[1])