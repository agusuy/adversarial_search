# -*- coding: utf-8 -*-
from adversarial_search import Game
from adversarial_search.utils import coord_id, board_lines, print_board, game_result, cached_property, \
    cached_indexed_property


class Cuanteti(Game):
    """ Game component for Cuanteti.
    """
    PLAYERS = ('Xs', 'Os')

    def __init__(self, board=None, enabled=0):
        Game.__init__(self, *Cuanteti.PLAYERS)
        self.board = board if board else '.' * 16
        self.enabled = enabled

    class _Move(int):
        def __str__(self):
            return coord_id(*divmod(self, 4))

    def active_player(self):
        return self.players[self.enabled]

    @cached_property('__moves__')
    def moves(self):
        return [self._Move(square) for square in range(16) if self.board[square] == '.']

    def results(self):
        if not self.moves():
            result_xs = sum(len(ln) - 2 if ln == 'X' * len(ln) else 1
                            for ln in board_lines(self.board, 4, 4)
                            if len(ln) > 2 and (ln == 'X' * len(ln) or 'XXX' in ln))
            result_os = sum(len(ln) - 2 if ln == 'O' * len(ln) else 1
                            for ln in board_lines(self.board, 4, 4)
                            if len(ln) > 2 and (ln == 'O' * len(ln) or 'OOO' in ln))
            # print (list(board_lines(self.board, 4, 4)))
            # print (result_xs, result_os)
            return game_result('Xs', self.players, result_xs - result_os)
        else:
            return None

    @cached_indexed_property('__next__')
    def next(self, move):
        board_list = list(self.board)
        enabled_player = self.players[self.enabled]
        board_list[move] = enabled_player[0]
        return Cuanteti(''.join(board_list), (self.enabled + 1) % 2)

    def __str__(self):
        return print_board(self.board.replace('.', ' '), 4, 4, '-', '|', '+')

    def __repr__(self):
        return '%s[%s]' % (self.players[self.enabled][0], self.board)


# Quick test #######################################################################################

def run_test_game(agent1=None, agent2=None):
    if not agent1:
        from adversarial_search.agents.mcts import MCTSAgent
        agent1 = MCTSAgent('Computer', simulation_count=10)
    if not agent2:
        from adversarial_search.agents.files import FileAgent
        agent2 = FileAgent(name='Human')
    from adversarial_search.core import run_match
    run_match(Cuanteti(), agent1, agent2)


if __name__ == '__main__':
    run_test_game()
