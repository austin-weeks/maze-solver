from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cell import Cell
    from maze import Maze

def solve_dfs(maze: 'Maze', cell: 'Cell') -> bool:
    maze.animate()
    cell.visited = True
    if cell is maze.cells[-1][-1]:
        return True
    for neighbor in maze.get_neighbors(cell):
        if neighbor.visited:
            continue
        cell.draw_move(neighbor)
        if solve_dfs(maze, neighbor):
            return True
        else:
            cell.draw_move(neighbor, undo=True)
    return False
