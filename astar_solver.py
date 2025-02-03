from heapq import heappush, heappop
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cell import Cell
    from maze import Maze

def solve_a_star(maze: 'Maze') -> bool:
    def distance_to_end(node: 'Cell') -> int:
        return abs(node.col_ind - maze.end.col_ind) + abs(node.row_ind - maze.end.row_ind)
    
    pq: list[tuple[int, int, Cell]] = [] # (f_score, dist_to_end, cell) - handles tie-breaking based on f-scores
    heappush(pq, (0, 0, maze.start)) 
    parents: dict[Cell, Cell] = {maze.start: None}
    distances = {maze.start: 0}
    while pq:
        _, _, cell = heappop(pq)
        if cell.visited:
            continue
        cell.visited = True
        if cell in parents and parents[cell]:
            maze.animate()
            parents[cell].draw_move(cell, undo=True)
        if cell is maze.end:
            path: list[Cell] = []
            cur = cell
            while cur:
                path.append(cur)
                cur = parents[cur]
            path.reverse()
            for i in range(1, len(path)):
                maze.animate()
                path[i - 1].draw_move(path[i])
            return True
        neighbors = [n for n in maze.get_neighbors(cell) if not n.visited]
        for neighbor in neighbors:
            cur_dist = distances[cell] + 1
            end_dist = distance_to_end(neighbor)
            f_score = cur_dist + end_dist
            if neighbor not in distances or cur_dist < distances[neighbor]:
                distances[neighbor] = cur_dist
                parents[neighbor] = cell
                heappush(pq, (f_score, end_dist, neighbor))
    return False
