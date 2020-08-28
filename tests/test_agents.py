""" Test cases for module agents.
"""
import random
from itertools import combinations
from unittest.mock import patch, call

import pytest

from .context import adversarial_search as a_s
from .test_games import Silly

Agent = a_s.agents.agent.Agent
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


@pytest.fixture
def game():
    return a_s.core.Game()


class TestBaseAgent:
    @patch.object(Agent, '__abstractmethods__', set())
    def setup(self):
        self.agent = a_s.agents.agent.Agent("test agent")

    def test_init(self):
        with pytest.raises(TypeError) as e:
            Agent("test agent")
        assert "Can't instantiate abstract class %s" % Agent.__name__ in str(e.value)

    def test_name(self):
        assert self.agent.name == "test agent"

    @patch.object(Agent, '_decision', return_value='1')
    @patch.object(a_s.core.Game, 'moves')
    def test_select_move(self, mock_moves, mock_decision, game):
        assert self.agent.select_move(game, *['1', '2', '3']) == '1'
        mock_moves.assert_not_called()
        mock_decision.assert_called_once_with(('1', '2', '3'), game)

    @patch.object(Agent, '_decision', return_value='1')
    @patch.object(a_s.core.Game, 'moves', return_value=('1', '2', '3'))
    def test_select_move__no_moves_parameter(self, mock_moves, mock_decision, game):
        assert self.agent.select_move(game) == '1'
        mock_moves.assert_called_once_with()
        mock_decision.assert_called_once_with(('1', '2', '3'), game)

    @patch.object(Agent, '_decision')
    @patch.object(a_s.core.Game, 'moves', return_value=None)
    def test_select_move__no_moves(self, mock_moves, mock_decision, game):
        assert self.agent.select_move(game) is None
        mock_moves.assert_called_once_with()
        mock_decision.assert_not_called()

    def test__decision(self):
        assert self.agent._decision(['1', '2', '3'], None) is None

    def test_match_begins(self, game):
        assert self.agent.player is None
        self.agent.match_begins("player", game)
        assert self.agent.player == "player"

    def test_match_moves(self, game):
        assert self.agent.match_moves(game, "1", game) is None

    def test_match_ends(self, game):
        assert self.agent.match_ends(game) is None

    def test_str(self):
        self.agent.player = "player"
        assert str(self.agent) == "test agent(player)"


class TestRandomAgent:
    def setup(self):
        self.agent = RandomAgent(name="test agent")

    def test_init(self):
        assert issubclass(RandomAgent, Agent)
        assert isinstance(self.agent, RandomAgent)
        assert isinstance(self.agent.random, random.Random)

    def test__decision__result(self):
        moves = ['1', '2', '3']
        move = self.agent._decision(moves)
        assert move in moves

    def test__decision(self):
        moves = ['1', '2', '3']
        with patch.object(self.agent, 'random') as mock_random:
            mock_random.choice.return_value = "2"
            move = self.agent._decision(moves)
            mock_random.choice.assert_called_once_with(moves)
        assert move == "2"


class TestMiniMaxAgent:
    def setup(self):
        self.agent = MiniMaxAgent(name="test agent")

    def test_init(self):
        assert issubclass(MiniMaxAgent, Agent)
        assert isinstance(self.agent, MiniMaxAgent)
        assert isinstance(self.agent.horizon, int)
        assert isinstance(self.agent.random, random.Random)

    @patch.object(MiniMaxAgent, '_minimax', return_value=1)
    @patch.object(a_s.core.Game, 'next', return_value=game)
    def test__decision(self, mock_game_next, mock__minimax, game):
        moves = ['1', '2', '3']
        move = self.agent._decision(moves, game)

        assert mock_game_next.call_count == len(moves)
        mock_game_next.assert_has_calls([call(move) for move in moves])
        assert mock__minimax.call_count == len(moves)
        mock__minimax.assert_has_calls([call(mock_game_next.return_value, 1)]*len(moves))
        assert move in moves

    @patch.object(MiniMaxAgent, 'heuristic')
    @patch.object(a_s.core.Game, 'results', return_value={'A': 1})
    def test_terminal_value__game_ended(self, mock_results, mock_heuristic, game):
        self.agent.player = "A"
        result = self.agent.terminal_value(game, 1)
        mock_results.assert_called_once_with()
        assert result == mock_results.return_value[self.agent.player]
        mock_heuristic.assert_not_called()

    @pytest.mark.parametrize("horizon_delta, value",
                             [(-1, None),
                              (0, 1),
                              (1, 1),
                              ])
    @patch.object(MiniMaxAgent, 'heuristic')
    @patch.object(a_s.core.Game, 'results', return_value={})
    def test_terminal_value__game_not_ended(self, mock_results, mock_heuristic, horizon_delta, value, game):
        depth = self.agent.horizon + horizon_delta
        mock_heuristic.return_value = value
        result = self.agent.terminal_value(game, depth)
        mock_results.assert_called_once_with()
        if value:
            mock_heuristic.assert_called_once_with(game, depth)
        else:
            mock_heuristic.assert_not_called()
        assert result == value

    @patch.object(MiniMaxAgent, 'terminal_value', return_value=-1)
    def test__minimax__terminal(self, mock_terminal_value, game):
        depth = 1
        result = self.agent._minimax(game, depth)
        mock_terminal_value.assert_called_once_with(game, depth)
        assert result == -1

    def test_heuristic__no_function(self, game):
        with patch.object(self.agent, 'random') as mock_random:
            mock_random.random.return_value = 0
            result = self.agent.heuristic(game, 1)
            mock_random.random.assert_called_once_with()
        assert result == -0.5

    def test_heuristic(self, game):
        with patch.object(self.agent, 'random') as mock_random, \
                patch.object(self.agent, '__heuristic__') as mock___heuristic__:
            mock___heuristic__.return_value = 0.5
            result = self.agent.heuristic(game, 1)
            mock___heuristic__.assert_called_once_with(self.agent, game, 1)
            mock_random.assert_not_called()
        assert result == 0.5
class TestSanityAgents:
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
