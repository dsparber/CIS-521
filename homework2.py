############################################################
# CIS 521: Homework 2
############################################################

student_name = "Daniel Sparber"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from math import *
from random import random


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
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def __str__(self):
        return "\n".join(["".join(["T" if v else "F" for v in self.board[row]]) for row in range(self.rows)])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, value):
        return str(self) == str(value)

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        if row + 1 < self.rows:
            self.board[row + 1][col] = not self.board[row + 1][col]
        if row - 1 >= 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if col + 1 < self.cols:
            self.board[row][col + 1] = not self.board[row][col + 1]
        if col - 1 >= 0:
            self.board[row][col - 1] = not self.board[row][col - 1]

    def scramble(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col]:
                    return False
        return True

    def copy(self):
        p = create_puzzle(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                p.board[row][col] = self.board[row][col]
        return p

    def successors(self):
        for row in range(self.rows):
            for col in range(self.cols): 
                sucessor = self.copy()
                sucessor.perform_move(row, col)
                yield (row, col), sucessor

    def find_solution(self):
        queue = [self]
        moves = dict()
        moves[self] = []


        while queue:
            current = queue.pop()

            if current.is_solved():
                return moves[current]

            for move, neighbor in current.successors():
                if neighbor not in moves:
                    moves[neighbor] = moves[current] + [move]
                    queue.insert(0, neighbor)

def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for _ in range(cols)] for _ in range(rows)])

p = create_puzzle(2, 2)
for move, new_p in p.successors():
    print(move, new_p.get_board())

for i in range(2, 6):
    p = create_puzzle(i, i)
    print(len(list(p.successors())))

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