############################################################
# CIS 521: Homework 3
############################################################

student_name = "Daniel Sparber"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import heapq
from math import sqrt, ceil


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = []
    for row in range(rows):
        board.append([])
        for col in range(cols):
            value = 0 if (row == rows - 1 and col == cols - 1) else (1 + row * cols + col)
            board[row].append(value)

    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.rows = len(board)
        self.cols = len(board[0])
        self.board = board

    def get_board(self):
        return self.board

    def as_tuple(self):
        return tuple([tuple(row) for row in self.board])

    def get_position(self, value):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == value:
                    return row, col

    def perform_move(self, direction):
        row, col = self.get_position(0)
        if direction == "up" and row > 0:
            self.board[row][col] = self.board[row - 1][col]
            self.board[row - 1][col] = 0
            return True, self
        if direction == "down" and row < self.rows - 1:
            self.board[row][col] = self.board[row + 1][col]
            self.board[row + 1][col] = 0
            return True, self
        if direction == "left" and col > 0:
            self.board[row][col] = self.board[row][col - 1]
            self.board[row][col - 1] = 0
            return True, self
        if direction == "right" and col < self.cols - 1:
            self.board[row][col] = self.board[row][col + 1]
            self.board[row][col + 1] = 0
            return True, self

        return False, self

    def scramble(self, num_moves):
        num_moved = 0
        while num_moved < num_moves:
            success, _  = self.perform_move(random.choices(["up", "down", "left", "right"]))
            if success:
                num_moved += 1

    def correct_value(self, row, col):
        if row == self.rows - 1 and col == self.cols - 1:
            return 0
        return (1 + row * self.cols + col)


    def is_solved(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != self.correct_value(row, col):
                    return False
        return True

    def copy(self):
        board = []
        for row in range(self.rows):
            board.append([])
            for col in range(self.cols):
                board[row].append(self.board[row][col])
        return TilePuzzle(board)

    def successors(self):
        result = []
        for direction in  ["up", "down", "left", "right"]:
            valid, copy = self.copy().perform_move(direction)
            if valid:
                result.append((direction, copy))

        return result

    def __lt__(self, value):
        return False

    def __gt__(self, value):
        return False

    def iddfs_helper(self, limit, moves):

        if self.is_solved():
            yield moves

        if limit > 0:
            for move, copy in self.successors():
                for result in copy.iddfs_helper(limit - 1, moves + [move]):
                    yield result
        
    # Required
    def find_solutions_iddfs(self):
        limit = 1
        while True:
            any_solution = False
            for solution in self.iddfs_helper(limit, []):
                any_solution = True
                yield solution
            
            if any_solution:
                break
            else:
                limit += 1

    # Required
    def find_solution_a_star(self):

        def h(node):
            distance = 0
            for row in range(node.rows):
                for col in range(node.cols):
                    value = node.correct_value(row, col)
                    current_row, current_col = node.get_position(value)
                    distance += abs(row - current_row) + abs(col - current_col)
            
            return distance

        queue = [(h(self), self)]

        distance = dict()
        distance[self.as_tuple()] = h(self)

        g = dict()
        g[self.as_tuple()] = 0

        path = dict()
        path[self.as_tuple()] = []

        while queue:
            _, node = heapq.heappop(queue)

            if node.is_solved():
                return path[node.as_tuple()]
            
            for move, neighbor in node.successors():
                g[neighbor.as_tuple()] = g[node.as_tuple()] + 1
                f = g[neighbor.as_tuple()] + h(neighbor)

                visited = neighbor.as_tuple() in distance

                if not visited or f < distance[neighbor.as_tuple()]:
                    heapq.heappush(queue, (f, neighbor))
                    distance[neighbor.as_tuple()] = f
                    path[neighbor.as_tuple()] = path[node.as_tuple()] + [move]




############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):

    rows = len(scene)
    cols = len(scene[0])

    def get_neighbors(node):
        row = node[0]
        col = node[1]
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x = row + dx
                y = col + dy
                if 0 <= x < rows and 0 <= y < cols:
                    if not scene[x][y]:
                        neighbors.append((x, y))

        return neighbors

    def cost(p1, p2):
        return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def h(node):
        return cost(node, goal)

    queue = [(h(start), start)]

    f = dict()
    f[start] = h(start)

    g = dict()
    g[start] = 0

    path = dict()
    path[start] = [start]

    while queue:
        _, node = heapq.heappop(queue)

        if node == goal:
            return path[node]
        
        for neighbor in get_neighbors(node):
            g_neighbor = g[node] + cost(node, neighbor)
            f_neighbor = g_neighbor+ h(neighbor)

            visited = neighbor in f

            if not visited or f_neighbor < f[neighbor]:
                heapq.heappush(queue, (f_neighbor, neighbor))
                f[neighbor] = f_neighbor
                g[neighbor] = g_neighbor
                path[neighbor] = path[node] + [neighbor]



############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def solve_distinct_disks(length, n):
    start = tuple(list(range(n)) + [-1] * (length - n))
    goal = start[::-1]

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

    def h(node):
        sum = 0
        for x in range(n):
            diff =  ceil(abs(node.index(x) - goal.index(x)) / 2)
            sum += diff
        return sum

    queue = [(h(start), start)]

    distance = dict()
    distance[start] = h(start)

    g = dict()
    g[start] = 0

    path = dict()
    path[start] = []

    while queue:
        _, node = heapq.heappop(queue)

        if node == goal:
            return path[node]
        
        for move, neighbor in get_neighbors(node):
            g[neighbor] = g[node] + 1
            f = g[neighbor] + h(neighbor)

            visited = neighbor in distance

            if not visited or f < distance[neighbor]:
                heapq.heappush(queue, (f, neighbor))
                distance[neighbor] = f
                path[neighbor] = path[node] + [move]


############################################################
# Section 4: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 4.5

feedback_question_2 = """
Finding out how priority queues work in python was the most challenging part
"""

feedback_question_3 = """
I liked everything.
"""
