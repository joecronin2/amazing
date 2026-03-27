from generators import MazeGeneratorDFS
from graphic import MlxMazeRenderer, MlxAPI
from typing import Any, Optional, Callable


class MazeGame:
    def __init__(self, dims: tuple[int, int] = (31, 21), size: int = 20):
        self.size = size
        self.maze = MazeGeneratorDFS().generate(dims)
        self.player_pos = self.maze.start

        self.w, self.h = self.maze.width * size, self.maze.height * size

        self.api: Optional[MlxAPI] = None
        self.win: Any = None
        self.renderer: Optional[MlxMazeRenderer] = None

        self.visited: set[tuple[int, int]] = {self.player_pos}

        self.actions: dict[int, Callable[[], Any]] = {
            65361: lambda: self._move_player((-1, 0)),
            65362: lambda: self._move_player((0, -1)),
            65363: lambda: self._move_player((1, 0)),
            65364: lambda: self._move_player((0, 1)),
            65307: self._exit,
        }

    def _move_player(self, d: tuple[int, int]) -> None:
        n = (self.player_pos[0] + d[0], self.player_pos[1] + d[1])
        if self.maze.in_bounds(n) and not self.maze.is_wall(n):
            self.player_pos = n
            self.visited.add(n)
            if n == self.maze.end:
                self._exit()

    def _setup_hooks(self) -> None:
        if not self.api or not self.win:
            return
        api, win = self.api, self.win
        api.on_key_down(win, self._handle_input, self)
        api.on_close(win, lambda _: api.loop_exit())
        api.on_loop(self._update, self)

    def _handle_input(self, code: int, _) -> None:
        if action := self.actions.get(code):
            action()

    def _update(self, _) -> int:
        if self.renderer:
            self.renderer.render(self.player_pos, self.visited)
        return 0

    def _exit(self) -> None:
        if self.api:
            self.api.loop_exit()

    def run(self) -> None:
        with MlxAPI() as api:
            self.api = api
            self.win = api.create_window((self.w, self.h), "A-Maze-Ing")
            self.renderer = MlxMazeRenderer(api, self.win, self.maze, self.size)
            self._setup_hooks()
            api.loop()
