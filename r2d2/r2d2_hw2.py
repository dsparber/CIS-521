###Include your imports###
import math
import queue
import random
import itertools
from queue import Queue, PriorityQueue
from collections import defaultdict
import os

class Graph:
    def __init__(self, V, E):
        self.vertics = V
        self.edges = E
        # Storing nodes as list and adjecancy lists within dict
        self.adjecent = {v: [] for v in V} 
        for u, v in E:
            self.adjecent[u] = self.adjecent[u] + [v]
            self.adjecent[v] = self.adjecent[v] + [u]


    def neighbors(self, u):
        return self.adjecent[u]

    def dist_between(self, u, v):
        return 1 if v in self.neighbors(u) else None

def BFS_or_DFS(G, start, goal, bfs):
    visited = set()
    prev = dict()
    prev[start] = None 

    queue = [start]

    while queue:
        cur = queue.pop()
        visited.add(cur)

        if cur == goal:
            break

        for neighbor in G.neighbors(cur):
            if neighbor not in visited:
                if bfs:
                    queue.insert(0, neighbor)
                else:
                    queue.append(neighbor)
                prev[neighbor] = cur

    path = []
    cur = goal
    while cur:
        path.insert(0, cur)
        cur = prev[cur]

    return path, list(visited)

def BFS(G, start, goal):
    return BFS_or_DFS(G, start, goal, bfs=True)

def DFS(G, start, goal):
    return BFS_or_DFS(G, start, goal, bfs=False)

def A_star(G, start, goal):

    def h(n):
        # Robot can not go diagonal -> dX + dY is valid
        dX = abs(goal[0] - n[0])
        dY = abs(goal[1] - n[0])
        return dX + dY

    visited = []

    prev = dict()
    prev[start] = None 

    g = dict()
    g[start] = 0

    f = dict()
    f[start] = g[start] + h(start)

    queue = PriorityQueue()
    queue.put((0, start))

    while not queue.empty():
        _, cur = queue.get()
        visited.append(cur)

        if cur == goal:
            break

        for neighbor in G.neighbors(cur):
            if neighbor not in visited:
                g_n = g[cur] + 1
                f_n = g_n + h(neighbor)
                if neighbor not in g or g_n < g[neighbor]: 
                    g[neighbor] = g_n
                    f[neighbor] = f_n
                    queue.put((f_n, neighbor))
                    prev[neighbor] = cur

    path = []
    cur = goal
    while cur:
        path.insert(0, cur)
        cur = prev[cur]

    return path, visited

def tsp(G, start, goals):
    optimal_order = None
    optimal_path = None

    for permutation in itertools.permutations(goals):
        order = tuple([start] + list(permutation))
        path = []
        for i in range(len(order) - 1):
            path += A_star(G, order[i], order[(i + 1) % len(order)])[0][0:-1]
        path.append(order[-1])

        if optimal_path is None or len(path) < len(optimal_path):
            optimal_path = path
            optimal_order = order


    return optimal_order, optimal_path

def path2move(path):
    moves = []
    current_direction = None
    current_count = None
    for i in range(1, len(path)):
        prev = path[i - 1]
        cur = path[i]

        dY = cur[0] - prev[0]
        dX = cur[1] - prev[1]

        if dX == 1: 
            direction = 'east'
        elif dX == -1: 
            direction = 'west'
        elif dY == 1: 
            direction = 'south'
        else: 
            direction = 'north'

        if current_direction == direction:
            current_count += 1
        else:
            if current_direction:
                moves.append((current_direction, current_count))
            current_direction, current_count = (direction, 1)

    if current_direction:
        moves.append((current_direction, current_count))
    
    return moves

def r2d2_action(movement, droid, speed, time):
    degrees = {
        'north': 90,
        'east': 0,
        'south': 270,
        'west': 180
    }

    for direction, duration in movement:
        droid.roll(speed, degrees[direction], time * duration)


##########Helper functions, Do not change##########

###generate vertics and edges to define a graph###
def generate_map(row, column, barriers):
    vertics = [(i, j) for i in range(row) for j in range(column)]
    edges = []
    for vertic in vertics:
        for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_vertic = (vertic[0] + move[0], vertic[1] + move[1])
            if next_vertic in vertics:
                edges.append((vertic, next_vertic))

    for barrier in barriers:
        edges.remove(barrier)
        edges.remove((barrier[1], barrier[0]))

    return vertics, edges

###Generate Random Map
def generate_random(row, column):
    vertics = [(i, j) for i in range(row) for j in range(column)]
    edges = []
    for vertic in vertics:
        for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_vertic = (vertic[0] + move[0], vertic[1] + move[1])
            if next_vertic in vertics:
                edges.append((vertic, next_vertic))

    num_of_barriers = round(row * 2 *column/3)
    barriers = random.sample(edges, num_of_barriers)
    for barrier in barriers:
        if barrier in edges:
            edges.remove(barrier)
        if random.random() > 0.15:

            if (barrier[1], barrier[0]) in edges:
                edges.remove((barrier[1], barrier[0]))

    return vertics, edges


###display the graph###
def printmap(G):
	rows = G.vertics[-1][0] + 1
	cols = G.vertics[-1][1] + 1
	for i in range(2 * rows - 1):
		print_row = ''
		if i % 2 == 0:
			for j in range(cols):
				current_node = (int(i / 2), j)
				right_node = (int(i / 2), j + 1)
				pattern = '☐'
				if (current_node, right_node) in G.edges and (right_node, current_node) in G.edges:
					print_row += pattern + ' ' + '  '
				else:
					if right_node in G.vertics:
						print_row += pattern + ' ' + '| '
					else:
						print_row += pattern + ' ' + '  '
		else:
			for j in range(cols):
				current_node = (math.ceil(i/2), j)
				up_node = (math.ceil(i/2) - 1, j)
				if j == 0:
					if (current_node, up_node) in G.edges and (up_node, current_node) in G.edges: 
						print_row += '  ' + ' '
					else:
						print_row += '-- '
				else: 
					if (current_node, up_node) in G.edges and (up_node, current_node) in G.edges:
						print_row += '  ' + '  '
					else:
						print_row += '--- '
		print(print_row)


###display the solution###
def printpath(G, start, goal, path):
	rows = G.vertics[-1][0] + 1
	cols = G.vertics[-1][1] + 1
	for i in range(2 * rows - 1):
		print_row = ''
		if i % 2 == 0:
			for j in range(cols):
				current_node = (int(i / 2), j)
				right_node = (int(i / 2), j + 1)
				if current_node == goal:
					pattern = '☒'
				elif current_node in path:
					pattern = '☑'
				else:
					pattern = '☐'
				if (current_node, right_node) in G.edges and (right_node, current_node) in G.edges:
					print_row += pattern + ' ' + '  '
				else:
					if right_node in G.vertics:
						print_row += pattern + ' ' + '| '
					else:
						print_row += pattern + ' ' + '  '
		else:
			for j in range(cols):
				current_node = (math.ceil(i/2), j)
				up_node = (math.ceil(i/2) - 1, j)
				if j == 0:
					if (current_node, up_node) in G.edges and (up_node, current_node) in G.edges: 
						print_row += '  ' + ' '
					else:
						print_row += '-- '
				else: 
					if (current_node, up_node) in G.edges and (up_node, current_node) in G.edges:
						print_row += '  ' + '  '
					else:
						print_row += '--- '
		print(print_row)

###########For GUI, Do not change#############
def parse_scene(scene_file):
    if not os.path.exists(scene_file):
        raise FileNotFoundError
    width = None
    height = None
    contents = []
    with open(scene_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if width is None:
                width = len(line)
            else:
                if len(line) != width:
                    raise ValueError
            tmp = []
            for char in line:
                if char == '.':
                    tmp.append(False)
                elif char == 'X':
                    tmp.append(True)
                else:
                    raise ValueError
            contents.append(tmp)

    height = len(contents)
    barriers = []
    for r in range(height):
        for c in range(width):
            if contents[r][c] is True:
                barriers.append((r, c))
    return {
        'rows': height,
        'columns': width,
        'scene': contents,
        'barriers': barriers
        }


def load_scene(scene_file):
    data = parse_scene(scene_file=scene_file)
    rows = data['rows']
    columns = data['columns']
    if rows < 2 or columns < 2:
        raise ValueError('the minimum size of a scene is 2x2')
    scene = data['scene']
    barriers = data['barriers']
    vertics, edges = generate_map_new(row=rows, column=columns, barriers=barriers)
    g = Graph(V=vertics, E=edges)
    return {
        'rows': rows,
        'columns': columns,
        'scene': scene,
        'graph': g
        }

def find_path_new(graph, method, start, goals):
    if not isinstance(graph, Graph):
        raise TypeError
    if not isinstance(start, tuple):
        raise TypeError
    if not isinstance(goals, list):
        raise TypeError
    if not goals:
        raise ValueError

    for point in goals:
        if point not in graph.vertics:
            raise ValueError

    if start not in graph.vertics:
        raise ValueError

    if method == 'dfs':
        func = DFS
    elif method == 'bfs':
        func = BFS
    elif method == 'a_star':
        func = A_star
    elif method == 'tsp':
        func = tsp
        if goals is None:
            raise ValueError
    else:
        raise NotImplementedError

    if method in ['dfs', 'bfs', 'a_star']:
        goals = goals[0]
        result = func(graph, start, goals)
        path = [result[0]]
        node_visited = result[1]
        return len(goals), path, node_visited
    else:
        # result = func(graph, start, goals)
        path = list(func(graph, start, goals))
        return len(goals), path
