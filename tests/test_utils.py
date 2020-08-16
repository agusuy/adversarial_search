import pytest

from .context import adversarial_search as a_s


class TestUtils:
    """ Test cases for utils
    """

    @pytest.mark.parametrize("col, row, expected_coord",
                             [(0, 0, 'a1'),
                              (2, 6, 'c7'),
                              (3, 7, 'd8'),
                              ])
    def test_coord(self, col, row, expected_coord):
        """ Test utils.coord_id(column, row)
        """
        assert a_s.utils.coord_id(col, row) == expected_coord

    def test_coord_main_diagonal(self):
        """ Test utils.coord_id(column, row)
        """
        columns = list(a_s.utils.__COLUMNS__)
        for i, col in zip(range(len(columns)), columns):
            assert col + str(i + 1) == a_s.utils.coord_id(i, i)

    @pytest.mark.parametrize("board, rows, cols, row_sep, col_sep, joint_sep, row_fmt, expected_print",
                             [('A', 1, 1, '!', '!', '!', '%s\n', 'A\n'),
                              ('ABCD', 2, 2, '', '', '', '%s\n', 'AB\nCD\n'),
                              ('ABCD', 2, 2, '-', '|', '', '%s\n', 'A|B\n--\nC|D\n'),
                              ('ABCD', 2, 2, '-', '|', '+', '%s\n', 'A|B\n-+-\nC|D\n'),
                              ('ABCD', 2, 2, '', '|', '+', '%s\n', 'A|B\nC|D\n'),
                              ('ABCD', 2, 2, '', '', '', '|%s|\n', '|AB|\n|CD|\n'),
                              ('ABCD', 2, 2, '-', '', '', '|%s|\n', '|AB|\n|--|\n|CD|\n'),
                              ('ABCDEF', 3, 2, '', '', '', '%s\n', 'AB\nCD\nEF\n'),
                              ('ABCDEF', 2, 3, '', '', '', '%s\n', 'ABC\nDEF\n'),
                              (" " * 9, 3, 3, "-", "|", "+", '%s\n', ' | | \n-+-+-\n | | \n-+-+-\n | | \n'),
                              ])
    def test_print_board(self, board, rows, cols, row_sep, col_sep, joint_sep, row_fmt, expected_print):
        """ Test utils.print_board(board, rows, cols, row_sep, col_sep, joint_sep, row_fmt)
        """
        assert a_s.utils.print_board(board, rows, cols, row_sep, col_sep, joint_sep, row_fmt) == expected_print

    @pytest.mark.parametrize("board, row_num, col_num, expected_rows, expected_cols",
                             [('A', 1, 1, ['A'], ['A']),
                              ('ABCD', 2, 2, ['AB', 'CD'], ['AC', 'BD']),
                              ('ABCDEFGHI', 3, 3, ['ABC', 'DEF', 'GHI'], ['ADG', 'BEH', 'CFI']),
                              ('ABCDEF', 3, 2, ['AB', 'CD', 'EF'], ['ACE', 'BDF']),
                              ('ABCDEF', 2, 3, ['ABC', 'DEF'], ['AD', 'BE', 'CF']),
                              ('ABCDEF', 1, 6, ['ABCDEF'], ['A', 'B', 'C', 'D', 'E', 'F']),
                              ('ABCDEF', 6, 1, ['A', 'B', 'C', 'D', 'E', 'F'], ['ABCDEF']),
                              ])
    def test_board_orthogonals(self, board, row_num, col_num, expected_rows, expected_cols):
        """ Testing orthogonal lines (functions board_rows, board_columns, board_orthogonals).
        """
        assert a_s.utils.board_rows(board, row_num, col_num) == expected_rows
        assert a_s.utils.board_columns(board, row_num, col_num) == expected_cols
        assert list(a_s.utils.board_orthogonals(board, row_num, col_num)) == expected_rows + expected_cols

    @pytest.mark.parametrize("board, row_num, col_num, expected_positive_diagonals, expected_negative_diagonals",
                             [('A', 1, 1, ['A'], ['A']),
                              ('ABCD', 2, 2, ['A', 'BC', 'D'], ['C', 'AD', 'B']),
                              ('ABCDEFGHI', 3, 3, ['A', 'BD', 'CEG', 'FH', 'I'], ['G', 'DH', 'AEI', 'BF', 'C']),
                              ('ABCDEF', 3, 2, ['A', 'BC', 'DE', 'F'], ['E', 'CF', 'AD', 'B']),
                              ('ABCDEF', 2, 3, ['A', 'BD', 'CE', 'F'], ['D', 'AE', 'BF', 'C']),
                              ('ABCDEF', 1, 6, ['A', 'B', 'C', 'D', 'E', 'F'], ['A', 'B', 'C', 'D', 'E', 'F']),
                              ('ABCDEF', 6, 1, ['A', 'B', 'C', 'D', 'E', 'F'], ['F', 'E', 'D', 'C', 'B', 'A']),
                              ])
    def test_board_diagonals(self, board, row_num, col_num, expected_positive_diagonals, expected_negative_diagonals):
        """ Testing diagonal lines (functions board_positive_diagonals, board_negative_diagonals, board_diagonals).
        """
        assert a_s.utils.board_positive_diagonals(board, row_num, col_num) == expected_positive_diagonals
        assert a_s.utils.board_negative_diagonals(board, row_num, col_num) == expected_negative_diagonals
        assert list(a_s.utils.board_diagonals(board, row_num, col_num)) == \
               expected_positive_diagonals + expected_negative_diagonals

    @pytest.mark.parametrize("board, rows, cols, expected_lines", [
        ('A', 1, 1,
         ['A', 'A', 'A', 'A']),
        ('ABCD', 2, 2,
         ['AB', 'CD', 'AC', 'BD', 'A', 'BC', 'D', 'C', 'AD', 'B']),
        ('ABCDEFGHI', 3, 3,
         ['ABC', 'DEF', 'GHI', 'ADG', 'BEH', 'CFI', 'A', 'BD', 'CEG', 'FH', 'I', 'G', 'DH', 'AEI', 'BF', 'C']),
        ('ABCDEF', 3, 2,
         ['AB', 'CD', 'EF', 'ACE', 'BDF', 'A', 'BC', 'DE', 'F', 'E', 'CF', 'AD', 'B']),
        ('ABCDEF', 2, 3,
         ['ABC', 'DEF', 'AD', 'BE', 'CF', 'A', 'BD', 'CE', 'F', 'D', 'AE', 'BF', 'C']),
        ('ABCDEF', 1, 6,
         ['ABCDEF', 'A', 'B', 'C', 'D', 'E', 'F', 'A', 'B', 'C', 'D', 'E', 'F', 'A', 'B', 'C', 'D', 'E', 'F']),
        ('ABCDEF', 6, 1,
         ['A', 'B', 'C', 'D', 'E', 'F', 'ABCDEF', 'A', 'B', 'C', 'D', 'E', 'F', 'F', 'E', 'D', 'C', 'B', 'A']),
    ])
    def test_board_lines(self, board, rows, cols, expected_lines):
        """Test utils.board_lines(board, rows, cols)
        """
        assert list(a_s.utils.board_lines(board, rows, cols)) == expected_lines
