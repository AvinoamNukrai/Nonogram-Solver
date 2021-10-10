# intro2cs1, 2019, ex8_helper.py
# DO NOT submit this file (we already have it (: )
# Matan Levy

import re


WHITE_BLANK_REP = 0
BLACK_BLANK_REP = 1
WHITE_BLANK = "_"
BLACK_BLANK = "X"
UNKNOWN_BLANK = "?"
CHR_SEPARATOR = " "
LINE_REGEX = "(?:[1]*)"
LINE_SEPARATOR = " "
REPLACE_FROM = "-1"
REPLACE_TO = "0"


def print_board(board):
    """
    This function prints the input board game to the screen.
    :param board: The matrix that represents the game board.
    :return: None
    """
    rep_str = ""
    for row in board:
        for blank in row:
            if blank == WHITE_BLANK_REP:
                rep_str += WHITE_BLANK
            elif blank == BLACK_BLANK_REP:
                rep_str += BLACK_BLANK
            else:
                rep_str += UNKNOWN_BLANK
            rep_str += CHR_SEPARATOR
        rep_str += "\n"
    print(rep_str)


def get_line_constraints(lst):
    """
    This function gets a list of 1,0,-1 and returns the constraints of this line (with respect to 1)
    :param lst: a list of 0,1,-1
    :return: constraints list
    """
    return [len(group) for group in LINE_SEPARATOR.join(
        list(re.findall(LINE_REGEX, "".join(map(str, lst)).replace(REPLACE_FROM, REPLACE_TO)))).split()]


if __name__ == "__main__":
    pass



