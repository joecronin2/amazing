from game import MazeGame
from generators import MazeGeneratorDFS
from solverapp import MazeSolverApp
from solvers import MazeSolverDFS
from output import create_output


def main():
    # app = MazeSolverApp()
    gen = MazeGeneratorDFS()
    solver = MazeSolverDFS()
    app = MazeGame(gen, solver)
    create_output(app)
    app.run()


if __name__ == "__main__":
    main()
