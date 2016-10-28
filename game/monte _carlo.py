import datetime
from random import choice

class MonteCarlo:
    def __init__(self, game, **kwargs):
        self.game = game
        self.states = []
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get('max_moves', 100)
        self.wins = {}
        self.plays = {}

    def update(self, state):
        self.states.append(state)

    def get_move(self):
        state = self.states[-1]
        player = self.game.get_current_player(state)
        moves = state[0][:].get_moves(player.colour)
        if not moves:
            return
        if len(moves) == 1:
            return moves[1]
        start = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - start < self.calculation_time:
            self.run_simulation()

    def run_simulation(self):
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.game.get_current_player(state)
        winner = None
        expand = True
        for i in range(self.max_moves):
            possible_moves = self.game.mover.board.get_moves(player.colour)
            move = choice(possible_moves)
            state = self.game.get_next_state(state, move)
            states_copy.append(state)
            if expand and (player, state) not in self.plays:
                expand = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0
            visited_states.add((player, state))
            player = self.game.get_current_player(state)
            winner = self.game.get_winner(state[0])
            if winner:
                break
        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[((player, state))] += 1
            if player.colour == winner:
                self.wins[(player, state)] += 1
