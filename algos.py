#!/usr/bin/env python3

from dataclasses import dataclass
from collections import deque


@dataclass
class AlgoResults:
    path : list
    visited_in_order : list


def bfs(grid, start, destination):
    path_found = []                                                                           
    visited_in_order = []

    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
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
                    visited_in_order.append((nx, ny))
                    parent[nx][ny] = (x, y)
                    queue.append((nx, ny))
                    # Check to early exit, if so reconstruct path
                    if ((nx, ny) == destination):
                        while (nx, ny) != start:
                            path_found.append((nx, ny))
                            nx, ny = parent[nx][ny]
                        path_found.append(start)
                        
                        return AlgoResults(path_found, visited_in_order)

    return None # No path found