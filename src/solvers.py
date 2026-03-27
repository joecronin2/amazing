from maze import Maze, MazeSolver


class MazeSolverDFS(MazeSolver):
    def solve(self, maze: Maze) -> list[tuple[int, int]]:
        path = list(set())

        def dfs(pos: tuple[int, int]) -> bool:
            if pos in path:
                return False
            path.append(pos)
            if pos == maze.end:
                return True
            for neighbor in maze.open_neighbors(pos):
                if dfs(neighbor):
                    return True
            path.pop()
            return False

        if not dfs(maze.start):
            raise ValueError("no path found")
        return path
