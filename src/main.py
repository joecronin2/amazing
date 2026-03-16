from maze import Maze, MazeCell

def main() -> None:
    maze: Maze = Maze(30, 30)
    maze.randomize([MazeCell.WALL, MazeCell.EMPTY])

if __name__ == "__main__":
    main()
