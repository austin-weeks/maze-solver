from cell import Cell
from shapes import *
from window import Window
import time

class Maze():
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window | None = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self._cells: list[list[Cell]] = []

        self._create_cells()

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
                col.append(cell)
            cells.append(col)
        self._cells = cells
        self._draw_cells()

    def _draw_cells(self):
        if not self.window:
            return
        for row in self._cells:
            for cell in row:
                cell.draw()
                self._animate()

    def _animate(self):
        if not self.window:
            return
        self.window.redraw()
        time.sleep(0.01)
