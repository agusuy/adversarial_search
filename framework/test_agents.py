# coding=latin-1
""" Test cases for module _agents.
"""
import random
import unittest
from itertools import combinations

import _base as base
import _contests as contests
from _agents import RandomAgent, MiniMaxAgent, AlphaBetaAgent
from test_games import Silly
from tictactoe import TicTacToe


class TestAgents(unittest.TestCase):
    """ Basic testcases for agents behaviour.
    """

    def assertBetterAgent(self, agentWorse, agentBest, game, match_count=5):
        stats = contests.complete(contests.AllAgainstAll_Contest(game, [agentWorse, agentBest], match_count))
        self.assertGreater(stats.result_sum[agentBest], stats.result_sum[agentWorse])

    def assertBetterThanRandom(self, agent, game, match_count=10, seed=None):
        randomAgent = RandomAgent(random.Random(seed if seed else agent.name.__hash__()))
        self.assertBetterAgent(randomAgent, agent, game, match_count)

    def testSilly(self):
        game = Silly()
        # Run matches only to see if agent components fail.
        for agents in combinations([RandomAgent(), MiniMaxAgent(), AlphaBetaAgent()], 2):
            base.run_match(game, *agents)
        # Statistically MiniMax based agents should beat random agents even without a proper heuristic.
        self.assertBetterThanRandom(MiniMaxAgent(), game)
        self.assertBetterThanRandom(AlphaBetaAgent(), game)

    def testTicTacToe(self):
        rand = random.Random(123456789L)
        game = TicTacToe()
        minimax_agents = [MiniMaxAgent, AlphaBetaAgent]

        # Statistically MiniMax based agents should beat random agents even without a proper heuristic.
        for agent in minimax_agents:
            self.assertBetterThanRandom(agent(random=rand), game)

        # Statistically MiniMax based should improve with greater horizons.
        for agent in minimax_agents:
            self.assertBetterAgent(agent('Horizon1', horizon=1, random=rand),
                                   agent('Horizon5', horizon=5, random=rand), game, 20)

        # Statistically in MiniMax based agents having a simple heuristic should be better than none.
        for agent in minimax_agents:
            self.assertBetterAgent(agent('RandomHeuristic', random=rand),
                                   agent('SimpleHeuristic', heuristic=TicTacToe.simple_heuristic, random=rand), game)


if __name__ == "__main__":
    unittest.main()
