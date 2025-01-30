from dataclasses import dataclass
from tkinter import Canvas

@dataclass
class Point():
    x: int
    y: int
        

class Line():
    _stroke_width = 2
    def __init__(self, point_a: Point, point_b: Point):
        self.a = point_a
        self.b = point_b
    
    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=self._stroke_width
        )
        