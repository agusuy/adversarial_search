from examples.tictactoe import TicTacToe
from examples.toads_and_frogs import ToadsFrogs
from tests.test_game import GameTest


class TestTicTacToe(GameTest):
    """ TicTacToe test cases.
    """

    def test_basic(self):
        self.basic_test(TicTacToe)

    def test_traces(self):
        self.trace_test_text(TicTacToe(), """\
            X[.........] Xs b2
            O[....X....] Os a1
            X[O...X....] Xs a2
            O[OX..X....] Os a3
            X[OXO.X....] Xs c2
            """, Xs=1, Os=-1)
        self.trace_test_text(TicTacToe(), """\
            X[.........] Xs a2
            O[.X.......] Os b2
            X[.X..O....] Xs c2
            O[.X..O..X.] Os a1
            X[OX..O..X.] Xs a3
            O[OXX.O..X.] Os c3
            """, Xs=-1, Os=1)


class TestToadsFrogs(GameTest):
    """ Toads and Frogs test cases
    """

    def test_basic(self):
        self.basic_test(ToadsFrogs)

    def test_trace(self):
        self.trace_test_text(ToadsFrogs(None, 0, 3, 2), """\
            T[TTT__FFF] Toads a3
            F[TT_T_FFF] Frogs a6
            T[TT_TF_FF] Toads a2
            F[T_TTF_FF] Frogs a7
            T[T_TTFF_F] Toads a1
            F[_TTTFF_F] Frogs a8
            """, Toads=-1, Frogs=1)

        self.trace_test_text(ToadsFrogs(None, 0, 2, 1), """\
            T[TT_FF] Toads a2
            F[T_TFF] Frogs a4
            T[TFT_F] Toads a3
            F[TF_TF] Frogs a5
            T[TFFT_] Toads a4
            """, Toads=1, Frogs=-1)
