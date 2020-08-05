""" Test cases for module agents.
"""
import random
import unittest
from itertools import combinations

from .context import adversarial_search as a_s
from .test_games import Silly

RandomAgent = a_s.agents.random.RandomAgent
MiniMaxAgent = a_s.agents.minimax.MiniMaxAgent
AlphaBetaAgent = a_s.agents.alphabeta.AlphaBetaAgent
MCTSAgent = a_s.agents.mcts.MCTSAgent


class TestAgents(unittest.TestCase):
    """ Basic test cases for agents behaviour.
    """

    def assertBetterAgent(self, agent_worse, agent_best, game, match_count=10):
        players = game.players
        score_best_agent = 0
        score_worse_agent = 0
        for _ in range(match_count):
            result1, _ = a_s.core.run_match(game, agent_worse, agent_best)
            result2, _ = a_s.core.run_match(game, agent_best, agent_worse)
            score_best_agent += result1[players[1]] + result2[players[0]]
            score_worse_agent += result1[players[0]] + result2[players[1]]
        self.assertGreater(score_best_agent, score_worse_agent)

    def assertBetterThanRandom(self, agent, game, match_count=10, seed=None):
        random_agent = RandomAgent(random.Random(seed if seed else agent.name.__hash__()))
        self.assertBetterAgent(random_agent, agent, game, match_count)

    def testSilly(self):
        game = Silly()
        # Run matches only to see if agent components fail.
        agents = [
            RandomAgent(),
            MiniMaxAgent(),
            AlphaBetaAgent(),
            MCTSAgent(),
        ]
        for agents in combinations(agents, 2):
            a_s.core.run_match(game, *agents)

        # Statistically MiniMax based agents should beat random agents even without a proper heuristic.
        self.assertBetterThanRandom(MiniMaxAgent(), game)
        self.assertBetterThanRandom(AlphaBetaAgent(), game)
        self.assertBetterThanRandom(MCTSAgent(), game)


# TODO: Move to examples folder
'''
    def testTicTacToe(self):
        rand = random.Random(123456789)
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
'''

if __name__ == "__main__":
    unittest.main()
