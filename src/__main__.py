# from maze import Maze, MazeCell
from TestImpl import MazeGeneratorDFS, MazeSolverDFS


def main() -> None:
    maze = MazeGeneratorDFS().generate((30, 20))
    print(maze)
    print("\n\n")
    solver = MazeSolverDFS()
    solver.solve(maze)
    print(maze)


if __name__ == "__main__":
    main()
