from window import *
from maze import Maze
import time

def main():
    width = 1280
    height = 720
    window = Window(width, height)

    cell_size = 5
    maze = Maze(
        x1=5,
        y1=5,
        num_rows=((height - 5) // cell_size),
        num_cols=((width - 5) // cell_size),
        cell_size_x=cell_size,
        cell_size_y=cell_size,
        window=window,
        maze_creation_animation_time=0,
        maze_solving_animation_time=0,
        seed=12345
    )
    time.sleep(0.5)

    # choose your solver method here
    solved = maze.solve("dfs")

    print(("Maze was solved!" if solved else "Maze could not be solved :("))

    window.wait_for_close()

if __name__ == "__main__":
    main()