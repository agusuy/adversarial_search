# coding=latin-1
""" Implementacion del juego Toads and Frogs
"""

from _base import Game
from _utils import resultado, print_board, coord_id
from test_games import GameTest


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
            moves = [self._Move(pos) for pos in xrange(len(self.board)) if
                     self.board[pos:].startswith('T_') or self.board[pos:].startswith('TF_')]
        else:  # Frogs move
            moves = [self._Move(pos) for pos in xrange(len(self.board)) if
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


class Test_Toads_Frogs(GameTest):
    """ Toads and Frogs testcases
    """

    def test_basic(self):
        self.basic_test(Toads_Frogs, zero_sum=True, enabled_players=1)

    def test_trace(self):
        self.trace_test_text(Toads_Frogs(None, 0, 3, 2), """\
            T[TTT__FFF] Toads a3
            F[TT_T_FFF] Frogs a6
            T[TT_TF_FF] Toads a2
            F[T_TTF_FF] Frogs a7
            T[T_TTFF_F] Toads a1
            F[_TTTFF_F] Frogs a8
            """, Toads=-1, Frogs=1)

        self.trace_test_text(Toads_Frogs(None, 0, 2, 1), """\
            T[TT_FF] Toads a2
            F[T_TFF] Frogs a4
            T[TFT_F] Toads a3
            F[TF_TF] Frogs a5
            T[TFFT_] Toads a4
            """, Toads=1, Frogs=-1)


if __name__ == '__main__':
    from _agents import RandomAgent, FileAgent
    from _base import run_match, match

    # for move_number, moves, game_state in match(Toads_Frogs(None, 0, 5, 4), RandomAgent(name='Agent1'), RandomAgent(name='Agent2')):
    #     if move_number is not None:
    #         print '%d: %s -> %r' % (move_number, moves, game_state)
    #     else:
    #         print 'Result: %s' % (moves)
    #         print 'Final board: %r'  % (game_state)
    run_match(Toads_Frogs(None, 0, 5, 4), RandomAgent(), FileAgent(name='Human'))
