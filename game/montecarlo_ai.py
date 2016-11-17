from copy import deepcopy
from random import choice
import time
from math import log, sqrt
from game import kit

class MonteCarloAI:
    def __init__(self, game, colour, **kwargs):
        self.colour = colour
        self.game = game
        self.simulation_time = kwargs.get('time', 1)
        self.state_node = {}

    def get_move(self, state):
        state = deepcopy(state)
        move = self.monte_carlo_search(state)
        return move

    def monte_carlo_search(self, state):
        results = {}
        root = None
        if state in self.state_node:
            root = self.state_node[state]
        else:
            children_amount = len(state[0].get_moves(state[1]))
            if (not self.game.get_winner(state[0]) == self.colour
                and children_amount == 0):
                children_amount = 1
            root = Node(state, None, children_amount)

        root.parent = None
        start = time.time()
        while (time.time() - start < self.simulation_time
               and root.moves_left_to_expand > 0):
            selected_node = self.select_node(root)
            result = self.run_simulation(selected_node.state)
            self.back_propagate(selected_node, result)
        for child in root.children:
            wins, plays = child.get_wins_and_plays()
            position = child.move
            results[position] = (wins, plays)
        return self.get_best_move(root)

    @staticmethod
    def get_best_move(node):
        most_plays = -float('inf')
        best_wins = -float('inf')
        best_moves = []
        for child in node.children:
            wins, plays = child.get_wins_and_plays()
            if plays > most_plays:
                most_plays = plays
                best_moves = [child.move]
                best_wins = wins
            elif plays == most_plays:
                if wins > best_wins:
                    best_wins = wins
                    best_moves = [child.move]
                elif wins == best_wins:
                    best_moves.append(child.move)
        return choice(best_moves)

    @staticmethod
    def back_propagate(node, delta):
        while node.parent is not None:
            node.plays += 1
            node.wins += delta
            node = node.parent

        node.plays += 1
        node.wins += delta

    def select_node(self, root):
        current_node = root
        while root.moves_left_to_expand > 0:
            possible_moves = current_node.state[0].get_moves(current_node.state[1])
            if not possible_moves:
                if self.game.get_winner(current_node.state[0]) == current_node.state[1]:
                    current_node.propagate_completion()
                    return current_node
                else:
                    next_state = self.game.get_next_state(current_node.state,
                                                          None)
                    pass_node = Node(next_state, None, 1)
                    current_node.add_child(pass_node)
                    self.state_node[next_state] = pass_node
                    current_node = pass_node
                    continue
            elif len(current_node.children) < len(possible_moves):
                to_expand = [move for move in possible_moves
                             if move not in current_node.moves_expanded]
                move = choice(to_expand)
                state = self.game.get_next_state(current_node.state, move)
                possible_moves = state[0].get_moves(state[1])
                child = Node(state, move, len(possible_moves))
                current_node.add_child(child)
                self.state_node[state] = child
                return child
            else:
                current_node = self.get_best_child(current_node)
        return current_node

    def get_best_child(self, node):
        opponent_turn = (node.state[1] != self.colour)
        values = {}
        for child in node.children:
            wins, plays = child.get_wins_and_plays()
            if opponent_turn:
                wins = plays - wins
            parent_plays = node.get_wins_and_plays()[1]
            values[child] = self.get_ucb(wins, plays, parent_plays)
        best = max(values, key=values.get)
        return best

    def run_simulation(self, state):
        WIN = 1
        LOSS = 0
        state = deepcopy(state)
        while True:
            winner = self.game.get_winner(state[0])
            if winner:
                if winner == self.colour:
                    return WIN
                else:
                    return LOSS
            moves = state[0].get_moves(state[1])
            if not moves:
                state = (state[0], kit.Board.get_colour_of_other_player(state[1]))
                moves = state[0].get_moves(state[1])
            picked_move = choice(moves)
            # state = deepcopy(state[0]).make_move(picked_move, state[1])
            state = self.game.get_next_state(state, picked_move)

    @staticmethod
    def get_ucb(wins, plays, parent_plays):
        return (wins / plays) + sqrt(2 * log(parent_plays) / plays)


class Node:
    def __init__(self, state, move, children_amount):
        self.state = state
        self.plays = 0
        self.wins = 0
        self.children = []
        self.parent = None
        self.moves_expanded = set()
        self.moves_left_to_expand = children_amount
        self.move = move # the move that led to this state

    def propagate_completion(self):
        if self.parent is None:
            return
        if self.moves_left_to_expand > 0:
            self.moves_left_to_expand -= 1
        self.parent.propagate_completion()

    def add_child(self, node):
        self.children.append(node)
        self.moves_expanded.add(node.move)
        node.parent = self

    def has_children(self):
        return len(self.children) > 0

    def get_wins_and_plays(self):
        return self.wins, self.plays

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return 'move: {} wins: {} plays: {}'.format(self.move, self.wins,
                                                    self.plays)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.state == other.state
