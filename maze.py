from cell import Cell
from shapes import *
from window import Window
import time, random
from collections import deque

ANIMATION_DELAY = 0.005

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
        animation_step_time: int = ANIMATION_DELAY
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self._animation_delay = animation_step_time
        self._cells: list[list[Cell]] = []

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
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
        self._cells = cells

    def _draw_cell(self, cell: Cell):
        if not self.window:
            return
        cell.draw()
        self._animate()

    def _animate(self):
        if not self.window:
            return
        self.window.redraw()
        time.sleep(self._animation_delay)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.top_wall = False
        self._draw_cell(entrance)

        exit_cell = self._cells[-1][-1]
        exit_cell.bottom_wall = False
        self._draw_cell(exit_cell)

    
    def _break_walls_r(self, c: int, r: int):
        cell = self._cells[c][r]
        cell.visited = True
        while True:
            neighbors: list[tuple[int, int, str]] = []
            if self._cell_can_visit(c, r - 1):
                neighbors.append((c, r - 1, "up"))
            if self._cell_can_visit(c, r + 1):
                neighbors.append((c, r + 1, "down"))
            if self._cell_can_visit(c - 1, r):
                neighbors.append((c - 1, r, "left"))
            if self._cell_can_visit(c + 1, r):
                neighbors.append((c + 1, r, "right"))

            if not neighbors:
                self._draw_cell(cell)
                return
            next_c, next_r, direction = neighbors.pop(random.randint(0, len(neighbors) - 1))
            next_cell = self._cells[next_c][next_r]
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
            self._break_walls_r(next_c, next_r)

    def _cell_can_visit(self, c: int, r: int):
        if c < 0 or r < 0:
            return False
        if c >= len(self._cells) or r >= len(self._cells[0]):
            return False
        if self._cells[c][r].visited:
            return False
        return True

    def _reset_cells_visited(self):
        for row in self._cells:
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
            case "dfs": return self._solve_dfs(self._cells[0][0])
            case "bfs": return self._solve_bfs()
            case "a*": return self._solve_a_star()
        raise ValueError(f"Maze lacks a '{method}' solver. Please use 'dfs', 'bfs', or 'a*'.")
    
    def _solve_dfs(self, cell: Cell) -> bool:
        self._animate()
        cell.visited = True
        if cell is self._cells[-1][-1]:
            return True
        for neighbor in self._get_neighbors(cell):
            if neighbor.visited:
                continue
            cell.draw_move(neighbor)
            if self._solve_dfs(neighbor):
                return True
            else:
                cell.draw_move(neighbor, undo=True)
        return False
    
    def _solve_bfs(self) -> bool:
        to_visit = deque([self._cells[0][0]])
        parents: dict[Cell, Cell] = {}
        while to_visit:
            self._animate()
            cell = to_visit.popleft()
            if cell.visited:
                continue
            cell.visited = True
            if cell in parents:
                parent = parents[cell]
                parent.draw_move(cell, undo=True)

            if cell is self._cells[-1][-1]:
                solution: list[Cell] = []
                cur = cell
                while cur in parents:
                    solution.append(cur)
                    cur = parents[cur]
                solution.append(self._cells[0][0])
                solution.reverse()
                for i in range(1, len(solution)):
                    self._animate()
                    solution[i - 1].draw_move(solution[i])
                return True
            
            neighbors = [n for n in self._get_neighbors(cell) if not n.visited]
            for neighbor in neighbors:
                parents[neighbor] = cell
                to_visit.append(neighbor)
        return False
    
    def _solve_a_star(self) -> bool:
        pass

    def _get_neighbors(self, cell: Cell) -> list[Cell]:
        def in_bounds(c, r):
            if c < 0 or r < 0:
                return False
            if c >= len(self._cells) or r >= len(self._cells[0]):
                return False
            return True
        neighbors: list[Cell] = []
        # we do bottom and right first, as the maze goes from top left to bottom right
        c, r = cell.col_ind, cell.row_ind
        if not cell.bottom_wall and in_bounds(c, r + 1):
            neighbors.append(self._cells[c][r + 1])
        if not cell.right_wall and in_bounds(c + 1, r):
            neighbors.append(self._cells[c + 1][r])
        if not cell.top_wall and in_bounds(c, r - 1):
            neighbors.append(self._cells[c][r - 1])
        if not cell.left_wall and in_bounds(c - 1, r):
            neighbors.append(self._cells[c - 1][r])
        return neighbors
