###############################################################################

# Ex: Ex8 intro2cs 2020 Hebrew University - Nonogram.
# Login: avinoam_nukrai
# Name: Avinoam Nukrai
# ID: 206997132
# Description: The next project is a solution for Nonogram game boards.
# The solution is implemented very efficiently - Backtracking. Enjoy!

###############################################################################

# IMPORT
import math

# GLOBALS
WHITE = 0
BLACK = 1
UNKNOWN = -1


def update_par_helper(row, blocks, add_num):
    """The current function accepts line, line constraint, and integer.The
    purpose of the function is to update the parameters it receives (those
    parameters which the main function receives) according to the
    pointer value. For each of the three possible values, it will
    update the parameters differently"""
    update_pointer_value = 0
    update_row = row[1:]
    update_blocks = blocks[:]
    if add_num == 0:
        update_pointer_value = 0
    elif add_num == 1:
        if len(update_blocks) > 0:
            b = update_blocks[0] - 1
            if b == 0:
                update_pointer_value = -1
                del update_blocks[0]
            elif b > 0:
                update_pointer_value = 1
                update_blocks[0] = b
    return update_row, update_blocks, update_pointer_value


def add_to_start(solutions, add_num):
    """The current function gets a list of lists and number. The function
    will add all sub-lists into an updated list with each sub-list added
    at the beginning of the list the number the function is gets"""
    final_list = []
    if solutions is None:
        return None
    for solution in solutions:
        final_list.append([add_num] + solution)
    return final_list


def recursive_solution(row, blocks, first_slot_pointer):
    """The current function receives a list (single row in the matrix), a
    constraint list, and another variable that will be used for its recursive
    readings. The function returns a list of lists with all options for coloring
    the line. In each call the function calls for a helper function which
    updates the parameters it receives and also calls for another helper
    function which handles the final list that we want to return, all according
    to what the first_slot is worth. The function will detect an invalid
    sequence and eliminate it immediately by returning the None value"""
    # the base case
    if len(row) == 0:
        if len(blocks) == 0:
            return [[]]
        else:
            return None
    # steps into the base case: first_slot_pointer can be 1 or 0 or -1
    if first_slot_pointer == 1:
        # first_slot_pointer == 1 we will enter to the first slot- the 1 value
        if row[0] == WHITE:
            return None
        update_r, update_b, update_f = update_par_helper(row, blocks, 1)
        solutions = recursive_solution(update_r, update_b, update_f)
        return add_to_start(solutions, BLACK)

    elif first_slot_pointer == 0:
        # first_slot_pointer == 0 we will enter to the first slot- the 1 value
        # or 0 value, it's depend on what is the first slot is.
        ones_update_solutions = []
        if row[0] != WHITE and len(blocks) > 0:
            update_r, update_b, update_f = update_par_helper(row, blocks, 1)
            ones_solutions = recursive_solution(update_r, update_b, update_f)
            ones_update_solutions = add_to_start(ones_solutions, BLACK)

        zeros_update_solutions = []
        if row[0] != BLACK:
            update_r, update_b, update_f = update_par_helper(row, blocks, 0)
            zeros_solutions = recursive_solution(update_r, update_b, update_f)
            zeros_update_solutions = add_to_start(zeros_solutions, WHITE)

        # in the end we will takes all the options of 1,0 if they are relevant.
        return (ones_update_solutions if ones_update_solutions is not None else
                []) + (zeros_update_solutions if zeros_update_solutions is not
                                                        None else [])

    elif first_slot_pointer == -1:
        # first_slot_pointer == -1 we will enter to the first slot- the 0 value
        if row[0] == BLACK:
            return None
        update_r, update_b, update_f = update_par_helper(row, blocks, 0)
        solutions_for_minus = recursive_solution(update_r, update_b, update_f)
        return add_to_start(solutions_for_minus, WHITE)


def get_row_variations(row, blocks):
    """The function accepts a list (signal matrix row) and a constraints list
    and returns a list of lists of all options to paint the same
    row according to constraints by calling to recursive_solution function"""
    list_of_variations = recursive_solution(row, blocks, 0)
    if list_of_variations == [[]]:
        return [[]]
    return list_of_variations


def get_intersection_row(rows):
    """The current function accepts a list of lists (all rows of the matrix)
    and returns the cutting of the rows - a list of all common organs
    located in the same places in all rows in some values in each"""
    intersection_list = []
    if rows:
        for i in range(len(rows[0])):
            temp_list = []
            for row in rows:
                temp_list.append(row[i])
            if sum(temp_list) == len(rows):
                intersection_list.append(BLACK)
            elif sum(temp_list) == 0 and UNKNOWN not in temp_list:
                intersection_list.append(WHITE)
            else:
                intersection_list.append(UNKNOWN)
        return intersection_list
    return []


def conclude_from_constraints_helper(board, constraints):
    """The current function receives a board and a list of constraints. The
    function updates the palette it receives by going over each line's color
    options and overlapping them. The function returns a boolean value."""
    bool_value = False
    for i in range(len(board)):
        row_variations = get_row_variations(board[i], constraints[0][i])
        variations_intersection = get_intersection_row(row_variations)
        if board[i] != variations_intersection:
            board[i] = variations_intersection
            bool_value = True
    return bool_value


def conclude_from_constraints(board, constraints):
    """The current function receives a board and a list of constraints.
    The function updates the board it receives by calling the
    conclude_from_constraints_helper function and returns the value None"""
    conclude_from_constraints_helper(board, constraints)


def create_board(constraints):
    """The current function accepts the list of constraints of the matrix. The
    function creates a board of -1 on size n * m when n is the length constraint
    of the rows and m is the column constraint length"""
    board = []
    for i in range(len(constraints[0])):
        temp_board = []
        for j in range(len(constraints[1])):
            temp_board.append(UNKNOWN)
        board.append(temp_board)
    return board


def solve_easy_nonogram(constraints):
    """The current function accepts the list of constraints of the matrix. The
    function returns a complete solution to a nonogram game by using previous
    functions and by combining the rows and columns in the backtracing process.
    if the function will not find complete solution she will return the last one"""
    board = create_board(constraints)
    bool_value = True
    while bool_value:
        row_bool = conclude_from_constraints_helper(board, constraints)
        board = list(map(list, list(zip(*board))))
        col_bool = conclude_from_constraints_helper(board, constraints[::-1])
        board = list(map(list, list(zip(*board))))
        if not row_bool and not col_bool:
            bool_value = False
    return board
# new


def solve_nonogram(constraints):
    """this function is solving all kinds of boards of the game and returning 
    the all possible solutions for it"""  # BTM
    return [solve_easy_nonogram(constraints)]


def comb_func(n, k):
    """ the current function gets the n integer representing number of positions
    to choose fromand and the k integer that representing number of free zeros
    and it returns integer representing number of different combinations of
    choosing unordered subsets of k elements from a fixed set of n elements """
    return math.factorial(n)//(math.factorial(k)*math.factorial(n-k))


def count_row_variations(length, blocks):
    """ Gets length and blocks and returns how many possible colourings of it
    there are integer representing number of possible colourings for the row """
    num_of_zeros = length-sum(blocks)-(len(blocks)-1)
    free_places = len(blocks) + num_of_zeros
    if free_places < num_of_zeros or free_places < 0 or num_of_zeros < 0:
        return 0
    return comb_func(free_places, num_of_zeros)


def count_row_variations2(length, blocks, row):
    """the current function is calculating all the possible coloring of a row
    that already colored in some parts"""
    return len(get_row_variations(row, blocks))  # BTM