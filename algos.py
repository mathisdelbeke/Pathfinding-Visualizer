#!/usr/bin/env python3

from dataclasses import dataclass
from collections import deque
import heapq


@dataclass
class AlgoResults:
    path : list
    visited_in_order : list


def bfs(grid, start, destination):
    path_found = []                                                                           
    visited_in_order = []

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
                    visited_in_order.append((nx, ny))
                    parent[nx][ny] = (x, y)
                    queue.append((nx, ny))
                    # Check to early exit, if so reconstruct path
                    if ((nx, ny) == destination):
                        while (nx, ny) != start:
                            path_found.append((nx, ny))
                            nx, ny = parent[nx][ny]
                        path_found.append(start)
                        return AlgoResults(path_found[::-1], visited_in_order)

    return None # No path found


def dijkstra(grid, start, destination):
    path_found = []

    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    sr, sc = start
    gr, gc = destination

    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[sr][sc] = 0

    came_from = {}  # For path reconstruction: (row, col) -> (prev_row, prev_col)

    heap = [(0, sr, sc)]

    while heap:
        current_dist, r, c = heapq.heappop(heap)

        if (r, c) == (gr, gc):
            # Reconstruct path
            while (r, c) != start:
                path_found.append((r, c))
                r, c = came_from[(r, c)]
            path_found.append(start)
            return AlgoResults(path_found[::-1], [None])

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                new_dist = current_dist + 1
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    came_from[(nr, nc)] = (r, c)
                    heapq.heappush(heap, (new_dist, nr, nc))

    return None  # No path found
