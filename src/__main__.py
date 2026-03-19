from TestImpl import MazeGeneratorDFS, MazeSolverDFS
from graphic import MlxMazeRenderer, MlxAPI


class MazeApp:
    def __init__(self, dims: tuple[int, int] = (31, 21), size: int = 20):
        self.size, self.maze = size, MazeGeneratorDFS().generate(dims)
        # MazeSolverDFS().solve(self.maze)
        self.w, self.h = self.maze.width * size, self.maze.height * size
        self.api, self.win, self.renderer = None, None, None

    def _setup_hooks(self) -> None:
        if not self.api or not self.win:
            return
        api, win = self.api, self.win
        api.on_key_down(win, self._handle_input, self)
        api.on_close(win, lambda _: api.loop_exit())
        api.on_loop(self._update, self)

    def _handle_input(self, code: int, _) -> None:
        if self.api and code == 65307:
            self.api.loop_exit()

    def _update(self, _) -> int:
        if self.renderer:
            self.renderer.render()
        return 0

    def run(self) -> None:
        with MlxAPI() as api:
            self.api, self.win = api, api.create_window((self.w, self.h), "A-Maze-Ing")
            self.renderer = MlxMazeRenderer(api, self.win, self.maze, self.size)
            self._setup_hooks()
            api.loop()


def main():
    app = MazeApp()
    app.run()


if __name__ == "__main__":
    main()
