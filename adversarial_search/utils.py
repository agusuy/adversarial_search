# -*- coding: utf-8 -*-
import itertools

def default_repr(obj):
    """ Implementaci�n por defecto del m�todo __repr__ de un object. Imprime el
        tipo de obj, y los nombres y valores de sus atributos entre par�ntesis. 
    """
    attrs = getattr(obj, '__dict__', {}).items()
    attrs.sort()
    return '%s(%s)' % (type(obj), ', '.join(['%s=%s' % attr for attr in attrs]))


__COLUMNS__ = 'abcdefghijklmnopqrstuvwxyz'


def coord_id(column, row):
    """ Retorna la coordenada en formato letra para la columna y n�meros para 
        la fila. Por ejemplo: coord(1,1) = 'a1', coord(3,7) = 'c7'. 
    """
    # TODO Columnas mayores estilo planilla electr�nica ... z1, aa1, ab1 ...
    return '%s%d' % (__COLUMNS__[column], row + 1)


def iterate(func, count=None):
    """ Generador que llama sin par�metros count veces al callable func. Si
        count es None la repetici�n es indefinida. 
    """
    return [func() for _ in itertools.repeat(None, count)]


def flip_dict(dict_dict):
    """ Recibe un dict de dict, de la forma {k1:{k2:v}} y retorna otro de la 
        forma {k2:{k1:v}}
    """
    resultado = {}
    for key1, dict1 in dict_dict.iteritems():
        for key2, value in dict1.iteritems():
            resultado.setdefault(key2, {})[key1] = value
    return resultado

# Funciones de manejo del tablero ##############################################

def print_board(board, rows, cols, row_sep='', col_sep='', joint_sep='', row_fmt='%s\n'):
    """ Retorna el tablero en formato tabular.
    """
    row_sep = row_fmt % joint_sep.join(row_sep * cols) if row_sep else ''
    return row_sep.join([row_fmt % col_sep.join(board[row * cols:(row + 1) * cols]) for row in range(rows)])


def board_rows(board, rows, cols):
    """ Retorna las filas de un tablero con sus casillas.
    """
    return [''.join(board[row * cols:(row + 1) * cols]) for row in range(rows)]


def board_columns(board, rows, cols):
    """ Retorna las columnas de un tablero con sus casillas.
    """
    return [''.join([board[row * cols + col] for row in range(rows)]) for col in range(cols)]


def board_indexed(board, rows, cols):
    """ Retorna las casillas del tablero indexadas, es decir tuplas (fila, 
        columna, casilla).
    """
    return [(row, col, board[row * cols + col]) for row in range(rows) for col in range(cols)]


def board_pdiags(board, rows, cols):
    """ Retorna las diagonales positivas del tablero con sus casillas.
    """
    return [''.join([b for r, c, b in board_indexed(board, rows, cols) if s == r + c]) for s in range(rows + cols - 1)]


def board_ndiags(board, rows, cols):
    """ Retorna las diagonales negativas del tablero con sus casillas.
    """
    return [''.join([b for r, c, b in board_indexed(board, rows, cols) if s == c - r]) for s in range(1 - rows, cols)]


def board_diags(board, rows, cols):
    """ Retorna las diagonales del tablero con sus casillas.
    """
    for x in board_pdiags(board, rows, cols):
        yield x
    for x in board_ndiags(board, rows, cols):
        yield x


def board_orths(board, rows, cols):
    """ Retorna las filas y columnas del tablero con sus casillas.
    """
    for x in board_rows(board, rows, cols):
        yield x
    for x in board_columns(board, rows, cols):
        yield x


def board_lines(board, rows, cols):
    """ Retorna las l�neas del tablero con sus casillas.
    """
    for x in board_orths(board, rows, cols):
        yield x
    for x in board_diags(board, rows, cols):
        yield x


# Resultados de juego ##########################################################

def resultado(jugador, jugadores, valor=1):
    """ Retorna un dict con todos los jugadores menos jugador con resultado
        -valor. El resultado de jugador se ajusta para que la suma de resultados 
        sea cero.
        Por defecto (valor=1) marca a jugador como ganador. Para marcar a 
        jugador como perdedor usar valor=-1. Si valor=0 se tiene un empate.
        Si valor es None se retorna None.
    """
    if valor is None:
        return None
    else:
        r = dict([(j, -valor) for j in jugadores if j != jugador])
        r[jugador] = valor * (len(jugadores) - 1)
        return r


# Decorators ###################################################################

def cached_property(cache_name):
    """ Decorator for parameterless methods that caches the returned value inside
        an attribute of the object, named as cache_name.
    """

    def decorator(f):
        def decorated(self, *args, **kargs):
            if not hasattr(self, cache_name):
                setattr(self, cache_name, f(self, *args, **kargs))
            return getattr(self, cache_name)

        return decorated

    return decorator


def cached_indexed_property(cache_name):
    """ Decorator for methods with one parameter that caches the returned value
        in a dict inside an attribute of the object, named as cache_name.
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
