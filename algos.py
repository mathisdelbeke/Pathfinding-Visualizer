#!/usr/bin/env python3

from dataclasses import dataclass
from collections import deque
import heapq


@dataclass
class AlgoResults:
    path : list
    discovered_in_order : list


def bfs(grid, start, destination):
    path_found = []                                                                           
    discovered_in_order = []

    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    visited = [[False] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]
    
    queue = deque()
    queue.append(start)
    visited[start[0]][start[1]] = True

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check bounds
            if 0 <= nx < rows and 0 <= ny < cols:
                #check new and walkable
                if not visited[nx][ny] and grid[nx][ny] == 0:
                    visited[nx][ny] = True
                    discovered_in_order.append((nx, ny))
                    parent[nx][ny] = (x, y)
                    queue.append((nx, ny))
                    # Check to early exit, if so reconstruct path
                    if ((nx, ny) == destination):
                        while (nx, ny) != start:
                            path_found.append((nx, ny))
                            nx, ny = parent[nx][ny]
                        path_found.append(start)
                        return AlgoResults(path_found[::-1], discovered_in_order)

    return None # No path found


def dijkstra(grid, start, destination):
    path_found = []
    discovered_in_order = []

    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0
    parent = [[None] * cols for _ in range(rows)]

    heap = [(0, start[0], start[1])]

    while heap:
        current_dist, x, y = heapq.heappop(heap)
        if (x, y) == destination:
            # Reconstruct path
            while (x, y) != start:
                path_found.append((x, y))
                x, y = parent[x][y]
            path_found.append(start)
            return AlgoResults(path_found[::-1], discovered_in_order)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                new_dist = current_dist + 1
                if new_dist < dist[nx][ny]:
                    dist[nx][ny] = new_dist
                    parent[nx][ny] = (x, y)
                    heapq.heappush(heap, (new_dist, nx, ny))
                    discovered_in_order.append((nx, ny))

    return None  # No path found


def a_star(grid, start, destination):
    
    def heuristic(a, b):                                                    # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    path_found = []
    discovered_in_order = []

    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, destination), 0, start))  # (f, g, position)

    parent = {}
    g_score = {start: 0}

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        if current == destination:
            # Reconstruct path
            while current in parent:
                path_found.append(current)
                current = parent[current]
            path_found.append(start)
            return AlgoResults(path_found[::-1], discovered_in_order)

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue

                tentative_g = current_g + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, destination)
                    heapq.heappush(open_set, (f, tentative_g, neighbor))
                    parent[neighbor] = current
                    discovered_in_order.append(neighbor)

    return None  # No path found