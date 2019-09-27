############################################################
# CIS 521: Homework 4
############################################################

student_name = "Daniel Sparber"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.



############################################################
# Section 1: Sudoku Solver
############################################################

def sudoku_cells():
    return [(row, col) for row in range(9) for col in range(9)]

def sudoku_row_arcs():
    return [((row, a), (row, b)) for row in range(9) for a in range(9) for b in range(9) if a != b]

def sudoku_col_arcs():
    return [((a, col), (b, col)) for a in range(9) for b in range(9) for col in range(9) if a != b]

def sudoku_box_arcs():
    arcs = []
    for startRow in [0, 3, 6]:
        for startCol in [0, 3, 6]:
            arcs += [((startRow + dR1, startCol + dC1), (startRow + dR2, startCol + dC2)) 
                        for dR1 in range(3) for dR2 in range(3) for dC1 in range(3) for dC2 in range(3) 
                        if dR1 != dR2 or dC1 != dC2]
    return arcs

def sudoku_arcs():
    return sudoku_row_arcs() + sudoku_col_arcs() + sudoku_box_arcs()


def read_board(path):
    board = dict()

    with open(path, "r") as file:
        for row in range(9):
            line = file.readline()
            for col in range(9):
                char = line[col]

                if char == "*":
                    board[(row, col)] = set(range(1,10))
                else:
                    number = int(char)
                    board[(row, col)] = {number}
    
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ROW_ARCS = sudoku_row_arcs()
    COL_ARCS = sudoku_col_arcs()
    BOX_ARCS = sudoku_box_arcs()
    ARCS = ROW_ARCS + COL_ARCS + BOX_ARCS

    def __init__(self, board):
        self.board = dict(board)

    def __str__(self):
        string = ""
        for row in range(9):
            for col in range(9):
                if len(self.get_values((row, col))) == 0:
                    string += "-"
                elif len(self.get_values((row, col))) == 1:
                    string += str(list(self.get_values((row, col)))[0])
                else:
                    string += "_"
            string += "\n"

        return string

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        # No restriction
        if (cell1, cell2) not in self.ARCS:
            return False
        
        # Multiple possible values
        if len(self.board[cell2]) > 1:
            return False

        # No same values
        if len(self.board[cell1].intersection(self.board[cell2])) == 0:
            return False

        # Regular case
        self.board[cell1] = self.board[cell1] - self.board[cell2]
        return True

    def value_impossible(self, value, neighbors):
        return all([value not in self.get_values(y) for y in neighbors]) 

    def solved(self):
        return all([len(self.get_values(cell)) == 1 for cell in self.CELLS])

    def unsolveable(self):
        return any([len(self.get_values(cell)) == 0 for cell in self.CELLS])

    def remove_based_on_neighbors(self, cell1):
        if len(self.get_values(cell1)) == 1:
            return False

        for value in self.get_values(cell1):
            if self.value_impossible(value, self.neighbors(cell1, arcs=self.ROW_ARCS)) or \
             self.value_impossible(value, self.neighbors(cell1, arcs=self.COL_ARCS)) or \
             self.value_impossible(value, self.neighbors(cell1, arcs=self.BOX_ARCS)):

                self.board[cell1] = {value}
                return True
        
        return False

    def neighbors(self, cell, arcs=None):
        return {y for (x, y) in (arcs or self.ARCS) if x == cell}

    def infer_ac3(self):
        queue = self.ARCS[:]
        while queue:
            x_i, x_j = queue.pop(0)
            if self.remove_inconsistent_values(x_i, x_j):
                for x_k in (self.neighbors(x_i) - {x_j}):
                    queue.append((x_k, x_i))


    def infer_improved(self):
        self.infer_ac3()

        changed = False
        for cell in self.CELLS:
            if self.remove_based_on_neighbors(cell):
                changed = True

        if changed:
            self.infer_improved()

    def get_first_undecided(self):
        for cell in self.CELLS:
            if len(self.get_values(cell)) > 1:
                return cell

    def infer_with_guessing(self):
        self.infer_improved()

        if self.solved():
            return


        # Tree search with deterministic guessing
        stack = []
        cell = self.get_first_undecided()
        for value in self.get_values(cell):
            stack.append((cell, value, self.board))
        
        while stack:
            cell, value, board = stack.pop()

            self.board = dict(board)
            self.board[cell] = {value}

            self.infer_improved()

            if self.solved():
                return

            if not self.unsolveable():
                cell = self.get_first_undecided()
                for value in self.get_values(cell):
                    stack.append((cell, value, self.board))



############################################################
# Section 2: Dominoes Games
############################################################

def create_dominoes_game(rows, cols):
    pass

class DominoesGame(object):

    # Required
    def __init__(self, board):
        pass

    def get_board(self):
        pass

    def reset(self):
        pass

    def is_legal_move(self, row, col, vertical):
        pass

    def legal_moves(self, vertical):
        pass

    def perform_move(self, row, col, vertical):
        pass

    def game_over(self, vertical):
        pass

    def copy(self):
        pass

    def successors(self, vertical):
        pass

    def get_random_move(self, vertical):
        pass

    # Required
    def get_best_move(self, vertical, limit):
        pass
        
############################################################
# Section 3: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 3

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
