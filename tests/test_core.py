import pytest

import adversarial_search.agents.agent
from .context import adversarial_search as a_s


class TestGame:
    def setup(self):
        self.game = a_s.core.Game(*('A', 'B'))

    def test_players(self):
        assert self.game.players == ('A', 'B')

    @staticmethod
    def assert_not_implemented(function, *args):
        with pytest.raises(NotImplementedError):
            function(*args)

    def test_active_player(self):
        self.assert_not_implemented(self.game.active_player)

    def test_moves(self):
        self.assert_not_implemented(self.game.moves)

    def test_results(self):
        self.assert_not_implemented(self.game.results)

    def test_next(self):
        self.assert_not_implemented(self.game.next, "move")
