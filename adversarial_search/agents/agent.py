import random

from abc import ABC, abstractmethod


class Agent(ABC):
    """ Base class for agents participating in games.
    """

    def __init__(self, name):
        self.name = name
        self.player = None

    def select_move(self, game, *moves):
        """ Agents move choice. If no moves are provided, choices are retrieved from the game.
        """
        if not moves:
            moves = game.moves()
            if not moves:
                return None
        return self._decision(moves, game)

    @abstractmethod
    def _decision(self, moves, game):
        """ Method called by Agent.select_move() to actually make the choice of move. This should be
            overridden by subclasses.
        """
        pass

    def match_begins(self, player, game):
        """ Tells the agent that a match he is participating in is starting. This should not be
            called again until the match ends.
        """
        self.player = player

    def match_moves(self, before, move, after):
        """ Tells the agent the active player have moved in the match he is participating in.
        """
        pass

    def match_ends(self, game):
        """ Tells the agent the match he was participating in has finished. The game parameter holds
            the final game state.
        """
        pass

    def __str__(self):
        return '%s(%s)' % (self.name, self.player)

    def __hash__(self):
        return self.name.__hash__()

    @staticmethod
    def rand_gen(x):
        """ If x is `None` or `int` or `long`, returns random.Random(x), else returns x.
        """
        return random.Random(x) if x is None or type(x) == int else x
