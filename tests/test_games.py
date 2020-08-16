import random

import pytest

from .context import adversarial_search as a_s

Game = a_s.core.Game
utils = a_s.utils


class GameTest:
    """ Base class for game test cases.
    """

    @staticmethod
    def basic_test(game_class, **checks):
        """ Simulates many games randomly checking basic behaviour of the game component. Checks
            flags activate some asserts. Options are:

            + zero_sum: checks if results sum zero.
        """
        # TODO - player_turns: maximum number of consecutive turns a player may have.
        # TODO - alternated: checks players alternate in turns.  
        zero_sum = checks.get('zero_sum', False)
        rnd = random.Random(123456)

        for _ in range(100):
            game = game_class()
            for _ in range(100):
                moves = game.moves()
                results = game.results()
                if results is None:
                    # If no results, then there must be moves.
                    assert moves, "No results and no moves: %s" % game
                    # None is not a valid move.
                    assert not [m for m in moves if m is None], "None move: %r %r" % (game, moves)
                    game = game.next(rnd.choice(moves))
                else:
                    assert not moves, "Results and moves: %r %r %r" % (game, results, moves)
                    # Zero sum results check.
                    assert zero_sum
                    assert sum(results.values()) == 0, "Nonzero sum: %r %r" % (game, results)

                    break

    @staticmethod
    def trace_test(game, *trace, **results):
        """ Simulates a match with a trace of moves, verifying game's behaviour at each step. If
            results are given, it checks if the game finishes and if the results are the same. The
            trace must be a list of two or three items sequences. Two items represent player and
            move, while three items represent state, player and move. If the state is included, its
            checked to be equal to the game object representation.
        """
        for ply in trace:
            if len(ply) > 2:
                game_repr, player, move = ply
                assert '%r' % game == game_repr
            else:
                player, move = ply
            moves = game.moves()
            assert moves, 'Player %s has no moves: %r %r' % (player, game, moves)
            assert moves is not None
            assert str(move) in map(str, moves), 'Move %s is not valid: %r %r' % (move, game, moves)
            if move not in moves:  # Seek actual move.
                move = [m for m in moves if str(m) == move][0]
            assert game.results() is None
            next_game = game.next(move)
            assert game != next_game
            game = next_game
        if not results:
            assert game.results() is None
        else:
            assert results == game.results()

    def trace_test_text(self, game, trace, **results):
        """ Allows to write a full trace in text, to use with `GameTest.trace_test`. Each ply in the
            trace is a line, each component of the ply is separated by spaces.
        """
        trace = trace.strip()
        return self.trace_test(game, *[tuple(ln.split()) for ln in trace.splitlines()], **results)


class Silly(Game):
    """ Certainly a silly game, for testing purposes only. Players A and B play, with A starting the
        game. Each turn, the active player gets to decide if he wins (+), he loses (-), its a tie
        (=), or he continues playing or he enables the other player.
    """
    RESULTS = {'+': 1, '=': 0, '-': -1, 'A': None, 'B': None}
    PLAYERS = tuple([j for j, r in RESULTS.items() if r is None])

    def __init__(self, state='A', result=None):
        Game.__init__(self, *Silly.PLAYERS)
        self.state = state
        self._result = result

    def active_player(self):
        return self.state

    def moves(self):
        if self._result is None:
            return list(Silly.RESULTS.keys())
        else:
            return []

    def results(self):
        return utils.game_result(self.state, self.players, self._result)

    def next(self, move):
        result = Silly.RESULTS[move]
        if result is None:
            return Silly(move)
        else:
            return Silly(self.state, result)

    def __str__(self):
        return 'Silly[%s]' % self.state

    def __repr__(self):
        return self.state


class TestGameSilly(GameTest):
    """ Testing reference game Silly.
    """

    def test_basic(self):
        self.basic_test(Silly, zero_sum=True, enabled_players=1)

    @pytest.mark.parametrize("game, trace, results",
                             [(Silly(), ('AA+',), {'A': 1, 'B': -1}),
                              (Silly(), ('AA=',), {'A': 0, 'B': 0}),
                              (Silly(), ('AA-',), {'A': -1, 'B': 1}),
                              (Silly(), ('AAA',), {}),
                              (Silly(), ('AAB',), {}),
                              (Silly(), ('AAA', 'AA+'), {'A': 1, 'B': -1}),
                              (Silly(), ('AAA', 'AA='), {'A': 0, 'B': 0}),
                              (Silly(), ('AAA', 'AA-'), {'A': -1, 'B': 1}),
                              (Silly(), ('AAA', 'AAA'), {}),
                              (Silly(), ('AAA', 'AAB'), {}),
                              (Silly(), ('AAB', 'BB+'), {'A': -1, 'B': 1}),
                              (Silly(), ('AAB', 'BB='), {'A': 0, 'B': 0}),
                              (Silly(), ('AAB', 'BB-'), {'A': 1, 'B': -1}),
                              (Silly(), ('AAB', 'BBA'), {}),
                              (Silly(), ('AAB', 'BBB'), {}),
                              ])
    def test_traces(self, game, trace, results):
        self.trace_test(Silly(), *trace, **results)

    @pytest.mark.parametrize("game, trace, results",
                             [(Silly(), 'A B\nB A\n' * 5, {}),
                              (Silly(), 'A A\n' * 10, {}),
                              (Silly(), 'A B\n' + 'B B\n' * 5, {}),
                              ])
    def test_text(self, game, trace, results):
        self.trace_test_text(game, trace, **results)


# TODO: Move to examples folder
'''
TicTacToe = a_s.games.tictactoe.TicTacToe


class TestTicTacToe(GameTest):
    """ TicTacToe test cases.
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


Toads_Frogs = a_s.games.toads_and_frogs.ToadsFrogs


class TestToadsFrogs(GameTest):
    """ Toads and Frogs test cases
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


Cuanteti = a_s.games.cuanteti.cuanteti


class TestCuanteti(GameTest):
    """ Cuanteti test cases.
    """

    def test_basic(self):
        self.basic_test(Cuanteti, zero_sum=True, enabled_players=1)
'''
