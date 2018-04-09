# -*- coding: utf-8 -*-
from ..core import Game
from ..utils import coord_id, print_board, resultado

class Toads_Frogs(Game):
    """ Game component for Toads and Frogs
    """

    PLAYERS = ('Toads', 'Frogs')

    def __init__(self, board=None, enabled=0, chips_per_player=3, empty_spaces=2):
        Game.__init__(self, *Toads_Frogs.PLAYERS)
        if board:
            self.board = board
        else:
            self.board = 'T' * chips_per_player + '_' * empty_spaces + 'F' * chips_per_player
        self.enabled = enabled

    def active_player(self):
        return self.players[self.enabled]

    class _Move(int):
        def __str__(self):
            return coord_id(0, self)

    def moves(self):
        if not self.enabled:  # Toads move
            moves = [self._Move(pos) for pos in range(len(self.board)) if
                     self.board[pos:].startswith('T_') or self.board[pos:].startswith('TF_')]
        else:  # Frogs move
            moves = [self._Move(pos) for pos in range(len(self.board)) if
                     self.board[:pos + 1].endswith('_F') or self.board[:pos + 1].endswith('_TF')]
        return moves

    def results(self):
        # There is no draw in this game
        enabled_player = self.players[self.enabled]
        if not self.enabled:
            moves = 'T_' in self.board or 'TF_' in self.board
        else:
            moves = '_F' in self.board or '_TF' in self.board
        if not moves:
            return resultado(enabled_player, self.players, -1)
        return None

    def next(self, move):
        board_list = list(self.board)
        enabled_player = self.players[self.enabled]
        board_list[move] = '_'
        if not self.enabled:  # A toad moves
            position = move + 1 if board_list[move + 1] == '_' else move + 2
        else:  # A frog moves
            position = move - 1 if board_list[move - 1] == '_' else move - 2
        board_list[position] = enabled_player[0]
        return Toads_Frogs(''.join(board_list), (self.enabled + 1) % 2)

    def __str__(self):
        return print_board(self.board, 1, len(self.board) + 1)

    def __repr__(self):
        return '%s[%s]' % (self.players[self.enabled][0], self.board)

# Quick test #######################################################################################

def run_test_game(agent1=None, agent2=None):
    if not agent1:
        from ..agents.random import RandomAgent
        agent1 = RandomAgent(name='Computer')
    if not agent2:
        from ..agents.file import FileAgent
        agent2 = FileAgent(name='Human')
    from ..core import run_match
    run_match(Toads_Frogs(None, 0, 5, 4), agent1, agent2)
