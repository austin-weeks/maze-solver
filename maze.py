from cell import Cell
from shapes import *
from window import Window
import time, random

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

    def _create_cells(self):
        cells = []
        for c in range(self.num_cols):
            x = self.x1 + (self.cell_size_x * c)
            col = []
            for r in range(self.num_rows):
                y = self.y1 + (self.cell_size_y * r)
                cell = Cell(
                    x,
                    x + self.cell_size_x,
                    y,
                    y + self.cell_size_y,
                    self.window,
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
