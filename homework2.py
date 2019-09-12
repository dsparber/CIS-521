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
    possible = [list(board) + [i] for i in range(n)]
    return [tuple(board) for board in possible if n_queens_valid(board)]

def n_queens_solutions(n):
    stack = [tuple()]
    visited = set()

    while stack:
        current = stack.pop()

        if len(current) == n:
            if n_queens_valid(current):
                yield list(current)
        else:
            for neighbor in n_queens_helper(n, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

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


############################################################
# Section 3: Linear Disk Movement
############################################################

def solve_disks(length, num_disks, distinct):
    
    initial = tuple([(x if distinct else 1) if x < num_disks else -1 for x in range(length)])
    goal = initial[::-1]

    def get_neighbors(cells):
        neighbors = []
        for index, cell in enumerate(cells):
            if cell >= 0:
                # move right
                if index + 1 < length and cells[index + 1] == -1:
                    copy = list(cells)
                    copy[index] = -1
                    copy[index + 1] = cell
                    neighbors.append(((index, index + 1), tuple(copy)))
                # move left
                if index >= 1 and cells[index - 1] == -1:
                    copy = list(cells)
                    copy[index] = -1
                    copy[index - 1] = cell
                    neighbors.append(((index, index - 1), tuple(copy)))
                # jump right
                if index + 2 < length and cells[index + 1] != -1 and cells[index + 2] == -1:
                    copy = list(cells)
                    copy[index] = -1
                    copy[index + 2] = cell
                    neighbors.append(((index, index + 2), tuple(copy)))
                # jump left
                if index >= 2 and cells[index - 1] != -1 and cells[index - 2] == -1:
                    copy = list(cells)
                    copy[index] = -1
                    copy[index - 2] = cell
                    neighbors.append(((index, index - 2), tuple(copy)))

        return neighbors

    queue = [initial]
    moves = dict()
    moves[initial] = []

    while queue:
        current = queue.pop()

        if current == goal:
            return moves[current]

        for move, neighbor in get_neighbors(current):
            if neighbor not in moves:
                moves[neighbor] = moves[current] + [move]
                queue.insert(0, neighbor)


def solve_identical_disks(length, n):
    return solve_disks(length, n, False)

def solve_distinct_disks(length, n):
    return solve_disks(length, n, True)


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
3h
"""

feedback_question_2 = """
The assignment was not challenging, there were no stumbling blocks
"""

feedback_question_3 = """
I liked everything. The assignment was great fun!
"""