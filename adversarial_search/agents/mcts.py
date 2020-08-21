from.agent import Agent


class MCTSAgent(Agent):
    """ An agent implementing flat MonteCarlo Tree Search.
    """

    def __init__(self, name="MCTSAgent", simulation_count=3, random=None, heuristic=None):
        Agent.__init__(self, name)
        self.simulationCount = simulation_count
        self.random = self.rand_gen(random)
        self.__heuristic__ = heuristic

    def _decision(self, moves, game):
        next_game_states = [[move, game.next(move), 0, 0] for move in moves]
        for s in range(self.simulationCount):
            for game_state in next_game_states:
                game_state[2] = game_state[2] + 1
                game_state[3] = game_state[3] + self.simulation(game_state[1])
        max_val = max(game_state[3] for game_state in next_game_states)
        return self.random.choice([move for [move, _, _, v] in next_game_states if v == max_val])

    def simulation(self, game):
        results = game.results()
        while not results:
            game = game.next(self.random.choice(game.moves()))
            results = game.results()
        return results[self.player]
