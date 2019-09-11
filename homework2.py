############################################################
# CIS 521: Homework 2
############################################################

student_name = "Daniel Sparber"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from math import *


############################################################
# Section 0: Additional helper functions by Daniel
############################################################

def search(search_type, inital_state, get_neighbors, is_goal):
    
    if search_type not in ["dfs", "bfs"]:
        raise "Invalid search type: " + search_type 
    
    stack = [inital_state]
    visited = []

    dfs = search_type == "dfs"

    while stack:
        current = stack.pop()
        visited.append(current)

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                if dfs:
                    stack.append(neighbor)
                else:
                    stack.insert(0, neighbor)

        if is_goal(current):
            yield current

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    # n^2 choose n
    return factorial(n ** 2) // (factorial(n) * factorial(n ** 2 - n))

def num_placements_one_per_row(n):
    return n ** n

def n_queens_valid(board):
    n = len(board)
    no_same_column = len(set(board)) == n  # Every number is present exactly once
    no_same_diag_1 = len({(value - row) for row, value in enumerate(board)}) == n
    no_same_diag_2 = len({(value + row) for row, value in enumerate(board)}) == n
    return no_same_column and no_same_diag_1 and no_same_diag_2

def n_queens_helper(n, board):
    possible = [board + [i] for i in range(n)]
    return [board for board in possible if n_queens_valid(board)]

def n_queens_solutions(n):
    return search(
        search_type="dfs",
        inital_state=[],
        get_neighbors=lambda board: n_queens_helper(n, board),
        is_goal=lambda board: len(board) == n and n_queens_valid(board)
    )

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        pass

    def get_board(self):
        pass

    def perform_move(self, row, col):
        pass

    def scramble(self):
        pass

    def is_solved(self):
        pass

    def copy(self):
        pass

    def successors(self):
        pass

    def find_solution(self):
        pass

def create_puzzle(rows, cols):
    pass

############################################################
# Section 3: Linear Disk Movement
############################################################

def solve_identical_disks(length, n):
    pass

def solve_distinct_disks(length, n):
    pass

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""