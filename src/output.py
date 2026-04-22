from io import TextIOWrapper
from maze import Maze
from game import MazeGame


def hexify_maze(maze: Maze, f: TextIOWrapper):
    for y in range(maze.height):
        for x in range(maze.width):
            h = maze.bin_neighbors((x, y))
            f.write(hex(h)[2])
        f.write("\n")


def directify_solution(game: MazeGame, f: TextIOWrapper):
    solution = game.solver.solve(game.maze)
    for cell, i in zip(solution, range(len(solution))):
        if cell is solution[-1]:
            break
        x, y = cell
        if (x + 1, y) == solution[i+1]:
            f.write("E")
        elif (x - 1, y) == solution[i+1]:
            f.write("W")
        elif (x, y + 1) == solution[i+1]:
            f.write("S")
        elif (x, y - 1) == solution[i+1]:
            f.write("N")
    f.write("\n")


def create_output(game: MazeGame, output_file: str = "output.txt"):
    with open(output_file, "w") as f:
        hexify_maze(game.maze, f)
        f.write("\n")
        f.write(str(game.maze.start).removeprefix("(").removesuffix(")"))
        f.write("\n")
        f.write(str(game.maze.end).removeprefix("(").removesuffix(")"))
        f.write("\n")
        directify_solution(game, f)
