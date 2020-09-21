
class Game(object):
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


def match(game, *agents_list, **agents):
    """ A match controller in the form of a generator. Participating agents can be specified either
        as a list (agents_list) or pairs player=agent. If the list is used, agents are assigned in
        the same order as the game players.

        The generator returns tuples. First `(0, agents, initial game state)`. After that
        `(move_number, move, game state)` for each move. Finally `(None, results, final game state)`.
        The generator handles the match, asking the enabled agents to move, keeping track of game states
        and notifying all agents as needed.
    """
    for player, agent in zip(game.players, agents_list):
        agents[player] = agent
    for player, agent in agents.items():  # Tells all agents the match begins.
        agent.match_begins(player, game)
    move_num = 0
    yield (move_num, agents, game)
    results = game.results()
    while not results:  # Game is not over.
        chosen_move = agents[game.active_player()].select_move(game)
        next_game = game.next(chosen_move)
        for player, agent in agents.items():  # Tells all agents about the moves.
            agent.match_moves(game, chosen_move, next_game)
        game = next_game
        move_num += 1
        yield (move_num, chosen_move, game)
        results = game.results()
    for player, agent in agents.items():  # Tells all agents the match ends.
        agent.match_ends(game)
    yield (None, results, game)


def run_match(game, *agents_list, **agents):
    """ Runs a full match returning the results and final game state.
    """
    for m, d, g in match(game, *agents_list, **agents):
        if m is None:  # Game over.
            return (d, g)
    return (None, game)  # Should not happen.
