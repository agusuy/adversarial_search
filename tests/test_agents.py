""" Test cases for module agents.
"""
import random
from itertools import combinations
from unittest.mock import patch, call, MagicMock

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


class DummyGame(a_s.Game):

    def active_player(self):
        pass

    def moves(self):
        pass

    def results(self):
        pass

    def next(self, move):
        pass


INF = a_s.agents.alphabeta.INFINITE
TEST_GAME = DummyGame()


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
    @patch.object(DummyGame, 'moves')
    def test_select_move(self, mock_moves, mock_decision):
        assert self.agent.select_move(TEST_GAME, *['1', '2', '3']) == '1'
        mock_moves.assert_not_called()
        mock_decision.assert_called_once_with(('1', '2', '3'), TEST_GAME)

    @patch.object(Agent, '_decision', return_value='1')
    @patch.object(DummyGame, 'moves', return_value=('1', '2', '3'))
    def test_select_move__no_moves_parameter(self, mock_moves, mock_decision):
        assert self.agent.select_move(TEST_GAME) == '1'
        mock_moves.assert_called_once_with()
        mock_decision.assert_called_once_with(('1', '2', '3'), TEST_GAME)

    @patch.object(Agent, '_decision')
    @patch.object(DummyGame, 'moves', return_value=None)
    def test_select_move__no_moves(self, mock_moves, mock_decision):
        assert self.agent.select_move(TEST_GAME) is None
        mock_moves.assert_called_once_with()
        mock_decision.assert_not_called()

    def test__decision(self):
        assert self.agent._decision(['1', '2', '3'], None) is None

    def test_match_begins(self):
        assert self.agent.player_type is None
        self.agent.match_begins("player", TEST_GAME)
        assert self.agent.player_type == "player"

    def test_match_moves(self):
        assert self.agent.match_moves(TEST_GAME, "1", TEST_GAME) is None

    def test_match_ends(self):
        assert self.agent.match_ends(TEST_GAME) is None

    def test_str(self):
        self.agent.player_type = "player"
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
    @patch.object(DummyGame, 'next', return_value=TEST_GAME)
    def test__decision(self, mock_game_next, mock__minimax):
        moves = ['1', '2', '3']
        move = self.agent._decision(moves, TEST_GAME)

        assert mock_game_next.call_count == len(moves)
        mock_game_next.assert_has_calls([call(move) for move in moves])
        assert mock__minimax.call_count == len(moves)
        mock__minimax.assert_has_calls([call(mock_game_next.return_value, 1)] * len(moves))
        assert move in moves

    @patch.object(MiniMaxAgent, 'heuristic')
    @patch.object(DummyGame, 'results', return_value={'A': 1})
    def test_terminal_value__game_ended(self, mock_results, mock_heuristic):
        self.agent.player_type = "A"
        result = self.agent.terminal_value(TEST_GAME, 1)
        mock_results.assert_called_once_with()
        assert result == mock_results.return_value[self.agent.player_type]
        mock_heuristic.assert_not_called()

    @pytest.mark.parametrize("horizon_delta, value",
                             [(-1, None),
                              (0, 1),
                              (1, 1),
                              ])
    @patch.object(MiniMaxAgent, 'heuristic')
    @patch.object(DummyGame, 'results', return_value={})
    def test_terminal_value__game_not_ended(self, mock_results, mock_heuristic, horizon_delta, value):
        depth = self.agent.horizon + horizon_delta
        mock_heuristic.return_value = value
        result = self.agent.terminal_value(TEST_GAME, depth)
        mock_results.assert_called_once_with()
        if value:
            mock_heuristic.assert_called_once_with(TEST_GAME, depth)
        else:
            mock_heuristic.assert_not_called()
        assert result == value

    @patch.object(MiniMaxAgent, 'terminal_value', return_value=-1)
    def test__minimax__terminal(self, mock_terminal_value):
        depth = 1
        result = self.agent._minimax(TEST_GAME, depth)
        mock_terminal_value.assert_called_once_with(TEST_GAME, depth)
        assert result == -1

    @patch("adversarial_search.agents.minimax.min", side_effect=min)
    @patch("adversarial_search.agents.minimax.max", side_effect=max)
    @patch.object(DummyGame, 'active_player', side_effect=['A', 'B', 'B'])
    @patch.object(DummyGame, 'next')
    @patch.object(DummyGame, 'moves', return_value=('1', '2'))
    @patch.object(MiniMaxAgent, 'terminal_value', side_effect=[None, None, 1, 1, None, 1, 1])
    def test__minimax(self, mock_terminal_value, mock_moves, mock_next, mock_active_player, mock_max, mock_min):
        self.agent.player_type = "A"
        mock_next.return_value = TEST_GAME

        mock__minimax = MagicMock(side_effect=self.agent._minimax)
        self.agent._minimax = mock__minimax

        depth = 1

        result = self.agent._minimax(TEST_GAME, depth)

        assert result == 1
        assert mock_max.call_count == 1
        assert mock_min.call_count == 2
        assert mock_moves.call_count == 3
        assert mock_terminal_value.call_count == 7
        mock_terminal_value.assert_has_calls([
            call(TEST_GAME, depth),
            call(TEST_GAME, depth + 1),
            call(TEST_GAME, depth + 2),
            call(TEST_GAME, depth + 2),
            call(TEST_GAME, depth + 1),
            call(TEST_GAME, depth + 2),
            call(TEST_GAME, depth + 2)
        ])
        assert mock__minimax.call_count == 7
        mock__minimax.assert_has_calls([
            call(TEST_GAME, depth),
            call(TEST_GAME, depth + 1),
            call(TEST_GAME, depth + 2),
            call(TEST_GAME, depth + 2),
            call(TEST_GAME, depth + 1),
            call(TEST_GAME, depth + 2),
            call(TEST_GAME, depth + 2),
        ])

    def test_heuristic__no_function(self):
        with patch.object(self.agent, 'random') as mock_random:
            mock_random.random.return_value = 0
            result = self.agent.heuristic(TEST_GAME, 1)
            mock_random.random.assert_called_once_with()
        assert result == -0.5

    def test_heuristic(self):
        with patch.object(self.agent, 'random') as mock_random, \
                patch.object(self.agent, '__heuristic__') as mock___heuristic__:
            mock___heuristic__.return_value = 0.5
            result = self.agent.heuristic(TEST_GAME, 1)
            mock___heuristic__.assert_called_once_with(self.agent, TEST_GAME, 1)
            mock_random.assert_not_called()
        assert result == 0.5


class TestAlphaBetaAgent:
    def setup(self):
        self.agent = AlphaBetaAgent(name="test agent")

    def test_init(self):
        assert issubclass(AlphaBetaAgent, Agent)
        assert isinstance(self.agent, AlphaBetaAgent)

    @patch.object(AlphaBetaAgent, 'terminal_value', return_value=-1)
    def test__minimax__terminal(self, mock_terminal_value):
        depth = 1
        result = self.agent._minimax(TEST_GAME, depth)
        mock_terminal_value.assert_called_once_with(TEST_GAME, depth)
        assert result == -1

    minimax_test_cases = [
        (['A', ], [None, -1, 3], [-INF, INF], 3,
         [call(TEST_GAME, 1, -INF, INF), call(TEST_GAME, 2, -INF, INF), call(TEST_GAME, 2, -1, INF)]),
        (['B', ], [None, 3, 5], [-INF, INF], 3,
         [call(TEST_GAME, 1, -INF, INF), call(TEST_GAME, 2, -INF, INF), call(TEST_GAME, 2, -INF, 3)]),
        (['A', ], [None, 5], [-INF, 3], 5, [call(TEST_GAME, 1, -INF, 3), call(TEST_GAME, 2, -INF, 3)]),
        (['B', ], [None, -4], [3, INF], -4, [call(TEST_GAME, 1, 3, INF), call(TEST_GAME, 2, 3, INF)]),
        (['A', 'B', 'A', 'A', 'B', 'A'],
         [None, None, None, -1, 3, None, 5, None, None, -6, -4],
         [-INF, INF], 3,
         [call(TEST_GAME, 1, -INF, INF),
          call(TEST_GAME, 2, -INF, INF),
          call(TEST_GAME, 3, -INF, INF),
          call(TEST_GAME, 4, -INF, INF),
          call(TEST_GAME, 4, -1, INF),
          call(TEST_GAME, 3, -INF, 3),
          call(TEST_GAME, 4, -INF, 3),
          call(TEST_GAME, 2, 3, INF),
          call(TEST_GAME, 3, 3, INF),
          call(TEST_GAME, 4, 3, INF),
          call(TEST_GAME, 4, 3, INF)]),
    ]

    @pytest.mark.parametrize(
        "active_player_returns, terminal_value_returns, call_args, expected_result, expected_calls", minimax_test_cases,
        ids=['max_player_no_pruning', 'min_player_no_pruning', 'max_player_pruning', 'min_player_pruning', 'all'])
    @patch.object(DummyGame, 'active_player')
    @patch.object(DummyGame, 'next')
    @patch.object(DummyGame, 'moves', return_value=('1', '2'))
    @patch.object(MiniMaxAgent, 'terminal_value')
    def test__minimax(
            self, mock_terminal_value, mock_moves, mock_next, mock_active_player,
            active_player_returns, terminal_value_returns, call_args, expected_result, expected_calls):
        mock_active_player.side_effect = active_player_returns
        mock_terminal_value.side_effect = terminal_value_returns
        mock_next.return_value = TEST_GAME

        self.agent.player_type = "A"

        mock__minimax = MagicMock(side_effect=self.agent._minimax)
        self.agent._minimax = mock__minimax

        result = self.agent._minimax(TEST_GAME, 1, *call_args)

        assert result == expected_result
        mock__minimax.assert_has_calls(expected_calls)


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
