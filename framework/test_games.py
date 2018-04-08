# coding=latin-1
""" Casos de prueba para el m�dulo juegos.
"""
import random
import unittest

import _base as base
import _utils as utils


class GameTest(unittest.TestCase):
    """ Base class for game testcases.
    """

    def basic_test(self, Game, **checks):
        """ Simulates many games randomnly checking basic behaviour of the game 
            component.
            Checks flags activate some asserts. Options are:
            - zero_sum: checks if results sum zero.
        """
        # TODO - player_turns: maximum number of consecutive turns a player may have.
        # TODO - alternated: checks players alternate in turns.  
        zero_sum = checks.get('zero_sum', False)
        rnd = random.Random(123456)

        for _ in range(100):
            game = Game()
            for _ in range(100):
                moves = game.moves()
                results = game.results()
                if results is None:
                    # If no results, then there must be moves.
                    self.assertTrue(moves, "No results and no moves: %s" % game)
                    # None is not a valid move.
                    self.assertFalse([m for m in moves if m is None], "None move: %r %r" % (game, moves))
                    game = game.next(rnd.choice(moves))
                else:
                    self.assertFalse(moves, "Results and moves: %r %r %r" % (game, results, moves))
                    # Zero sum results check.
                    zero_sum and self.assertEqual(sum(results.values()), 0, "Nonzero sum: %r %r" % (game, results))
                    break

    def trace_test(self, game, *trace, **results):
        """ Simulates a match with a trace of moves, verifying game's behaviour
            at each step. If results are given, it checks if the game finishes
            and if the results are the same. 
            The trace must be a list of two or three items sequences. Two items
            represent player and move, while three items represent state, player
            and move. If the state is included, its checked to be equal to the 
            game objetc's representation. 
        """
        for ply in trace:
            if len(ply) > 2:
                game_repr, player, move = ply
                self.assertEqual('%r' % game, game_repr)
            else:
                player, move = ply
            moves = game.moves()
            self.assertTrue(moves,
                            'Player %s has no moves: %r %r' % (player, game, moves))
            self.assertIsNotNone(moves)
            self.assertTrue(str(move) in map(str, moves),
                            'Move %s is not valid: %r %r' % (move, game, moves))
            if not move in moves:  # Seek actual move.
                move = [m for m in moves if str(m) == move][0]
            self.assertIsNone(game.results())
            game1 = game.next(move)
            self.assertNotEqual(game, game1)
            game = game1
        if not results:
            self.assertIsNone(game.results())
        else:
            self.assertDictEqual(results, game.results())

    def trace_test_text(self, game, trace, **results):
        """ Allows to write a full trace in text, to use with GameTest.trace_test.
            Each ply in the trace is a line, each component of the ply is
            separated by spaces.
        """
        trace = trace.strip()
        return self.trace_test(game, *[tuple(ln.split()) for ln in trace.splitlines()], **results)


class Silly(base.Game):
    """ Certainly a silly game, for testing purposes only.
        Players A and B play, with A starting the game. Each turn, the active
        player gets to decide if he wins (+), he loses (-), its a tie (=), or he 
        continues playing or he enables the other player.
    """
    RESULTS = {'+': 1, '=': 0, '-': -1, 'A': None, 'B': None}
    PLAYERS = tuple([j for j, r in RESULTS.items() if r is None])

    def __init__(self, state='A', result=None):
        base.Game.__init__(self, *Silly.PLAYERS)
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
        return utils.resultado(self.state, self.players, self._result)

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


class TestGame_Silly(GameTest):
    """ Testing reference game Silly.
    """

    def test_basic(self):
        self.basic_test(Silly, zero_sum=True, enabled_players=1)

    def test_traces(self):
        self.trace_test(Silly(), 'AA+', A=1, B=-1)
        self.trace_test(Silly(), 'AA=', A=0, B=0)
        self.trace_test(Silly(), 'AA-', A=-1, B=1)
        self.trace_test(Silly(), 'AAA')
        self.trace_test(Silly(), 'AAB')

        self.trace_test(Silly(), 'AAA', 'AA+', A=1, B=-1)
        self.trace_test(Silly(), 'AAA', 'AA=', A=0, B=0)
        self.trace_test(Silly(), 'AAA', 'AA-', A=-1, B=1)
        self.trace_test(Silly(), 'AAA', 'AAA')
        self.trace_test(Silly(), 'AAA', 'AAB')

        self.trace_test(Silly(), 'AAB', 'BB+', A=-1, B=1)
        self.trace_test(Silly(), 'AAB', 'BB=', A=0, B=0)
        self.trace_test(Silly(), 'AAB', 'BB-', A=1, B=-1)
        self.trace_test(Silly(), 'AAB', 'BBA')
        self.trace_test(Silly(), 'AAB', 'BBB')

        self.trace_test_text(Silly(), 'A B\nB A\n' * 5)
        self.trace_test_text(Silly(), 'A A\n' * 10)
        self.trace_test_text(Silly(), 'A B\n' + 'B B\n' * 5)


if __name__ == "__main__":
    unittest.main()
