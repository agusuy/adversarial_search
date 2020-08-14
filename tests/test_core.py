import unittest

from .context import adversarial_search as a_s


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = a_s.core.Game(*('A', 'B'))

    def test_players(self):
        self.assertEqual(('A', 'B'), self.game.players)

    def assert_not_implemented(self, function, *args):
        with self.assertRaises(NotImplementedError):
            function(*args)

    def test_active_player(self):
        self.assert_not_implemented(self.game.active_player)

    def test_moves(self):
        self.assert_not_implemented(self.game.moves)

    def test_results(self):
        self.assert_not_implemented(self.game.results)

    def test_next(self):
        self.assert_not_implemented(self.game.next, "move")


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = a_s.core.Agent("test agent")

    def test_name(self):
        self.assertEqual("test agent", self.agent.name)

    def test_decision(self):
        move = self.agent.decision(a_s.core.Game(), *['1', '2', '3'])
        self.assertEqual('1', move)

    def test__decision(self):
        move = self.agent._decision(['1', '2', '3'])
        self.assertEqual('1', move)

    def test_str(self):
        self.assertEqual("test agent(None)", str(self.agent))


if __name__ == '__main__':
    unittest.main()
