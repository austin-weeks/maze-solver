from cell import Cell
from shapes import *
from window import Window
import time, random

from dfs_solver import solve_dfs
from bfs_solver import solve_bfs
from dijkstra_solver import solve_dijkstra
from astar_solver import solve_a_star

ANIMATION_DELAY = 0.005
ANIMATION_FREQ = 50 # draw only ever x steps

class Maze():
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window | None = None,
        seed: int | None = None,
        maze_creation_animation_time: int = ANIMATION_DELAY,
        maze_solving_animation_time: int = ANIMATION_DELAY * 2
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self._generate_anim_delay = maze_creation_animation_time
        self._solve_anim_delay = maze_solving_animation_time
        self._anim_step = 0
        self.cells: list[list[Cell]] = []
        self.start: Cell = None
        self.end: Cell = None

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls()
        self._reset_cells_visited()

    def _create_cells(self):
        cells = []
        for c in range(self.num_cols):
            x = self.x1 + (self.cell_size_x * c)
            col = []
            for r in range(self.num_rows):
                y = self.y1 + (self.cell_size_y * r)
                cell = Cell(
                    x1=x,
                    x2=x + self.cell_size_x,
                    y1=y,
                    y2=y + self.cell_size_y,
                    col_ind=c,
                    row_ind=r,
                    window=self.window,
                    color=None
                )
                self._draw_cell(cell)
                col.append(cell)
            cells.append(col)
        self.cells = cells

    def _draw_cell(self, cell: Cell):
        if not self.window:
            return
        cell.draw()
        self.animate(generating=True)

    def animate(self, generating: bool = False):
        freq = ANIMATION_FREQ if generating else ANIMATION_FREQ // 3
        if self._anim_step < freq:
            self._anim_step += 1
            return
        else:
            self._anim_step = 0
        if not self.window:
            return
        self.window.redraw()
        delay = self._generate_anim_delay if generating else self._solve_anim_delay
        if delay > 0:
            time.sleep(delay)

    def _break_entrance_and_exit(self):
        entrance = self.cells[0][0]
        self.start = entrance
        entrance.top_wall = False
        self._draw_cell(entrance)

        exit_cell = self.cells[-1][-1]
        self.end = exit_cell
        exit_cell.bottom_wall = False
        self._draw_cell(exit_cell)
    
    def _break_walls(self):
        stack = [self.start]
        while stack:
            cell = stack.pop()
            cell.visited = True
            c, r = cell.col_ind, cell.row_ind
            neighbors: list[tuple[Cell, str]] = []
            if self._in_bounds(c, r - 1):
                neighbors.append((self.cells[c][r - 1], "up"))
            if self._in_bounds(c, r + 1):
                neighbors.append((self.cells[c][r + 1], "down"))
            if self._in_bounds(c - 1, r):
                neighbors.append((self.cells[c - 1][r], "left"))
            if self._in_bounds(c + 1, r):
                neighbors.append((self.cells[c + 1][r], "right"))
            neighbors = [n for n in neighbors if not n[0].visited]

            if not neighbors: # reached a dead end
                self._draw_cell(cell)
                continue
            next_cell, direction = neighbors.pop(random.randint(0, len(neighbors) - 1))
            if direction == "up":
                cell.top_wall = False
                next_cell.bottom_wall = False
            elif direction == "down":
                cell.bottom_wall = False
                next_cell.top_wall = False
            elif direction == "left":
                cell.left_wall = False
                next_cell.right_wall = False
            elif direction == "right":
                cell.right_wall = False
                next_cell.left_wall = False
            self._draw_cell(cell)
            stack.append(cell)
            stack.append(next_cell)

    def _reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def solve(self, method: str = "dfs") -> bool:
        """
        Solve the maze with the given method.\n
        Options:\n
        "dfs" - depth-first search (default)\n
        "bfs" - breadth-first search\n
        "a*" - A* pathfinding\n
        """
        match method:
            case "dfs": return solve_dfs(self, self.cells[0][0])
            case "bfs": return solve_bfs(self)
            case "dijkstra": return solve_dijkstra(self)
            case "a*": return solve_a_star(self)
        raise ValueError(f"Maze lacks a '{method}' solver. Please use 'dfs', 'bfs', 'dijkstra' or 'a*'.")
        
    def _in_bounds(self, c, r):
        if c < 0 or r < 0:
            return False
        if c >= len(self.cells) or r >= len(self.cells[0]):
            return False
        return True
        
    def get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        # we do bottom and right first, as the maze goes from top left to bottom right
        c, r = cell.col_ind, cell.row_ind
        if not cell.bottom_wall and self._in_bounds(c, r + 1):
            neighbors.append(self.cells[c][r + 1])
        if not cell.right_wall and self._in_bounds(c + 1, r):
            neighbors.append(self.cells[c + 1][r])
        if not cell.top_wall and self._in_bounds(c, r - 1):
            neighbors.append(self.cells[c][r - 1])
        if not cell.left_wall and self._in_bounds(c - 1, r):
            neighbors.append(self.cells[c - 1][r])
        return neighbors
