from maze import Maze, MazePath, MazeGenerator, MazeSolver
import random


class MazeGeneratorDFS(MazeGenerator):
    DIRECTIONS: tuple[tuple[int, int], ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def generate(self, dimensions: tuple[int, int]) -> Maze:
        maze = Maze(dimensions)
        width, height = dimensions
        # maze.generate_start_and_end()
        self._carve(maze, (0, 0))
        maze.set_start((0, 0))
        maze.set_end((width - 2, height - 1))
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


class MazeSolverDFS(MazeSolver):
    def solve(self, maze: Maze) -> MazePath:
        visited: set[tuple[int, int]] = set()

        def dfs(pos: tuple[int, int]) -> bool:
            if pos in visited:
                return False
            visited.add(pos)
            maze.path.add(pos)
            if pos == maze.end:
                return True
            for neighbor in maze.open_neighbors(pos):
                if dfs(neighbor):
                    return True
            maze.path.cells.pop()
            return False

        if not dfs(maze.start):
            raise ValueError("no path found")
        return maze.path


maze = MazeGeneratorDFS().generate((30, 20))
print(maze)
print("\n\n")
solver = MazeSolverDFS()
solver.solve(maze)
print(maze)
