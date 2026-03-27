from maze import Maze, MazeSolver, MazePath


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
