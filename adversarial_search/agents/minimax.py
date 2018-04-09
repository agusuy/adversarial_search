# -*- coding: utf-8 -*-
from ..core import Agent

class MiniMaxAgent(Agent):
    """ An agent implementing simple heuristic MiniMax.
    """

    def __init__(self, name="MiniMaxAgent", horizon=3, random=None, heuristic=None):
        Agent.__init__(self, name)
        self.horizon = horizon
        # An instance of random.Random or equivalent is expected, else an 
        # integer seed or None to create a random.Random.
        self.random = self.randgen(random)
        self.__heuristic__ = heuristic

    def decision(self, game, *moves):
        nexts = [(move, self._minimax(game.next(move), 1)) for move in game.moves()]
        max_val = max([val for (_, val) in nexts])
        return self.random.choice([move for (move, val) in nexts if val == max_val])

    def terminal_value(self, game, depth):
        """ Returns a result if node is terminal or maximum depth has been reached; else returns 
            None.
        """
        results = game.results()
        if results:
            return results[self.player]
        if depth >= self.horizon:
            return self.heuristic(game, depth)
        return None

    def _minimax(self, game, depth):
        result = self.terminal_value(game, depth)
        if result is None:
            result = (max if game.active_player() == self.player else min)(
                [self._minimax(game.next(move), depth + 1) for move in game.moves()])
        return result

    def heuristic(self, game, depth):
        """ This method implements the heuristic for the minimax algorithm. If no implementation is
            provided it returns a random value in [-0.5,+0.5). This default behaviour usually should
            not be applied in a game.
        """
        return self.__heuristic__(self, game, depth) if self.__heuristic__ else self.random.random() - 0.5
