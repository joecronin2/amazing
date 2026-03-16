from maze import Maze, MazeGenerator, MazeSolver
import random

def render_ascii_no_edges(maze: Maze) -> None:
    symbols = {True: "#", False: " "}
    for y in range(maze.height):
        line = ""
        for x in range(maze.width):
            if (x, y) == maze.start:
                line += "S"
            elif (x, y) == maze.end:
                line += "E"
            else:
                line += symbols[maze.is_wall(x, y)]
        print(line)


class MazeGeneratorDFS(MazeGenerator):
    def generate(self, width: int, height: int) -> Maze:
        maze = Maze(width, height)
        maze.set_start(0, 0)
        maze.set_end(width - 1, height - 1)
        self._carve(maze, 0, 0)
        return maze

    def _carve(self, maze: Maze, x: int, y: int) -> None:
        maze.set_open(x, y)
        dirs = list(maze.neighbors(x, y))
        random.shuffle(dirs)
        for nx, ny in dirs:
            jump_x, jump_y = nx + (nx - x), ny + (ny - y)
            if maze.in_bounds(jump_x, jump_y) and maze.is_wall(jump_x, jump_y):
                wall_x, wall_y = (x + jump_x) // 2, (y + jump_y) // 2
                maze.set_open(wall_x, wall_y)
                self._carve(maze, jump_x, jump_y)


class MazeSolverDFS(MazeSolver):
    def solve(self, maze: Maze) -> MazePath:



maze = MazeGeneratorDFS().generate(10, 10)
render_ascii_no_edges(maze)
