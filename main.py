from window import *
from maze import Maze

def main():
    width = 1080
    height = 720
    window = Window(width, height)

    cell_size = 47
    maze = Maze(
        5,
        5,
        ((height - 5) // cell_size),
        ((width - 5) // cell_size),
        cell_size,
        cell_size,
        window=window,
        animation_step_time=0.001
    )

    window.wait_for_close()

if __name__ == "__main__":
    main()