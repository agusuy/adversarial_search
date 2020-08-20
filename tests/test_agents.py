""" Test cases for module agents.
"""
import random
from itertools import combinations

import pytest

from .context import adversarial_search as a_s
from .test_games import Silly

RandomAgent = a_s.agents.random.RandomAgent
MiniMaxAgent = a_s.agents.minimax.MiniMaxAgent
AlphaBetaAgent = a_s.agents.alphabeta.AlphaBetaAgent
MCTSAgent = a_s.agents.mcts.MCTSAgent

AGENTS = [
    RandomAgent,
    MiniMaxAgent,
    AlphaBetaAgent,
    MCTSAgent,
]


class TestBaseAgent:
    def setup(self):
        self.agent = a_s.agents.agent.Agent("test agent")

    def test_name(self):
        assert self.agent.name == "test agent"

    def test_decision(self):
        assert self.agent.decision(a_s.core.Game(), *['1', '2', '3']) == '1'

    def test__decision(self):
        assert self.agent._decision(['1', '2', '3']) == '1'

    def test_str(self):
        assert str(self.agent) == "test agent(None)"


class TestAgents:
    """ Basic test cases for agents behaviour.
    """

    @staticmethod
    def assert_better_agent(agent_worse, agent_best, game, match_count=10):
        players = game.players
        score_best_agent = 0
        score_worse_agent = 0
        for _ in range(match_count):
            result1, _ = a_s.core.run_match(game, agent_worse, agent_best)
            result2, _ = a_s.core.run_match(game, agent_best, agent_worse)
            score_best_agent += result1[players[1]] + result2[players[0]]
            score_worse_agent += result1[players[0]] + result2[players[1]]
        assert score_best_agent > score_worse_agent

    def assert_better_than_random(self, agent, game, match_count=10, seed=None):
        random_agent = RandomAgent(random.Random(seed if seed else agent.name.__hash__()))
        self.assert_better_agent(random_agent, agent, game, match_count)

    @pytest.mark.parametrize('agent1, agent2', list(combinations(AGENTS, 2)))
    def test_sanity_agents(self, agent1, agent2):
        # Run matches only to see if agent components fail.
        a_s.core.run_match(Silly(), agent1(), agent2())

    @pytest.mark.parametrize('agent', [
        MiniMaxAgent,
        AlphaBetaAgent,
        MCTSAgent,
    ])
    def test_agent_against_random(self, agent):
        # Statistically MiniMax based agents should beat random agents even without a proper heuristic.
        self.assert_better_than_random(agent(), Silly())


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
