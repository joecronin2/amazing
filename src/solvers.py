from maze import Maze, MazeSolver


class MazeSolverDFS(MazeSolver):
    def solve(self, maze: Maze) -> list[tuple[int, int]]:
        stack = [(maze.start, [maze.start])]  # (position, path so far)
        while stack:
            pos, path = stack.pop()
            if pos == maze.end:
                return path
            for neighbor in maze.open_neighbors(pos):
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))
        raise ValueError("no path found")
