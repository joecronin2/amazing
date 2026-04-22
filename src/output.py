from maze import Maze


def create_output(maze: Maze, output_file: str = "output.txt"):
    with open(output_file, "w") as f:
        for y in range(maze.height):
            for x in range(maze.width):
                h = maze.bin_neighbors((x, y))
                f.write(hex(h)[2])
            f.write("\n")
        f.write("\n")
        f.write(str(maze.start).removeprefix("(").removesuffix(")"))
        f.write("\n")
        f.write(str(maze.end).removeprefix("(").removesuffix(")"))
        f.write("\n")
