# -*- coding: utf-8 -*-
from ..core import Agent


class MCTSAgent(Agent):
    """ An agent implementing flat MonteCarlo Tree Search.
    """

    def __init__(self, name="MCTSAgent", simulation_count=3, random=None, heuristic=None):
        Agent.__init__(self, name)
        self.simulationCount = simulation_count
        self.random = self.randgen(random)
        self.__heuristic__ = heuristic

    def decision(self, game, *moves):
        nexts = [[move, game.next(move), 0, 0] for move in game.moves()]
        for s in range(self.simulationCount):
            for next in nexts:
                next[2] = next[2] + 1
                next[3] = next[3] + self.simulation(next[1])
        max_val = max(next[3] for next in nexts)
        return self.random.choice([move for [move, _, _, v] in nexts if v == max_val])

    def simulation(self, game):
        results = game.results()
        while not results:
            game = game.next(self.random.choice(game.moves()))
            results = game.results()
        return results[self.player]
