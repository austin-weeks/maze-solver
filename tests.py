import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(maze._cells), num_cols)
        self.assertEqual(len(maze._cells[0]), num_rows)

    def test_create_entrance_exit(self):
        maze = Maze(0, 0, 5, 5, 10, 10)
        self.assertFalse(maze._cells[0][0].top_wall)
        self.assertFalse(maze._cells[-1][-1].bottom_wall)

    def test_reset_cells_visit(self):
        maze = Maze(0, 0, 5, 5, 10, 10)
        for i in range(maze.num_cols):
            for j in range(maze.num_rows):
                self.assertFalse(maze._cells[i][j].visited)

    def test_dfs(self):
        maze = Maze(0, 0, 10, 10, 5, 5)
        self.assertTrue(maze.solve("dfs"))

    def test_bfs(self):
        maze = Maze(0, 0, 10, 10, 5, 5)
        self.assertTrue(maze.solve("bfs"))

    def test_a_star(self):
        maze = Maze(0, 0, 10, 10, 5, 5)
        self.assertTrue(maze.solve("a*"))

if __name__ == "__main__":
    unittest.main()