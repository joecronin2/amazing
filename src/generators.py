from maze import Maze, MazeGenerator
import random


class MazeGeneratorDFS(MazeGenerator):
    DIRECTIONS: tuple[tuple[int, int], ...] = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    )

    def generate(self, dimensions: tuple[int, int]) -> Maze:
        width, height = dimensions
        maze = Maze((width, height))
        self._carve(maze, (0, 0))
        start_y = random.randrange(0, height, 2)
        maze.set_start((0, start_y))
        end_y = random.randrange(0, height, 2)
        maze.set_end((width - 1, end_y))
        return maze

    def _carve(self, maze: Maze, pos: tuple[int, int]) -> None:
        maze.set_open(pos)
        x, y = pos
        directions = list(self.DIRECTIONS)
        random.shuffle(directions)

        for dx, dy in directions:
            jump = (x + 2 * dx, y + 2 * dy)
            if maze.in_bounds(jump) and maze.is_wall(jump):
                wall = (x + dx, y + dy)
                maze.set_open(wall)
                self._carve(maze, jump)
