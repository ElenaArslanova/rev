from unittest import TestCase
from random import choice
from game.game import Game
from game.montecarlo_ai import Node
from settings import WHITE


class TestNode(TestCase):
    def setUp(self):
        self.game = Game(3, Game.Modes.human_human, Game.DifficultyLevels.easy,
                         True, 5)
        first_move = (1, 2)
        first_state = Game.get_next_state((self.game.mover.board, WHITE),
                                               first_move)
        self.root_possible_moves = self.game.mover.board.get_moves(WHITE)
        self.root = Node(first_state, first_move,
                         len(self.root_possible_moves))

    def test_propagate_completion(self):
        root_moves_to_expand = len(self.root_possible_moves)
        self.assertTrue(self.root.moves_left_to_expand == root_moves_to_expand)
        state = self.game.get_next_state(self.root.state, (2,  1))
        child = Node(state, (2, 1), 3)
        self.root.add_child(child)
        self.assertTrue(child.moves_left_to_expand > 0)
        child_moves_to_expand = child.moves_left_to_expand
        child.propagate_completion()
        self.assertTrue(child.moves_left_to_expand ==
                        child_moves_to_expand - 1)
        self.assertTrue(self.root.moves_left_to_expand == root_moves_to_expand)


    def test_add_child(self):
        child = self.get_child(self.root)
        self.assertFalse(self.root.children)
        self.root.add_child(child)
        self.assertTrue(len(self.root.children) == 1)
        self.assertEqual(self.root.children[0], child)

    def test_has_children(self):
        child = self.get_child(self.root)
        self.assertFalse(child.has_children())
        self.root.add_child(child)
        self.assertTrue(self.root.has_children())

    def get_child(self, node):
        possible_moves = self.game.mover.board.get_moves(node.state[1])
        move = choice(possible_moves)
        state = Game.get_next_state(self.root.state, move)
        return Node(state, move, len(state[0].get_moves(state[1])))