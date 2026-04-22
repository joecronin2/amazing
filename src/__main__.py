from game import MazeGame
from generators import MazeGeneratorDFS
from solverapp import MazeSolverApp
from solvers import MazeSolverDFS


def main():
    # app = MazeSolverApp()
    gen = MazeGeneratorDFS()
    solver = MazeSolverDFS()
    app = MazeGame(gen, solver)
    app.run()


if __name__ == "__main__":
    main()
