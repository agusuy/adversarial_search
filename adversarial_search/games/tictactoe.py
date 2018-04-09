# -*- coding: utf-8 -*-
from ..core import Game
from ..utils import coord_id, board_lines, print_board, resultado, cached_property, cached_indexed_property

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
        return [self._Move(square) for square in range(9) if self.board[square] == '.']

    def results(self):
        lines = [ln for ln in board_lines(self.board, 3, 3) if len(ln) == 3]
        result_Xs = len([ln for ln in lines if ln == 'XXX']) - len([ln for ln in lines if ln == 'OOO'])
        if not result_Xs and [ln for ln in lines if '.' in ln]:
            # Sin l�neas y con casillas a�n vac�as.
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

# Quick test #######################################################################################

def run_test_game(agent1=None, agent2=None):
    if not agent1:
        from ..agents.minimax import MiniMaxAgent
        agent1 = MiniMaxAgent('Computer', 3, heuristic=TicTacToe.simple_heuristic)
    if not agent2:
        from ..agents.file import FileAgent
        agent2 = FileAgent(name='Human')
    from ..core import run_match
    run_match(TicTacToe(), agent1, agent2)
