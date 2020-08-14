# -*- coding: utf-8 -*-
import sys
from ..core import Agent


class FileAgent(Agent):
    """ An agent that takes his moves from a file and keeps record of the match in another one. It
        is also used like a user interface using standard input and output.
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
        """ Writes all available moves and reads the decision from `in_file`. Each move must be in a
            separate line. All lines starting with a '#' are ignored.
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
