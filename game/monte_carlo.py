import datetime
from copy import copy
from random import choice
from math import log, sqrt

class MonteCarlo_ai:
    def __init__(self, game, **kwargs):
        self.game = game
        # self.states = []
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get('max_moves', 100)
        self.wins = {}
        self.plays = {}
        self.C = kwargs.get('C', sqrt(2)) # constant for calculating ucb

    # def update(self, state):
    #     self.states.append(state)

    def get_move(self):
        # state = self.states[-1]
        state = self.game.get_current_state()
        player = self.game.get_current_state_player(state)
        moves = state[0].get_moves(player.colour)
        if not moves:
            return
        if len(moves) == 1:
            return moves[1]

        # games = 0
        start = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - start < self.calculation_time:
            self.run_simulation()
            # games += 1

        moves_states = [(move, self.game.get_next_state(state, move))
                        for move in moves]
        percent_wins, move = max((self.wins.get((player, state), 0) /
                                  self.plays.get((player, state), 1),
                                 move)
                                 for move, state in moves_states)
        return move


    def run_simulation(self):
        visited_states = set()
        # states_copy = self.states[:]
        states_copy = []
        # state = states_copy[-1]
        state= self.game.get_current_state()
        player = self.game.get_current_state_player(state)
        winner = None
        expand = True
        for i in range(self.max_moves):
            possible_moves = state[0].get_moves(player.colour)
            move_states = [(move, self.game.get_next_state(state, move))
                           for move in possible_moves]
            if all(self.plays.get((player, state)) for player, state in move_states):
                log_total = log(
                sum(self.plays[(player, state)] for player, state in move_states))
                value, move, state = max(
                    (self.get_ucb(log_total, player, state), player, state)
                    for player, state in move_states)
            else:
                move, state = choice(move_states)
            states_copy.append(state)
            if expand and (player, state) not in self.plays:
                expand = False
                self.add_new_state_records(player, state)
            visited_states.add((player, state))
            player = self.game.get_current_state_player(state)
            winner = self.game.get_winner(state[0])
            if winner:
                break
        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[((player, state))] += 1
            if player.colour == winner:
                self.wins[(player, state)] += 1

    def get_ucb(self, log_total, player, state):
        return (self.wins[(player, state)] / self.plays[(player, state)]
                + self.C * sqrt(log_total / self.plays[(player, state)]))

    def add_new_state_records(self, player, state):
        self.plays[(player, state)] = 0
        self.wins[(player, state)] = 0