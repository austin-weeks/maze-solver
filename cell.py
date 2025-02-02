from shapes import *
from window import Window

WALL_WIDTH = 2
WALL_COLOR = "#171717"
class Cell():
    def __init__(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        col_ind: int,
        row_ind: int,
        window: Window | None = None,
        color: str = None
    ):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        self.col_ind = col_ind
        self.row_ind = row_ind

        self.window = window
        
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True

        self.visited = False

        self.fill_color = color if color else WALL_COLOR
        self.no_color = self.window.root.cget("background") if self.window else "white"

    def draw(self):
        self._draw_wall(self._x1, self._y1, self._x1, self._y2,
            self.fill_color if self.left_wall else self.no_color
        )
        self._draw_wall(self._x2, self._y1, self._x2, self._y2,
            self.fill_color if self.right_wall else self.no_color
        )
        self._draw_wall(self._x1, self._y1, self._x2, self._y1,
            self.fill_color if self.top_wall else self.no_color
        )
        self._draw_wall(self._x1, self._y2, self._x2, self._y2,
            self.fill_color if self.bottom_wall else self.no_color
        )
    
    def _draw_wall(self, p1_x, p1_y, p2_x, p2_y, color: str):
        self.window.draw_line(
            Line(
                Point(p1_x, p1_y),
                Point(p2_x, p2_y)
            ),
            color,
            stroke_width=WALL_WIDTH
        )
    
    def draw_move(self, other: 'Cell', undo=False):
        if not self.window:
            return
        color = "#6366f1" if not undo else "#71717a"
        self.window.draw_line(
            Line(self.center(), other.center()),
            color
        )

    def center(self) -> Point:
        return Point(
            (self._x1 + self._x2) // 2,
            (self._y1 + self._y2) // 2
        )
    
    def __lt__(self, other):
        if not isinstance(other, Cell):
            return False
        return True
