from heapq import heappop, heappush
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cell import Cell
    from maze import Maze

def solve_dijkstra(maze: 'Maze') -> bool:
    pq: list[tuple[int, Cell]] = [] # (distance, cell)
    heappush(pq, (0, maze.start)) 
    parents: dict[Cell, Cell] = {maze.start: None}
    distances = {maze.start: 0}
    while pq:
        _, cell = heappop(pq) # here we need to get the min distance node
        if cell.visited:
            print('cell has already been visited')
            continue
        cell.visited = True
        if cell in parents and parents[cell]:
            maze.animate()
            parents[cell].draw_move(cell, undo=True)
        if cell is maze.end: # we found the end, let's draw the correct path
            path = []
            cur = cell
            while cur:
                path.append(cur)
                cur = parents[cur]
            path.reverse()
            for i in range(1, len(path)):
                maze.animate()
                path[i -1].draw_move(path[i])
            return True
        neighbors = [n for n in maze.get_neighbors(cell) if not n.visited]
        for neighbor in neighbors:
            new_dist = distances[cell] + 1
            if neighbor not in distances or new_dist < distances[neighbor]:
                parents[neighbor] = cell
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    return False
