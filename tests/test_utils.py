# -*- coding: utf-8 -*-
import unittest

from .context import adversarial_search as a_s


class TestUtils(unittest.TestCase):
    """ Test cases for utils
    """

    def test_coord(self):
        """ Test utils.coord_id(column, row)
        """

        coord_id = a_s.utils.coord_id

        self.assertEqual('a1', coord_id(0, 0))
        self.assertEqual('c7', coord_id(2, 6))
        self.assertEqual('d8', coord_id(3, 7))

        columns = list(a_s.utils.__COLUMNS__)
        for i, col in zip(range(len(columns)), columns):
            self.assertEqual(col + str(i + 1), coord_id(i, i))

    def test_print_board(self):
        """ Test utils.print_board(board, rows, cols, row_sep, col_sep, joint_sep, row_fmt)
        """

        print_board = a_s.utils.print_board

        self.assertEqual('A\n', print_board('A', 1, 1, '!', '!', '!'))
        self.assertEqual('AB\nCD\n', print_board('ABCD', 2, 2))
        self.assertEqual('A|B\n--\nC|D\n', print_board('ABCD', 2, 2, '-', '|'))
        self.assertEqual('A|B\n-+-\nC|D\n', print_board('ABCD', 2, 2, '-', '|', '+'))
        self.assertEqual('A|B\nC|D\n', print_board('ABCD', 2, 2, '', '|', '+'))
        self.assertEqual('|AB|\n|CD|\n', print_board('ABCD', 2, 2, row_fmt='|%s|\n'))
        self.assertEqual('|AB|\n|--|\n|CD|\n', print_board('ABCD', 2, 2, '-', '', '', row_fmt='|%s|\n'))
        self.assertEqual('AB\nCD\nEF\n', print_board('ABCDEF', 3, 2))
        self.assertEqual('ABC\nDEF\n', print_board('ABCDEF', 2, 3))

        self.assertEqual(' | | \n-+-+-\n | | \n-+-+-\n | | \n',
                         print_board(" " * 9, 3, 3, row_sep="-", col_sep="|", joint_sep="+"))

    def test_board_orthogonals(self):
        """ Testing orthogonal lines (functions board_rows, board_columns, board_orthogonals).
        """
        board_rows = a_s.utils.board_rows
        board_columns = a_s.utils.board_columns
        board_orthogonal = a_s.utils.board_orthogonals

        def _test_orthogonals(board, row_num, col_num, expected_rows, expected_cols):
            self.assertEqual(expected_rows, board_rows(board, row_num, col_num))
            self.assertEqual(expected_cols, board_columns(board, row_num, col_num))
            self.assertEqual(expected_rows + expected_cols, list(board_orthogonal(board, row_num, col_num)))

        _test_orthogonals('A', 1, 1, ['A'], ['A'])
        _test_orthogonals('ABCD', 2, 2, ['AB', 'CD'], ['AC', 'BD'])
        _test_orthogonals('ABCDEFGHI', 3, 3, ['ABC', 'DEF', 'GHI'], ['ADG', 'BEH', 'CFI'])
        _test_orthogonals('ABCDEF', 3, 2, ['AB', 'CD', 'EF'], ['ACE', 'BDF'])
        _test_orthogonals('ABCDEF', 2, 3, ['ABC', 'DEF'], ['AD', 'BE', 'CF'])
        _test_orthogonals('ABCDEF', 1, 6, ['ABCDEF'], ['A', 'B', 'C', 'D', 'E', 'F'])
        _test_orthogonals('ABCDEF', 6, 1, ['A', 'B', 'C', 'D', 'E', 'F'], ['ABCDEF'])

    def test_board_diagonals(self):
        """ Testing diagonal lines (functions board_positive_diagonals, board_negative_diagonals, board_diagonals).
        """
        board_positive_diagonals = a_s.utils.board_positive_diagonals
        board_negative_diagonals = a_s.utils.board_negative_diagonals
        board_diagonals = a_s.utils.board_diagonals

        def _test_diagonals(board, row_num, col_num, expected_positive_diagonals, expected_negative_diagonals):
            self.assertEqual(expected_positive_diagonals, board_positive_diagonals(board, row_num, col_num))
            self.assertEqual(expected_negative_diagonals, board_negative_diagonals(board, row_num, col_num))
            self.assertEqual(expected_positive_diagonals + expected_negative_diagonals,
                             list(board_diagonals(board, row_num, col_num)))

        _test_diagonals('A', 1, 1, ['A'], ['A'])
        _test_diagonals('ABCD', 2, 2, ['A', 'BC', 'D'], ['C', 'AD', 'B'])
        _test_diagonals('ABCDEFGHI', 3, 3, ['A', 'BD', 'CEG', 'FH', 'I'], ['G', 'DH', 'AEI', 'BF', 'C'])
        _test_diagonals('ABCDEF', 3, 2, ['A', 'BC', 'DE', 'F'], ['E', 'CF', 'AD', 'B'])
        _test_diagonals('ABCDEF', 2, 3, ['A', 'BD', 'CE', 'F'], ['D', 'AE', 'BF', 'C'])
        _test_diagonals('ABCDEF', 6, 1, ['A', 'B', 'C', 'D', 'E', 'F'], ['F', 'E', 'D', 'C', 'B', 'A'])
        _test_diagonals('ABCDEF', 1, 6, ['A', 'B', 'C', 'D', 'E', 'F'], ['A', 'B', 'C', 'D', 'E', 'F'])


if __name__ == "__main__":
    unittest.main()
