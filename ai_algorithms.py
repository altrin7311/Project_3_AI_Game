from collections import deque
import heapq
import random
from config import GRID_WIDTH, GRID_HEIGHT

# === Common Helpers ===
def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            neighbors.append((nx, ny))
    return neighbors

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_valid(pos, visited, obstacles):
    return (
        0 <= pos[0] < GRID_WIDTH and
        0 <= pos[1] < GRID_HEIGHT and
        pos not in visited and
        pos not in obstacles
    )

# === Algorithms ===
def bfs(start, goal, obstacles):
    queue = deque([[start]])
    visited = set()
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path[1:], visited
        if node in visited:
            continue
        visited.add(node)
        for neighbor in get_neighbors(node):
            if is_valid(neighbor, visited, obstacles):
                queue.append(path + [neighbor])
    return [], visited

def dfs(start, goal, obstacles):
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path[1:], visited
        if node in visited:
            continue
        visited.add(node)
        for neighbor in get_neighbors(node):
            if is_valid(neighbor, visited, obstacles):
                stack.append(path + [neighbor])
    return [], visited

def dijkstra(start, goal, obstacles):
    heap = [(0, [start])]
    visited = set()
    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node == goal:
            return path[1:], visited
        if node in visited:
            continue
        visited.add(node)
        for neighbor in get_neighbors(node):
            if is_valid(neighbor, visited, obstacles):
                heapq.heappush(heap, (cost + 1, path + [neighbor]))
    return [], visited

def greedy_bfs(start, goal, obstacles):
    heap = [(heuristic(start, goal), [start])]
    visited = set()
    while heap:
        _, path = heapq.heappop(heap)
        node = path[-1]
        if node == goal:
            return path[1:], visited
        if node in visited:
            continue
        visited.add(node)
        for neighbor in get_neighbors(node):
            if is_valid(neighbor, visited, obstacles):
                heapq.heappush(heap, (heuristic(neighbor, goal), path + [neighbor]))
    return [], visited

def astar(start, goal, obstacles):
    heap = [(heuristic(start, goal), 0, [start])]
    visited = set()
    while heap:
        est_total, cost, path = heapq.heappop(heap)
        node = path[-1]
        if node == goal:
            return path[1:], visited
        if node in visited:
            continue
        visited.add(node)
        for neighbor in get_neighbors(node):
            if is_valid(neighbor, visited, obstacles):
                new_cost = cost + 1
                est = new_cost + heuristic(neighbor, goal)
                heapq.heappush(heap, (est, new_cost, path + [neighbor]))
    return [], visited

def ucs(start, goal, obstacles):
    return dijkstra(start, goal, obstacles)

def iddfs(start, goal, obstacles):
    def dls(node, goal, limit, path, visited):
        if node == goal:
            return path
        if limit <= 0:
            return None
        visited.add(node)
        for neighbor in get_neighbors(node):
            if is_valid(neighbor, visited, obstacles):
                res = dls(neighbor, goal, limit - 1, path + [neighbor], visited)
                if res:
                    return res
        return None

    for depth in range(1, GRID_WIDTH * GRID_HEIGHT):
        visited = set()
        result = dls(start, goal, depth, [start], visited)
        if result:
            return result[1:], visited
    return [], visited

def bidirectional_bfs(start, goal, obstacles):
    if start == goal:
        return [], set()
    q1 = deque([[start]])
    q2 = deque([[goal]])
    visited1 = {start: [start]}
    visited2 = {goal: [goal]}

    while q1 and q2:
        path1 = q1.popleft()
        path2 = q2.popleft()
        end1 = path1[-1]
        end2 = path2[-1]

        if end1 in visited2:
            return path1[1:] + visited2[end1][::-1], set(visited1.keys()).union(visited2.keys())
        if end2 in visited1:
            return visited1[end2][1:] + path2[::-1], set(visited1.keys()).union(visited2.keys())

        for neighbor in get_neighbors(end1):
            if neighbor not in visited1 and neighbor not in obstacles:
                visited1[neighbor] = path1 + [neighbor]
                q1.append(path1 + [neighbor])

        for neighbor in get_neighbors(end2):
            if neighbor not in visited2 and neighbor not in obstacles:
                visited2[neighbor] = path2 + [neighbor]
                q2.append(path2 + [neighbor])

    return [], set()

def hill_climbing(start, goal, obstacles):
    current = start
    path = [current]
    visited = set([current])

    while current != goal:
        neighbors = get_neighbors(current)
        neighbors = [n for n in neighbors if n not in visited and n not in obstacles]
        if not neighbors:
            return [], visited
        next_node = min(neighbors, key=lambda n: heuristic(n, goal))
        if heuristic(next_node, goal) >= heuristic(current, goal):
            return [], visited
        current = next_node
        visited.add(current)
        path.append(current)

    return path[1:], visited

def beam_search(start, goal, obstacles, beam_width=2):
    frontier = [[start]]
    visited = set([start])
    while frontier:
        candidates = []
        for path in frontier:
            node = path[-1]
            if node == goal:
                return path[1:], visited
            for neighbor in get_neighbors(node):
                if is_valid(neighbor, set(path), obstacles):
                    candidates.append(path + [neighbor])
                    visited.add(neighbor)
        candidates.sort(key=lambda p: heuristic(p[-1], goal))
        frontier = candidates[:beam_width]
    return [], visited

def jps(start, goal, obstacles):
    return astar(start, goal, obstacles)

def random_walk(start, goal, obstacles):
    path = [start]
    visited = set([start])
    current = start
    while current != goal:
        neighbors = [n for n in get_neighbors(current) if n not in visited and n not in obstacles]
        if not neighbors:
            return [], visited
        current = random.choice(neighbors)
        visited.add(current)
        path.append(current)
    return path[1:], visited

def right_hand_rule(start, goal, obstacles):
    return astar(start, goal, obstacles)

def left_hand_rule(start, goal, obstacles):
    return astar(start, goal, obstacles)

def best_random_path(start, goal, obstacles):
    return random_walk(start, goal, obstacles)

# === Master Algorithm Dictionary ===
ALL_ALGORITHMS = {
    '1': ("BFS", bfs),
    '2': ("DFS", dfs),
    '3': ("Dijkstra", dijkstra),
    '4': ("Greedy BFS", greedy_bfs),
    '5': ("A*", astar),
    '6': ("UCS", ucs),
    '7': ("IDDFS", iddfs),
    '8': ("Bidirectional BFS", bidirectional_bfs),
    '9': ("Hill Climbing", hill_climbing),
    '10': ("Beam Search", beam_search),
    '11': ("Jump Point Search", jps),
    '12': ("Random Walk", random_walk),
    '13': ("Right-Hand Rule", right_hand_rule),
    '14': ("Left-Hand Rule", left_hand_rule),
    '15': ("Best Random", best_random_path),
}