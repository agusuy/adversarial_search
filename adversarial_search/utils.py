# -*- coding: utf-8 -*-
import itertools

__COLUMNS__ = 'abcdefghijklmnopqrstuvwxyz'

def coord_id(column, row):
    """ Returns the give coordinate in "spreadsheet format". E.g. `coord(1,1) = 'a1'` and 
        `coord(3,7) = 'c7'`.
    """
    return '%s%d' % (__COLUMNS__[column], row + 1)

# Board handling ###################################################################################

def print_board(board, rows, cols, row_sep='', col_sep='', joint_sep='', row_fmt='%s\n'):
    """ Prints the board in a grid format.
    """
    row_sep = row_fmt % joint_sep.join(row_sep * cols) if row_sep else ''
    return row_sep.join([row_fmt % col_sep.join(board[row * cols:(row + 1) * cols]) for row in range(rows)])


def board_rows(board, rows, cols):
    """ Returns a list of row of the given board.
    """
    return [''.join(board[row * cols:(row + 1) * cols]) for row in range(rows)]


def board_columns(board, rows, cols):
    """ Returns a list of columns of the given board.
    """
    return [''.join([board[row * cols + col] for row in range(rows)]) for col in range(cols)]


def board_indexed(board, rows, cols):
    """ Returns the squares of the given board by index, as a list of tuples `(row, column, square)`.
    """
    return [(row, col, board[row * cols + col]) for row in range(rows) for col in range(cols)]


def board_pdiags(board, rows, cols):
    """ Returns a list of positive diagonals of the given board.
    """
    return [''.join([b for r, c, b in board_indexed(board, rows, cols) if s == r + c]) for s in range(rows + cols - 1)]


def board_ndiags(board, rows, cols):
    """ Returns a list of negative diagonals of the given board.
    """
    return [''.join([b for r, c, b in board_indexed(board, rows, cols) if s == c - r]) for s in range(1 - rows, cols)]


def board_diags(board, rows, cols):
    """ Returns a list of diagonals of the given board.
    """
    for x in board_pdiags(board, rows, cols):
        yield x
    for x in board_ndiags(board, rows, cols):
        yield x


def board_orths(board, rows, cols):
    """ Returns a list of rows and columns of the given board.
    """
    for x in board_rows(board, rows, cols):
        yield x
    for x in board_columns(board, rows, cols):
        yield x


def board_lines(board, rows, cols):
    """ Returns a list of lines of the given board. Lines can be horizontal, vertical or diagonal.
    """
    for x in board_orths(board, rows, cols):
        yield x
    for x in board_diags(board, rows, cols):
        yield x


# Game results #####################################################################################

def game_result(player, players, value=1):
    """ Retorna un dict con todos los jugadores menos jugador con resultado
        -valor. El resultado de jugador se ajusta para que la suma de resultados 
        sea cero.
        Por defecto (valor=1) marca a jugador como ganador. Para marcar a 
        jugador como perdedor usar valor=-1. Si valor=0 se tiene un empate.
        Si valor es None se retorna None.
    """
    if value is None:
        return None
    else:
        r = {p: -value for p in players if p != player}
        r[player] = value * (len(players) - 1)
        return r


# Decorators #######################################################################################

def cached_property(cache_name):
    """ Decorator for parameterless methods that caches the returned value inside an attribute of 
        the object, named as cache_name.
    """
    def decorator(f):
        def decorated(self, *args, **kargs):
            if not hasattr(self, cache_name):
                setattr(self, cache_name, f(self, *args, **kargs))
            return getattr(self, cache_name)
        return decorated

    return decorator

def cached_indexed_property(cache_name):
    """ Decorator for methods with one parameter that caches the returned value in a dict inside an
        attribute of the object, named as cache_name.
    """
    def decorator(f):
        def decorated(self, *args, **kargs):
            cache = getattr(self, cache_name, None)
            if cache is None:
                cache = {}
                setattr(self, cache_name, cache)
            index = args[0]
            if index not in cache:
                cache[index] = f(self, *args, **kargs)
            return cache[index]
        return decorated

    return decorator
