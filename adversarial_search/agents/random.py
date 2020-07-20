# -*- coding: utf-8 -*-
from ..core import Agent


class RandomAgent(Agent):
    """ An agent that moves randomly.
    """

    def __init__(self, random=None, name='RandomAgent'):
        Agent.__init__(self, name)
        # An instance of random.Random or equivalent is expected, else an 
        # integer seed or None to create a random.Random.
        self.random = self.randgen(random)

    def _decision(self, moves):
        return self.random.choice(moves)
