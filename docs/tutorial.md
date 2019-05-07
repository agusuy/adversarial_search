# Adversarial Search Framework Tutorial

The following tutorial explains the use of the Adversarial Search framework. As an example we will explain how to implement the game _"Toads and Frogs"_.

The game consists in a strip of n positions where an x amount of toads and frogs pieces can be place, and an y amount of empty spaces following the relation n = 2*x + y. Usually all the toads to the left and all frogs to the right, and leaving the empty places in the middle. The toads will move only to the right and frogs only to the left. A piece can only move to an adjacent position only if it is empty, but if there is piece of the other player, the piece can jump to the following position if it is empty. If non of those conditions apply, the piece has no possible movements. The game ends when a player has no possible movements to do.

Imagine that we have the following initial board: TT_FF, where the movements will be numbered from 0 to 4 from left to right. A possible game could be:

| Player | Movement |        Result        |
|:------:|:--------:|:--------------------:|
|  Toads |     1    |         T_TFF        |
|  Frogs |     3    |         TFT_F        |
|  Toads |     2    |         TF_TF        |
|  Frogs |     4    |         TFFT_        |
|  Toads |     3    |         TFF_T        |
|  Frogs |     _    | Frogs loose the game |

In the framework directory we have the main modules **_core_** and **utils**, and the folders **agents** and **games**.

## **core**

This module contains all the classes and functions required to implement and execute a new game. It includes the class **Game** and 2 functions **match** and **run_match**.

### **Game**

The class **Game** is the superclass for all games. To implement our game "Toads and Frogs" we have to implement a subclass of **Game**, where will we define the game players and its constructor in the following way:

```python
class Toads_Frogs(Game):
    """ Game component for Toads and Frogs
    """

    PLAYERS = ('Toads', 'Frogs')

    def __init__(self, board=None, enabled=0, chips_per_player=3, empty_spaces=2):
        Game.__init__(self, *Toads_Frogs.PLAYERS)
        if board:
            self.board = board
        else:
            self.board = 'T' * chips_per_player + '_' * empty_spaces + 'F' * chips_per_player
        self.enabled = enabled
```

The constructor will initialize the players and the board. The board can be given, or generated automatically based on the number of pieces of each player and amount of empty spaces. The board and the active player represents a state of the game.

To define a game we need to implement the following methods from the class **Games**: **moves**, **result**, and **next**.

The method **moves** calculates all the possible moves for each of the players. It returns a dictionary with elements in the form of **player**: **movements**, where movements is a list with the possible movements for the player in the current game state. The players that are not active (the ones that don't play this turn) should have an empty list, or not appear in the list. If the game has ended, the result must ne **None**. 

In out implementation of "Toads and Frogs", depending on the active player we will search the indexes of the positions where there is a piece with a possible move and will add it to a list. Note that in order to represent a movement an int is not used directly but instead an object of the class **_Move** is used, that is a subclass of **int**, that will serve as a better and clearer representation as an **str** (overriding the **\_\_str\_\_** method). If there are no movements the player will be finish and **None** will be return. Otherwise a dictionary with an only element corresponding to the active player and its list of movements will be return.

```python
class _Move(int):
    def __str__(self):
        return coord_id(0, self)

    def moves(self):
        if not self.enabled:  # Toads move
            moves = [self._Move(pos) for pos in range(len(self.board)) if
                     self.board[pos:].startswith('T_') or self.board[pos:].startswith('TF_')]
        else:  # Frogs move
            moves = [self._Move(pos) for pos in range(len(self.board)) if
                     self.board[:pos + 1].endswith('_F') or self.board[:pos + 1].endswith('_TF')]
        return moves
```

The **result** method looks at the game sate and determines if the game has finish or not. If it has not finish the method returns **None** or an empty dictionary, otherwise it will return the result of the game for each of the players. The result will consist on a dictionary in the form **{player: result}**, where result will be 0 if it ends in draw, a positive number if the player has won or negative if it lost. Different positive or negative values cloud represent different levels of victory or defeat, in case we would like to show how good was the victory or how bad was the defeat.

For "Toads and Frogs" we have to analyze the active player movements. If ths has no more movements the game will end with a defeat for him, if not the game will continue. Because of the characteristics of the game there is no draw result. Depending on the active player we will identify if it has a movement or not. If it has movements we will return **None**, if not we will call the the function **game_result** from the **utils** module. This method get as a parameter a player, a list of players, and result associated to the player. From this result value, a result value for the rest of the players will be calculated and a dictionary with the form **{player: result}** is returned. The result for the player that it gets as a parameter can be modified in a way that the sum of all the result will be 0.

```python
def results(self):
    # There is no draw in this game
    enabled_player = self.players[self.enabled]
    if not self.enabled:
        moves = 'T_' in self.board or 'TF_' in self.board
    else:
        moves = '_F' in self.board or '_TF' in self.board
    if not moves:
        return game_result(enabled_player, self.players, -1)
    return None
```

The **next** method gets as a parameter the movements to do in the turn (dictionary in the form **{player:movements}**), it will process them and return the next game state (resulting board).

In "Toads and Frogs" it has to get the movement of the active player, which is the one that represents the position in the board of the piece to move. So it has to update that position with a value that identifies the new empty space. Later it will have to identify the position where that piece will move, and update the position with the value "T" or "F" accordingly. Last we start a new instance of the game with a new board and the player which is enabled in the next turn.

```python
def next(self, move):
    board_list = list(self.board)
    enabled_player = self.players[self.enabled]
    board_list[move] = '_'
    if not self.enabled:  # A toad moves
        position = move + 1 if board_list[move + 1] == '_' else move + 2
    else:  # A frog moves
        position = move - 1 if board_list[move - 1] == '_' else move - 2
    board_list[position] = enabled_player[0]
    return Toads_Frogs(''.join(board_list), (self.enabled + 1) % 2)
```

It is also convenient to implement the methods **\_\_str\_\_** and **\_\_repr\_\_** that will give a string representations of the game.

```python
def __str__(self):
    return print_board(self.board, 1, len(self.board) + 1)

def __repr__(self):
    return '%s[%s]' % (self.players[self.enabled][0], self.board)
```

### **match** and **run_match**
 Going back to the **core** module, we also have 2 functions: **match** and **run_match**.
 
 * **match** - this is the function that allow us to create a match, and obtain the intermediate results while it is happening. The function can get a list of agents hat will play or a dictionary in the form **{player: agent}**. It is implemented as a generator, that will yield the tuples with the match information. Initially it will return a tuple **(0, agents, initial state of the game)**. Then for every movement it returns a tuple **(movement number, movements, game state)**. When the game is over it returns the tuple **(None, results, final state of the game)**. The generator will handle every aspect of the game, asking the agents for the next movement, calculate the intermediate states of the game and notifying the agents about what is happening in the game.

We can use the following code that will call the **match** method and it iterates over the intermediate results that are generated:

```python
agent1 = RandomAgent(name='Player 1')
agent2 = RandomAgent(name='Player 2')
game = Toads_Frogs(None, 0, 5, 4)
for move_number, moves, game_state in match(game, agent1, agent2):
    if move_number is not None:
        print('%d: %s -> %r' % (move_number, moves, game_state))
    else:
        print('Result: %s' % moves)
        print('Final board: %r' % game_state)
```
  
 * **run_match** - this function is use to run a game, but without getting the intermediate results. The parameters are the same as the other match function, and it returns a tuple **(results, final state of the game)**.
 
 To use it we can do:
 ```python
agent1 = RandomAgent(name='Player 1')
agent2 = RandomAgent(name='Player 2')
game = Toads_Frogs(None, 0, 5, 4)
results, final_state = run_match(game, agent1, agent2)
print('Result: %s' % results)
print('Final board: %r' % final_state)
```

### **Agent**

Also in the **core** module we have the class **Agent** that represents the behaviour of player.

An **Agent** object will have 2 attributes: name and the type of player assigned in the game. It also defines a bunch of methods, some of them corresponding to the agent actions (**decisions**), and others are useful to notify the agent about events that are happening during the game (**match_begins**, **match_moves**, **match_ends**). **decision** will use an auxiliary method _**decision** to chose the movement to perform. This is where the intelligence of the agent resides, so this method has to be overwritten by the subclasses that implement an agent.

The **agents** folder contains some implementations of agents: **AlphaBetaAgent**, **FileAgent**, **MCTSAgent**, **MiniMaxAgent**, and **RandomAgent**.
