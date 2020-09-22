from unittest.mock import patch

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
