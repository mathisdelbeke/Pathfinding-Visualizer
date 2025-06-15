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


# are both visited_in_order fair to compare???