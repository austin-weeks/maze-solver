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
        window: Window,
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
        self.color = color if color else self._default_color

    def draw(self):
        if self.left_wall:
            self._draw_line(self._x1, self._y1, self._x1, self._y2)
        if self.right_wall:
            self._draw_line(self._x2, self._y1, self._x2, self._y2)
        if self.top_wall:
            self._draw_line(self._x1, self._y1, self._x2, self._y1)
        if self.bottom_wall:
            self._draw_line(self._x1, self._y2, self._x2, self._y2)
        
    
    def _draw_line(self, p1_x, p1_y, p2_x, p2_y):
        self.window.draw_line(
            Line(
                Point(p1_x, p1_y),
                Point(p2_x, p2_y)
            ),
            self.color
        )
    
    def draw_move(self, other: 'Cell', undo=False):
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
