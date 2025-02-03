from collections import deque
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cell import Cell
    from maze import Maze

def solve_bfs(maze: 'Maze') -> bool:
    to_visit = deque([maze.start])
    parents: dict[Cell, Cell] = {maze.start: None}
    while to_visit:
        maze.animate()
        cell = to_visit.popleft()
        if cell.visited:
            continue
        cell.visited = True
        if cell in parents and parents[cell]:
            parent = parents[cell]
            parent.draw_move(cell, undo=True)

        if cell is maze.end:
            solution: list[Cell] = []
            cur = cell
            while cur:
                solution.append(cur)
                cur = parents[cur]
            solution.reverse()
            for i in range(1, len(solution)):
                maze.animate()
                solution[i - 1].draw_move(solution[i])
            return True
        
        neighbors = [n for n in maze.get_neighbors(cell) if not n.visited]
        for neighbor in neighbors:
            parents[neighbor] = cell
            to_visit.append(neighbor)
    return False
