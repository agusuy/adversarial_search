# -*- coding: utf-8 -*-
import random

class Game(object): ################################################################################
    """ Base class for all game components. The instance represents a game state, including 
        information about the board, the pieces, the players and any other data required to continue
	   the game. 
    """

    def __init__(self, *players):
        """ The constructor initializes the object to represent the game's initial state. Players 
            list indicates the players that will participate in the game. These are not the actual 
            agents in charge of moving, but only their role. Examples are 'Xs' and 'Os' or 'Whites'
            and 'Blacks'. Subclasses must support an empty or None players parameter, indicating a
            default option. A player may be any hashable type, but str is recommended.
        """
        self.players = players

    def active_player(self):
        """ Returns the player enabled to make moves in the current game state.
        """
        raise NotImplementedError('Class %s has not implemented method active_player.' % self.__class__.__name__)

    def moves(self):
        """ Returns all valid moves in the game state for the active player. If the game has 
            finished, it should be an empty sequence.
        """
        raise NotImplementedError('Class %s has not implemented method moves.' % self.__class__.__name__)

    def results(self):
        """ Returns the results of a finished game for every player. This will be a dict of the form
            `{player:float}`. Draws are always 0, with victory results being always positive and 
		  defeat always negative. Must return an empty dict if the game is not finished.
        """
        raise NotImplementedError('Class %s has not implemented method results.' % self.__class__.__name__)

    def next(self, move):
        """ Calculates and returns the next game state applying the given move. The moves parameter
            is one of the values returned by the moves method. Result should be None if any move is
            invalid or game has ended.
        """
        raise NotImplementedError('Class %s has not implemented method next.' % self.__class__.__name__)

    def __hash__(self):
        return hash(repr(self))

class Agent(object): ###############################################################################
    """ Base class for agents participating in games.
    """

    def __init__(self, name):
        self.name = name
        self.player = None

    def decision(self, game, *moves):
        """ Agents move choice. If no moves are provided, choices are retrieved from the game.
        """
        if not moves:
            moves = game.moves()
            if not moves:
                return None
        return self._decision(moves)

    def _decision(self, moves):
        """ Method called by Agent.decision() to actually make the choice of move. This should be 
            overriden by subclasses.
        """
        return moves[0]  # Please do not use this default implementation.

    def match_begins(self, player, game):
        """ Tells the agent that a match he is participating in is starting. This should not be 
            called again until the match ends.
        """
        self.player = player

    def match_moves(self, before, move, after):
        """ Tells the agent the active player have moved in the match he is participating in.
        """
        pass

    def match_ends(self, game):
        """ Tells the agent the match he was participating in has finished. The game parameter holds
            the final game state.
        """
        pass

    def __str__(self):
        return '%s(%s)' % (self.name, self.player)

    def __hash__(self):
        return self.name.__hash__()
    
    def randgen(self, x):
        """ If x is `None` or `int` or `long`, returns random.Random(x), else returns x.
        """
        return random.Random(x) if x is None or type(x) == int else x 

# Match ############################################################################################

def match(game, *agents_list, **agents): 
    """ A match controller in the form of a generator. Participating agents can be specified either
        as a list (agents_list) or pairs player=agent. If the list is used, agents are assigned in
        the same order as the game players.

        The generator returns tuples. First `(0, agents, initial game state)`. After that 
	   `(move_number, move, game state)` for each move. Finally `(None, results, 
	   final game state)`. The generator handles the match, asking the enabled agents to move,
        keeping track of game states and notifying all agents as needed.
    """
    for player, agent in zip(game.players, agents_list):
        agents[player] = agent
    for player, agent in agents.items():  # Tells all agents the match begins.
        agent.match_begins(player, game)
    move_num = 0
    yield (move_num, agents, game)
    results = game.results()
    while not results:  # Game is not over.
        chosen_move = agents[game.active_player()].decision(game)
        next_game = game.next(chosen_move)
        for player, agent in agents.items():  # Tells all agents about the moves.
            agent.match_moves(game, chosen_move, next_game)
        game = next_game
        move_num += 1
        yield (move_num, chosen_move, game)
        results = game.results()
    for player, agent in agents.items():  # Tells all agentes the match ends.
        agent.match_ends(game)
    yield (None, results, game)


def run_match(game, *agents_list, **agents):
    """ Runs a full match returning the results and final game state.
    """
    for m, d, g in match(game, *agents_list, **agents):
        if m is None:  # Game over.
            return (d, g)
    return (None, game)  # Should not happen.
