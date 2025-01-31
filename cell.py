from shapes import *
from window import Window

class Cell():
    _default_color = "black"
    def __init__(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        window: Window | None = None,
        color: str = None
    ):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self.window = window
        
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True

        self.fill_color = color if color else self._default_color
        self.no_color = self.window.root.cget("background") if self.window else "white"

    def draw(self):
        self._draw_line(self._x1, self._y1, self._x1, self._y2,
            self.fill_color if self.left_wall else self.no_color
        )
        self._draw_line(self._x2, self._y1, self._x2, self._y2,
            self.fill_color if self.right_wall else self.no_color
        )
        self._draw_line(self._x1, self._y1, self._x2, self._y1,
            self.fill_color if self.top_wall else self.no_color
        )
        self._draw_line(self._x1, self._y2, self._x2, self._y2,
            self.fill_color if self.bottom_wall else self.no_color
        )
    
    def _draw_line(self, p1_x, p1_y, p2_x, p2_y, color: str):
        self.window.draw_line(
            Line(
                Point(p1_x, p1_y),
                Point(p2_x, p2_y)
            ),
            color
        )
    
    def draw_move(self, other: 'Cell', undo=False):
        if not self.window:
            return
        color = "red" if not undo else "gray"
        self.window.draw_line(
            Line(self.center(), other.center()),
            color
        )

    def center(self) -> Point:
        return Point(
            (self._x1 + self._x2) // 2,
            (self._y1 + self._y2) // 2
        )
