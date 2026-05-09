from maze import Maze, MazeGenerator
import random


class MazeGeneratorDFS(MazeGenerator):
    def generate(self, dimensions: tuple[int, int]) -> Maze:
        width, height = dimensions
        maze = Maze((width, height))
        self._carve_iterative(maze, (0, 0))
        start_y = random.randrange(0, height, 2)
        maze.set_start((0, start_y))
        end_y = random.randrange(0, height, 2)
        maze.set_end((width - 1, end_y))
        return maze

    def _carve_iterative(self, maze: Maze, start: tuple[int, int]) -> None:
        stack = [start]
        maze.set_open(start)
        while stack:
            x, y = stack[-1]
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            carved = False
            for dx, dy in directions:
                jump = (x + 2 * dx, y + 2 * dy)
                if maze.in_bounds(jump) and maze.is_wall(jump):
                    wall = (x + dx, y + dy)
                    maze.set_open(wall)
                    maze.set_open(jump)
                    stack.append(jump)
                    carved = True
                    break
            if not carved:
                stack.pop()
