# coding=latin-1

import sys

from _utils import randgen


class Agent(object):
    """ Base class for agents participating in games.
    """

    def __init__(self, name):
        self.name = name
        self.player = None

    def decision(self, game, *moves):
        """ Agents move choice. If no moves are provided, choices are retrieved
            from the game.
        """
        if not moves:
            moves = game.moves()
            if not moves:
                return None
        return self._decision(moves)

    def _decision(self, moves):
        """ Method called by Agent.decision() to actually make the choice of
            move. This should be overriden by subclasses.
        """
        return moves[0]  # Please do not use this default implementation.

    def match_begins(self, player, game):
        """ Tells the agent that a match he is participating in is starting.
            This should not be called again until the match ends.
        """
        self.player = player

    def match_moves(self, before, move, after):
        """ Tells the agent the active player have moved in the match he is
            participating in.
        """
        pass

    def match_ends(self, game):
        """ Tells the agent the match he was participating in has finished. The
            game parameter holds the final game state.
        """
        pass

    def __str__(self):
        return '%s(%s)' % (self.name, self.player)

    def __hash__(self):
        return self.name.__hash__()


class FileAgent(Agent):
    """ An agent that takes his moves from a file and keeps record of the match
        in another one. It is also used like a user interface using standard 
        input and output.
    """

    def __init__(self, in_file=None, out_file=None, name='FileAgent'):
        Agent.__init__(self, name)
        if in_file is None:
            in_file = sys.stdin
        self.in_file = in_file
        if out_file is None:
            out_file = sys.stdout
        self.out_file = out_file

    def __print_state__(self, game):
        self.out_file.write('#\t%s\n' % str(game).replace('\n', '\n#\t'))

    def match_begins(self, player, game):
        Agent.match_begins(self, player, game)
        self.out_file.write('# %s starts a match.\n' % (self,))
        self.__print_state__(game)
        self.out_file.flush()

    def match_moves(self, before, move, after):
        self.out_file.write('# %s moves %s.\n' % (before.active_player(), move))
        self.__print_state__(after)
        self.out_file.flush()

    def match_ends(self, game):
        result = game.results()[self.player]
        outcome = 'defeat' if result < 0 else 'victory' if result > 0 else 'draw'
        self.out_file.write('# %s ends the match with %s (%.4f).\n' % (self, outcome, result))
        self.out_file.flush()

    def _decision(self, moves):
        """ Writes all available moves and reads the decision from in_file. Each
            move must be in a separate line. All lines starting with a '#' are 
            ignored.
        """
        self.out_file.write('# Available moves for %s: ' % self)
        self.out_file.write(' '.join([str(move) for move in moves]))
        self.out_file.write('\n')
        line = self.in_file.readline().strip()
        while line:
            if not line.startswith('#'):
                for move in [move for move in moves if str(move) == line]:
                    return move
            line = self.in_file.readline().strip()
        return None


class RandomAgent(Agent):
    """ An agent that moves randomly.
    """

    def __init__(self, random=None, name='RandomAgent'):
        Agent.__init__(self, name)
        # An instance of random.Random or equivalent is expected, else an 
        # integer seed or None to create a random.Random.
        self.random = randgen(random)

    def _decision(self, moves):
        return self.random.choice(moves)


class TraceAgent(Agent):
    """ An agent that reenacts (and records) a move trace.
    """

    def __init__(self, trace=[], proxy=None, name='TraceAgent'):
        Agent.__init__(self, name)
        self.trace = trace
        self.proxy = proxy

    def match_begins(self, player, game):
        Agent.match_begins(self, player, game)
        self._current_move = 0

    def _decision(self, moves):
        """ Returns the next move in the current trace. Else it uses the proxy
            agent to get a new move, recording it in the agents trace.
        """
        self._current_move += 1
        if self._current_move - 1 < len(self.trace):
            return self.trace[self._current_move - 1]
        else:
            move = self.proxy._decision(moves)
            self.trace.append(move)
            return move


class MiniMaxAgent(Agent):
    """ An agent implementing simple heuristic MiniMax.
    """

    def __init__(self, name="MiniMaxAgent", horizon=3, random=None, heuristic=None):
        Agent.__init__(self, name)
        self.horizon = horizon
        # An instance of random.Random or equivalent is expected, else an 
        # integer seed or None to create a random.Random.
        self.random = randgen(random)
        self.__heuristic__ = heuristic

    def decision(self, game, *moves):
        nexts = [(move, self._minimax(game.next(move), 1)) for move in game.moves()]
        max_val = max([val for (_, val) in nexts])
        return self.random.choice([move for (move, val) in nexts if val == max_val])

    def terminal_value(self, game, depth):
        """ Returns a result if node is terminal or maximum depth has been 
            reached. Else returns None.
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
        """ This method implements the heuristic for the minimax algorithm. If 
            no implementation is provided it returns a random value. This default
            behaviour usually should not be applied in a game.
        """
        return self.__heuristic__(self, game, depth) if self.__heuristic__ else self.random.random() * 2 - 1


INFINITE = 0x7FFFFFFF


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
        if active_player == self.player:
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
