from tkinter import Tk, Canvas
from shapes import *

class Window():
    def __init__(self, width: int, height: int):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.width = width
        self.height = height
        self.canvas = Canvas(height=height, width=width)
        self.canvas.pack()

        self.running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        """
        Main method for starting the window.
        Drawing lines should be performed before calling this method.
        """
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)