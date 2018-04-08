# coding=latin-1
""" Implementación del TaTeTí.
"""

from _base import Game
from _utils import coord_id, board_lines, print_board, resultado, cached_property, cached_indexed_property
from test_games import GameTest


class TicTacToe(Game):
    """ Game component for TicTacToe.
    """
    PLAYERS = ('Xs', 'Os')

    def __init__(self, board=None, enabled=0):
        Game.__init__(self, *TicTacToe.PLAYERS)
        self.board = board if board else '.' * 9
        self.enabled = enabled

    class _Move(int):
        def __str__(self):
            return coord_id(*divmod(self, 3))

    def active_player(self):
        return self.players[self.enabled]

    @cached_property('__moves__')
    def moves(self):
        if self.results():  # In order to avoid returning both moves and results.
            return None
        return [self._Move(square) for square in xrange(9) if self.board[square] == '.']

    def results(self):
        lines = [ln for ln in board_lines(self.board, 3, 3) if len(ln) == 3]
        result_Xs = len([ln for ln in lines if ln == 'XXX']) - len([ln for ln in lines if ln == 'OOO'])
        if not result_Xs and [ln for ln in lines if '.' in ln]:
            # Sin líneas y con casillas aún vacías.
            result_Xs = None
        return resultado('Xs', self.players, result_Xs)

    @cached_indexed_property('__next__')
    def next(self, move):
        board_list = list(self.board)
        enabled_player = self.players[self.enabled]
        board_list[move] = enabled_player[0]
        return TicTacToe(''.join(board_list), (self.enabled + 1) % 2)

    def __str__(self):
        return print_board(self.board.replace('.', ' '), 3, 3, '-', '|', '+')

    def __repr__(self):
        return '%s[%s]' % (self.players[self.enabled][0], self.board)

    @staticmethod
    def simple_heuristic(agent, game, depth):
        square_value = {'X': 1, 'O': -1, '.': 0}
        square_factors = [0.1, -0.1, 0.1, -0.1, 0.2, -0.1, 0.1, -0.1, 0.1]
        board_value = sum([square_value[s] * p for s, p in zip(game.board, square_factors)])
        return board_value if agent.player == 'Xs' else -board_value


class Test_TicTacToe(GameTest):
    """ TicTacToe testcases.
    """

    def test_basic(self):
        self.basic_test(TicTacToe, zero_sum=True, enabled_players=1)

    def test_traces(self):
        self.trace_test_text(TicTacToe(), """\
            X[.........] Xs b2
            O[....X....] Os a1
            X[O...X....] Xs a2
            O[OX..X....] Os a3
            X[OXO.X....] Xs c2
            """, Xs=1, Os=-1)
        self.trace_test_text(TicTacToe(), """\
            X[.........] Xs a2
            O[.X.......] Os b2
            X[.X..O....] Xs c2
            O[.X..O..X.] Os a1
            X[OX..O..X.] Xs a3
            O[OXX.O..X.] Os c3
            """, Xs=-1, Os=1)


################################################################################

if __name__ == '__main__':
    from _agents import MiniMaxAgent, FileAgent, RandomAgent
    from _base import run_match

    run_match(TicTacToe(), MiniMaxAgent('Computer', 3, heuristic=TicTacToe.simple_heuristic), FileAgent(name='Human'))
    # print run_match(TicTacToe(), RandomAgent(), MiniMaxAgent())
