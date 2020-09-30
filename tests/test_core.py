from unittest.mock import patch, Mock

import pytest

from .context import adversarial_search as a_s

Game = a_s.core.Game


class TestGame:
    @patch.object(Game, '__abstractmethods__', set())
    def setup(self):
        self.game = Game(*('A', 'B'))

    def test_init(self):
        with pytest.raises(TypeError) as e:
            Game()
        assert "Can't instantiate abstract class %s" % Game.__name__ in str(e.value)

    def test_players(self):
        assert self.game.players == ('A', 'B')

    def test_active_player(self):
        assert self.game.active_player() is None

    def test_moves(self):
        assert self.game.moves() is None

    def test_results(self):
        assert self.game.results() is None

    def test_next(self):
        assert self.game.next("move") is None


class TestMatch:

    def test_match(self):
        dummy_game = Mock()
        dummy_agent_1 = Mock()
        dummy_agent_2 = Mock()
        dummy_agent_1.select_move.side_effect = ['1', '2']
        dummy_agent_2.select_move.side_effect = ['1']
        dummy_game.players = ['A', 'B']
        dummy_game.results.side_effect = [
            {},
            {},
            {},
            {'A': 3, 'B': -3}
        ]
        dummy_game.active_player.side_effect = ['A', 'B', 'A', 'B']
        dummy_game.next.side_effect = [dummy_game, dummy_game, dummy_game, dummy_game]

        expected_result = [
            (0, {'A': dummy_agent_1, 'B': dummy_agent_2}, dummy_game),
            (1, '1', dummy_game),
            (2, '1', dummy_game),
            (3, '2', dummy_game),
            (None, {'A': 3, 'B': -3}, dummy_game)
        ]

        result = list(a_s.core.match(dummy_game, dummy_agent_1, dummy_agent_2))

        dummy_agent_1.match_begins.assert_called_once_with('A', dummy_game)
        dummy_agent_2.match_begins.assert_called_once_with('B', dummy_game)
        assert dummy_game.results.call_count == 4
        assert dummy_game.active_player.call_count == 3
        assert dummy_agent_1.select_move.call_count == 2
        assert dummy_agent_2.select_move.call_count == 1
        assert dummy_agent_1.match_moves.call_count == 3
        assert dummy_agent_2.match_moves.call_count == 3
        dummy_agent_1.match_ends.assert_called_once_with(dummy_game)
        dummy_agent_2.match_ends.assert_called_once_with(dummy_game)
        assert result == expected_result

    @patch('adversarial_search.core.match')
    def test_run_match(self, mock_match):
        dummy_game = Mock()
        dummy_agent_1 = Mock()
        dummy_agent_2 = Mock()
        mock_match.return_value = [
            (0, {'A': dummy_agent_1, 'B': dummy_agent_2}, dummy_game),
            (1, '1', dummy_game),
            (2, '1', dummy_game),
            (3, '2', dummy_game),
            (None, {'A': 3, 'B': -3}, dummy_game)
        ]

        result = a_s.core.run_match(dummy_game, dummy_agent_1, dummy_agent_2)

        assert mock_match.call_count == 1
        assert result == ({'A': 3, 'B': -3}, dummy_game)
