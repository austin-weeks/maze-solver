from dataclasses import dataclass
from tkinter import Canvas

@dataclass
class Point():
    x: int
    y: int
        
STROKE_WIDTH = 2
class Line():
    def __init__(self, point_a: Point, point_b: Point, stroke_width: int | None = None):
        self.a = point_a
        self.b = point_b
        self._stroke_width = stroke_width if stroke_width else STROKE_WIDTH

    def draw(self, canvas: Canvas, fill_color: str, stroke_width: int | None = None):
        canvas.create_line(
            self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=stroke_width if stroke_width else self._stroke_width 
        )
        