from window import *
from maze import Maze

def main():
    width = 1080
    height = 720
    window = Window(width, height)

    cell_size = 47
    maze = Maze(
        x1=5,
        y1=5,
        num_rows=((height - 5) // cell_size),
        num_cols=((width - 5) // cell_size),
        cell_size_x=cell_size,
        cell_size_y=cell_size,
        window=window,
        animation_step_time=0.001
    )

    # choose your solver method here
    solved = maze.solve("bfs")

    print(("Maze was solved!" if solved else "Maze could not be solved :("))

    window.wait_for_close()

if __name__ == "__main__":
    main()