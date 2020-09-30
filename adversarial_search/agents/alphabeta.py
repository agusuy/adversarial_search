from math import inf

from .minimax import MiniMaxAgent

INFINITE = inf


class AlphaBetaAgent(MiniMaxAgent):
    """ An agent implementing MiniMax with alpha-beta pruning.
        <http://en.wikipedia.org/wiki/Alpha-beta_pruning>
    """

    def __init__(self, name="AlphaBetaAgent", horizon=3, random=None, heuristic=None):
        MiniMaxAgent.__init__(self, name, horizon, random, heuristic)

    def _minimax(self, game, depth, alpha=-INFINITE, beta=INFINITE):
        result = self.terminal_value(game, depth)
        if result is not None:
            return result
        moves = game.moves()
        active_player = game.active_player()
        if active_player == self.player_type:
            for move in moves:
                value = self._minimax(game.next(move), depth + 1, alpha, beta)
                if alpha < value:
                    alpha = value
                if beta <= alpha:
                    break
            return alpha
        else:
            for move in moves:
                value = self._minimax(game.next(move), depth + 1, alpha, beta)
                if beta > value:
                    beta = value
                if beta <= alpha:
                    break
            return beta
